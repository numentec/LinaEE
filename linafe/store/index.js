export const state = () => ({
  drawer_image:
    'https://demos.creative-tim.com/material-dashboard/assets/img/sidebar-1.jpg',
  drawer: null,
  mini_variant: true,
  is_mini: true,
})
export const mutations = {
  SET_DRAWER_IMAGE(state, payload) {
    state.drawer_image = payload
  },
  SET_DRAWER(state, payload) {
    state.drawer = payload
  },
  SET_MINI_VARIANT(state, payload) {
    state.mini_variant = payload
  },
  SET_IS_MINI(state, payload) {
    state.is_mini = payload
  },
}
export const actions = {
  setMiniVariant({ commit }, payload) {
    commit('SET_MINI_VARIANT', payload)
  },
  setIsMini({ commit }, payload) {
    commit('SET_IS_MINI', payload)
  },
}
