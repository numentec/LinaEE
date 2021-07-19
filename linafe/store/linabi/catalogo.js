/* eslint-disable no-console */
import CustomStore from 'devextreme/data/custom_store'
// import { getField, updateField } from 'vuex-map-fields'

export const namespaced = true

export const state = () => ({
  curStore: [],
  curCatalog: [],
  photosList: [],
  changes: [],
  curVariants: [],
  filters: {},
  isLoading: false,
  totalCount: 0,
  breadCrumbsItems: [],
})

export const mutations = {
  SET_CUR_STORE(state, payload) {
    state.curStore = payload
  },
  SET_CUR_VARIANTS(state, payload) {
    state.curVariants = payload
  },
  SET_CUR_CATALOG(state, payload) {
    state.curCatalog = payload
  },
  SET_PHOTOS_LIST(state, payload) {
    state.photosList = payload
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
  addToCurCatalog({ commit, state }, payload) {
    let cc = state.curCatalog
    cc = cc.filter((el1) => {
      return !payload.find((el2) => {
        return el2.SKU === el1.SKU
      })
    })

    cc = cc.concat(payload)

    commit('SET_CUR_CATALOG', cc)

    if (state.photosList.length === 0) {
      const pl = Array.from(state.curCatalog, (item) => {
        return {
          sku: item.SKU,
          imgsrc: this.$config.fotosURL + item.SKU + this.$config.fotosExt,
          ordinal: 1,
        }
      })
      commit('SET_PHOTOS_LIST', pl)
    }
  },
  fetchData(context, localFilters = null) {
    context.commit('SET_LOADING_STATUS')

    const ctx = context
    const ax = this.$axios
    let usefilters

    if (localFilters) {
      usefilters = localFilters
    } else {
      usefilters = ctx.state.filters
    }

    // Quita los elementos que sean null, '' o undefined
    // y convierte en string el valor de la propiedad de cada objeto restante
    const curparams = Object.entries(usefilters).reduce(
      (a, [k, v]) => (v ? ((a[k] = v.toString()), a) : a),
      {}
    )

    // curparams = Object.entries(curparams).reduce(
    //   (a, [k, v]) => (v ? ((a[k] = v.toString()), a) : a),
    //   {}
    // )

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
        if (localFilters) {
          context.commit('SET_CUR_CATALOG', data)
        } else {
          context.commit('SET_CUR_STORE', data)
        }
      },
    })

    context.commit('SET_LOADING_STATUS')

    return store
  },
  async fetchCatalogData({ commit, dispatch }, filters = null) {
    commit('SET_LOADING_STATUS')

    // Quita los elementos que sean null, '' o undefined
    // y convierte en string el valor de la propiedad de cada objeto restante
    let curparams = Object.entries(filters).reduce(
      (a, [k, v]) => (v ? ((a[k] = v.toString()), a) : a),
      {}
    )

    curparams = Object.entries(curparams).reduce(
      (a, [k, v]) => (v ? ((a[k] = v.toString()), a) : a),
      {}
    )

    return await this.$axios
      .get('linabi/catalog/', {
        params: curparams,
      })
      .then((response) => {
        dispatch('addToCurCatalog', response.data)
        commit('SET_LOADING_STATUS')
      })
  },
  setBreadCrumbsItems({ commit }, payload) {
    commit('SET_BREAD_CRUMBS_ITEMS', payload)
  },
  setCurCatalog({ commit }, payload) {
    commit('SET_CUR_CATALOG', payload)
  },
  setPhotosList({ commit }, payload) {
    commit('SET_PHOTOS_LIST', payload)
  },
  iniPhotosList({ commit, state }) {
    const pl = Array.from(state.curCatalog, (item) => {
      return {
        sku: item.SKU,
        imgsrc: this.$config.fotosURL + item.SKU + this.$config.fotosExt,
        ordinal: 1,
      }
    })
    commit('SET_PHOTOS_LIST', pl)
  },
  addToPhotosList({ commit, state }, payload) {
    let pl = state.photosList
    pl = pl.filter((el1) => {
      return !payload.find((el2) => {
        return el2.SKU === el1.SKU
      })
    })

    pl = pl.concat(payload)

    commit('SET_PHOTOS_LIST', pl)
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
  getCurCatalog(state) {
    return state.curCatalog
  },
  getPhotosList(state) {
    return state.photosList
  },
  isLoading(state) {
    return state.isLoading
  },
}
