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
    location.reload()
  },
}

export const actions = {
  async userLogin({ commit }, credentials) {
    try {
      await this.$auth
        .loginWith('local', {
          data: credentials,
        })
        .then(({ data }) => {
          commit('SET_USER_DATA', data.user)
        })
    } catch (err) {
      this.error = err.response.data.message
    }
  },

  async registerUser({ commit, error }, credentials) {
    try {
      await this.$axios.post('/users/register/', credentials)
    } catch (err) {
      this.error = err
    }
  },

  async userLogout({ commit }) {
    await this.$auth.logout()
    commit('USER_LOGOUT')
  },
}
