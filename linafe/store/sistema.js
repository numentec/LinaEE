export const state = () => ({
  user: null,
})
export const mutations = {
  SET_USER_DATA(state, payload) {
    state.user = payload
    localStorage.setItem('user', JSON.stringify(payload))
  },
}
export const actions = {
  async login({ $axios, commit, error }, credentials) {
    try {
      const { data } = await $axios.post('/loguin/', credentials)
      $axios.defaults.headers.common.Authorization = `Bearer ${data.token}`
      commit('SET_USER_DATA', data)
      return {
        data,
      }
    } catch (e) {
      error({
        statusCode: 401,
        message: 'Failed registering user',
      })
    }
  },
  async registerUser({ $axios, commit, error }, credentials) {
    try {
      const { data } = await $axios.post('/users/register/', credentials)
      return {
        data,
      }
    } catch (e) {
      error({
        statusCode: 401,
        message: 'Failed registering user',
      })
    }
  },
  setUserData({ $axios, commit, error }, userData) {
    $axios.defaults.headers.common.Authorization = `Bearer ${userData.token}`
    commit('SET_USER_DATA', userData)
  },
}
export const getters = {
  loggedIn(state) {
    return !!state.user
  },
}
