/* eslint-disable no-console */
import CustomStore from 'devextreme/data/custom_store'

export const namespaced = true

export const state = () => ({
  filters: {},
  isLoading: false,
})

export const mutations = {
  SET_LOADING_STATUS(state) {
    state.isLoading = !state.isLoading
  },
  SET_FILTERS(state, payload) {
    state.filters = payload
  },
}

export const actions = {
  setFilters({ commit }, payload) {
    // Quita los elementos que sean null, '' o undefined
    const auxfilters = Object.entries(payload).reduce(
      (a, [k, v]) => (v ? ((a[k] = v), a) : a),
      {}
    )
    commit('SET_FILTERS', auxfilters)
  },
  setIsLoading({ commit }) {
    commit('SET_LOADING_STATUS')
  },
  fetchCatalogData(context) {
    context.commit('SET_LOADING_STATUS')

    const ctx = context
    const ax = this.$axios

    async function load() {
      return await ax
        .get('linabi/catalog/', {
          params: ctx.state.filters,
        })
        .then((response) => response.data)
    }

    const store = new CustomStore({ key: 'ID', load })

    context.commit('SET_LOADING_STATUS')

    return store
  },
}

export const getters = {
  getFilters(state) {
    return state.filters
  },
  // getTotalRows(state) {
  //   return state.dataSource.length
  // },
}
