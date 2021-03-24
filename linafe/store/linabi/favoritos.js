export const namespaced = true

export const state = () => ({
  breadCrumbs: [
    {
      text: 'Favoritos',
      disabled: false,
      href: '/linabi/favoritos',
    },
  ],
})

export const mutations = {
  SET_BREAD_CRUMBS(state, payload) {
    state.breadCrumbs = payload
  },
}

export const actions = {
  setBreadCrumbs({ commit }, payload) {
    commit('SET_BREAD_CRUMBS', payload)
  },
}

export const getters = {
  getBreadCrumbs(state) {
    return state.breadCrumbs
  },
}
