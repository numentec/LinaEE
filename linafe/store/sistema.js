export const state = () => ({
  user: null,
  tokens: {
    access: '',
    refresh: '',
  },
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
  LOGOUT_USER() {
    localStorage.removeItem('user')
    location.reload()
  },
}
export const actions = {
  async userLogin({ commit, error }, credentials) {
    try {
      await this.$axios.post('/login/', credentials).then(({ tokensData }) => {
        commit('SET_TOKENS_DATA', tokensData)
      })

      await this.$axios.post('/user_perms/cur').then(({ userData }) => {
        commit('SET_USER_DATA', userData)
      })
    } catch (err) {
      error({
        statusCode: err.statusCode,
        message: err.message,
      })
    }
  },

  async registerUser({ commit, error }, credentials) {
    try {
      await this.$axios.post('/users/register/', credentials)
    } catch (err) {
      error({
        statusCode: err.statusCode,
        message: err.message,
      })
    }
  },

  logoutUser({ commit }) {
    commit('LOGOUT_USER')
  },
}
export const getters = {
  loggedIn(state) {
    return !!state.user
  },
}
