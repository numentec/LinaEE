export const namespaced = true

export const state = () => ({
  user: null,
  tokens: {
    access: '',
    refresh: '',
  },
  error: null,
})

export const mutations = {
  SET_TOKENS_DATA(state, payload) {
    state.tokens = payload
    this.$axios.defaults.headers.common.Authorization = `Bearer ${payload.access}`
    localStorage.setItem('tokens', JSON.stringify(payload))
  },
  SET_USER_DATA(state, payload) {
    state.user = payload
    localStorage.setItem('user', JSON.stringify(payload))
  },
  USER_LOGOUT() {
    localStorage.removeItem('user')
    localStorage.removeItem('tokens')
    location.reload()
  },
}

export const actions = {
  async userLogin({ commit }, credentials) {
    await this.$axios
      .post('/login/', credentials)
      .then(({ data }) => {
        commit('SET_TOKENS_DATA', data)
      })
      .then((response) => {
        return this.$axios.get('/user_perms/cur').then(({ data }) => {
          commit('SET_USER_DATA', data)
        })
      })
  },

  async registerUser({ commit, error }, credentials) {
    try {
      await this.$axios.post('/users/register/', credentials)
    } catch (err) {
      this.error = err
    }
  },

  userLogout({ commit }) {
    commit('USER_LOGOUT')
  },
}

export const getters = {
  loggedIn(state) {
    return !!state.user
  },
}
