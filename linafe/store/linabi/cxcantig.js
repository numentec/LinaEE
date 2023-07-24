/* eslint-disable no-console */
import CustomStore from 'devextreme/data/custom_store'
// import { getField, updateField } from 'vuex-map-fields'

export const namespaced = true

export const state = () => ({
  curStore: [],
  changes: [],
  filters: {},
  isLoading: false,
  totalCount: 0,
  breadCrumbsItems: [],
})

export const mutations = {
  SET_CUR_STORE(state, payload) {
    state.curStore = payload
  },
  SET_LOADING_STATUS(state) {
    state.isLoading = !state.isLoading
  },
  SET_FILTERS(state, payload) {
    state.filters = Object.assign({}, payload)
  },
  SET_DATES(state, payload) {
    state.filters.p12 = payload.p12
    state.filters.p13 = payload.p13
  },
  SET_TOTAL_COUNT(state, payload) {
    state.totalCount = payload
  },
  SET_BREAD_CRUMBS_ITEMS(state, payload) {
    if (payload.length) {
      state.breadCrumbsItems = payload
    }
  },
  SET_CHANGES(state, changes) {
    state.changes = changes
  },
}

export const actions = {
  setFilters({ commit }, payload) {
    commit('SET_FILTERS', payload)
  },
  setCurStore({ commit }, payload) {
    commit('SET_CUR_STORE', payload)
  },
  setDates({ commit }, payload) {
    commit('SET_DATES', payload)
  },
  setIsLoading({ commit }) {
    commit('SET_LOADING_STATUS')
  },
  setTotalCount({ commit }, payload) {
    commit('SET_TOTAL_COUNT', payload)
  },
  fetchData(context) {
    context.commit('SET_LOADING_STATUS')

    const ctx = context
    const ax = this.$axios
    const usefilters = ctx.state.filters

    // Quita los elementos que sean null, '' o undefined
    // y convierte en string el valor de la propiedad de cada objeto restante
    const curparams = Object.entries(usefilters).reduce(
      (a, [k, v]) => (v ? ((a[k] = v.toString()), a) : a),
      {}
    )

    async function load() {
      return await ax
        .get('linabi/cxcantig/', {
          params: curparams,
        })
        .then((response) => response.data)
    }

    const store = new CustomStore({
      key: 'NO_CLIENTE',
      load,
      onLoaded: (data) => {
        context.commit('SET_CUR_STORE', data)
      },
    })

    context.commit('SET_LOADING_STATUS')

    return store
  },
  setBreadCrumbsItems({ commit }, payload) {
    commit('SET_BREAD_CRUMBS_ITEMS', payload)
  },
  setChanges({ commit }, payload) {
    commit('SET_CHANGES', payload)
  },
}

export const getters = {
  getFilters(state) {
    return state.filters
  },
  getCurStore(state) {
    return state.curStore
  },
  getTotalCount(state) {
    return state.totalCount
  },
  getBreadCrumbsItems(state) {
    return state.breadCrumbsItems
  },
  isLoading(state) {
    return state.isLoading
  },
}
