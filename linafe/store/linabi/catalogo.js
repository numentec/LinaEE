/* eslint-disable no-console */
import CustomStore from 'devextreme/data/custom_store'
import { getField, updateField } from 'vuex-map-fields'

export const namespaced = true

export const state = () => ({
  curStore: [],
  curVariants: [],
  filters: {},
  isLoading: false,
  totalCount: 0,
  breadCrumbsItems: [],
})

export const mutations = {
  updateField,
  SET_CUR_STORE(state, payload) {
    state.curStore = payload
  },
  SET_CUR_VARIANTS(state, payload) {
    state.curVariants = payload
  },
  SET_LOADING_STATUS(state) {
    state.isLoading = !state.isLoading
  },
  SET_FILTERS(state, payload) {
    state.filters = Object.assign({}, state.filters, payload)
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
  setCurStore({ commit }, payload) {
    commit('SET_CUR_STORE', payload)
  },
  setCurVariants({ state, commit }, payload) {
    const auxvariants = state.curVariants

    if (payload) {
      payload.forEach((obj) => {
        !auxvariants.includes(obj) && auxvariants.push(obj)
      })
    }

    commit('SET_CUR_VARIANTS', auxvariants)
  },
  clearCurVariants({ commit }) {
    commit('SET_CUR_VARIANTS', [])
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

    // Quita los elementos que sean null, '' o undefined
    // y convierte en string el valor de la propiedad de cada objeto restante
    const curparams = Object.entries(ctx.state.filters).reduce(
      (a, [k, v]) => (v ? ((a[k] = v), a) : a),
      {}
    )

    async function load() {
      return await ax
        .get('linabi/catalog/', {
          params: curparams,
        })
        .then((response) => response.data)
    }

    const store = new CustomStore({
      key: 'SKU',
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
}

export const getters = {
  getField,
  getCurStore(state) {
    return state.curStore
  },
  getCurVariants(state) {
    return state.curVariants
  },
  getProdVariants(state, sku) {
    const prodvariants = state.curVariants
    return prodvariants.filter((obj) => obj.SKU === sku)
  },
  getTotalCount(state) {
    return state.totalCount
  },
  getBreadCrumbsItems(state) {
    return state.breadCrumbsItems
  },
}
