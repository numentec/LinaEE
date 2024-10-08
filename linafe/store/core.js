export const namespaced = true

export const state = () => ({
  drawer: false,
  drawer_image:
    'https://demos.creative-tim.com/material-dashboard/assets/img/sidebar-1.jpg',
  is_mini: true,
  is_expanded: false,
  curCia: { name: 'CIA', id: '01' },
})

export const mutations = {
  SET_DRAWER_IMAGE(state, payload) {
    state.drawer_image = payload
  },
  SET_DRAWER(state, payload) {
    state.drawer = payload
  },
  SET_IS_MINI(state, payload) {
    state.is_mini = payload
  },
  SET_IS_EXPANDED(state, payload) {
    state.is_expanded = payload
  },
  SET_CURCIA(state, payload) {
    state.curCia.name = payload.name
    state.curCia.id = payload.id
  },
}

export const actions = {
  setDrawer({ commit }, payload) {
    commit('SET_DRAWER', payload)
  },
  setDrawerImage({ commit }, payload) {
    commit('SET_DRAWER_IMAGE', payload)
  },
  setIsMini({ commit }, payload) {
    commit('SET_IS_MINI', payload)
  },
  setIsExpanded({ commit }, payload) {
    commit('SET_IS_EXPANDED', payload)
  },
  setCurCia({ commit }, payload) {
    commit('SET_CURCIA', payload)
  },
}

export const getters = {
  getCurCia(state) {
    return state.curCia
  },
}
