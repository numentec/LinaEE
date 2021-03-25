export const namespaced = true

export const state = () => ({
  breadCrumbsItems: [],
})

export const mutations = {
  SET_BREAD_CRUMBS_ITEMS(state, payload) {
    if (payload.length) {
      state.breadCrumbsItems = payload
    }
  },
}

export const actions = {
  setBreadCrumbsItems({ commit }, payload) {
    commit('SET_BREAD_CRUMBS_ITEMS', payload)
  },
}

export const getters = {
  getBreadCrumbsItems(state) {
    return state.breadCrumbsItems
  },
}
