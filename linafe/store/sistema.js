export const namespaced = true

export const state = () => ({
  curuser: null,
  error: null,
})

export const mutations = {
  SET_USER_DATA(state, payload) {
    this.$auth.setUser(payload)
    state.curuser = payload
    localStorage.setItem('curuser', JSON.stringify(payload))
  },
  USER_LOGOUT() {
    localStorage.removeItem('curuser')
    // location.reload()
  },
  SET_ERROR(state, payload) {
    state.error = payload
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
        commit('SET_ERROR', null)
      })
      .catch((err) => {
        commit('SET_ERROR', err.response.data.non_field_errors[0])
      })
  },

  async registerUser({ commit, error }, userdata) {
    try {
      await this.$axios.$post('user_register/', userdata)
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
}
