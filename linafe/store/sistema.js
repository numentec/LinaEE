/* eslint-disable no-console */
import CustomStore from 'devextreme/data/custom_store'

export const namespaced = true

function clearLocalStorage(prefix) {
  for (const key in localStorage) {
    if (key.startsWith(prefix)) {
      localStorage.removeItem(key)
    }
  }
}

export const state = () => ({
  curuser: null,
  users: [],
  isLoading: false,
  error: { statusCode: 0, message: '' },
  cias: [],
  curCia: null,
  showBottomNav: true,
})

export const mutations = {
  SET_USER_DATA(state, payload) {
    this.$auth.setUser(payload)
    // console.log('SET_USER', this.$auth)
    state.curuser = payload
    localStorage.setItem('lina_curuser', JSON.stringify(payload))
  },
  USER_LOGOUT() {
    state.curuser = null
    clearLocalStorage('lina_')
    // localStorage.removeItem('lina_curuser')
    // location.reload()
  },
  SET_ERROR(state, payload) {
    state.error = payload
  },
  SET_USERS(state, payload) {
    state.users = payload
    localStorage.setItem('lina_users', JSON.stringify(payload))
  },
  SET_LOADING_STATUS(state) {
    state.isLoading = !state.isLoading
  },
  SET_CIAS(state, payload) {
    state.cias = payload
    localStorage.setItem('lina_cias', JSON.stringify(payload))
  },
  SET_CURCIA(state, payload) {
    state.curCia = Object.assign({}, payload)
    localStorage.setItem('lina_curCia', JSON.stringify(payload))
  },
  SET_SHOWBOTTOMNAV(state, payload) {
    state.showBottomNav = payload
    localStorage.setItem('lina_showBottomNav', JSON.stringify(payload))
  },
}

export const actions = {
  async userLogin({ commit }, credentials) {
    await this.$auth
      .loginWith('local', {
        data: credentials,
      })
      .then(({ data }) => {
        commit('SET_USER_DATA', data.user)
        commit('SET_ERROR', { statusCode: 0, message: '' })
      })
      .catch((err) => {
        let error

        if (err.response) {
          let msgerr = 'X'
          if (err.response.data.non_field_errors) {
            msgerr = err.response.data.non_field_errors[0]
          } else if (err.response.data.detail) {
            msgerr = err.response.data.detail
          } else {
            msgerr = err.response.statusText
          }
          error = {
            statusCode: err.response.status,
            message: msgerr,
          }
        } else if (error.request) {
          error = {
            statusCode: 503,
            message: 'No hubo respuesta del servidor',
          }
        } else {
          error = {
            statusCode: 1010,
            message: err.message,
          }
        }
        commit('SET_ERROR', error)
      })
  },

  async registerUser({ commit, error }, userdata) {
    try {
      await this.$axios.$post('profiles/', userdata)
    } catch (err) {
      commit('SET_ERROR', err.response.data.message)
    }
  },

  async userProfile({ commit, error }, userid) {
    try {
      await this.$axios.$get(`profiles/${userid}`).then((data) => {
        commit('SET_USERS', [data])
      })
    } catch (err) {
      commit('SET_ERROR', err.response.data.message)
    }
  },

  async renewPass({ commit, error }, pl) {
    try {
      await this.$axios.$put(`profiles/${pl.uid}/renew-pass/`, pl.pwd)
    } catch (err) {
      commit('SET_ERROR', err.response.data.message)
    }
  },

  async editUser({ commit, error }, userdata) {
    try {
      await this.$axios.$put('profiles/' + userdata.id + '/', userdata)
    } catch (err) {
      commit('SET_ERROR', err.response.data.message)
    }
  },

  async userLogout({ commit }) {
    await this.$auth.logout()
    commit('USER_LOGOUT')
  },

  setUserData({ commit }, payload) {
    commit('SET_USER_DATA', payload)
  },

  setError({ commit }, payload) {
    commit('SET_ERROR', payload)
  },

  fetchUsers({ commit }) {
    const ax = this.$axios

    commit('SET_LOADING_STATUS')

    async function load() {
      return await ax.get('users/actives/').then((response) => response.data)
    }

    const store = new CustomStore({
      key: 'id',
      load,
      onLoaded: (data) => {
        commit('SET_USERS', data)
      },
    })

    commit('SET_LOADING_STATUS')

    return store
  },

  setCias({ commit }, payload) {
    commit('SET_CIAS', payload)
  },

  setCurCia({ commit }, payload) {
    commit('SET_CURCIA', payload)
  },

  setShowBottomNav({ commit }, payload) {
    commit('SET_SHOWBOTTOMNAV', payload)
  },
}

export const getters = {
  getCurUser(state) {
    return state.curuser
  },
  getUsers(state) {
    return state.users
  },
  getCurCia(state) {
    return state.curCia
  },
  getCias(state) {
    return state.cias
  },
  getShowBottomNav(state) {
    return state.showBottomNav
  },
}
