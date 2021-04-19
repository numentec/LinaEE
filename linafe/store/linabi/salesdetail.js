import CustomStore from 'devextreme/data/custom_store'
import { getField, updateField } from 'vuex-map-fields'

export const namespaced = true

export const state = () => ({
  filters: {},
  isLoading: false,
  totalCount: 0,
  breadCrumbsItems: [],
})

export const mutations = {
  updateField,
  SET_LOADING_STATUS(state) {
    state.isLoading = !state.isLoading
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
}

export const actions = {
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

    // Quita los elementos que sean null, '' o undefined
    // y convierte en string el valor de la propiedad de cada objeto restante
    const curparams = Object.entries(ctx.state.filters).reduce(
      (a, [k, v]) => (v ? ((a[k] = v.toString()), a) : a),
      {}
    )

    async function load() {
      return await ax
        .get('linabi/salesdetail/', {
          params: curparams,
        })
        .then((response) => response.data)
    }

    const store = new CustomStore({ key: 'ID', load })

    context.commit('SET_LOADING_STATUS')

    return store
  },
  setBreadCrumbsItems({ commit }, payload) {
    commit('SET_BREAD_CRUMBS_ITEMS', payload)
  },
}

export const getters = {
  getField,
  getTotalCount(state) {
    return state.totalCount
  },
  getBreadCrumbsItems(state) {
    return state.breadCrumbsItems
  },
}
