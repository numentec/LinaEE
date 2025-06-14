export const namespaced = true

export const state = () => ({
  customer: {},
  customCatalog: {},
  customCatalogs: [],
  customCatalogsLoaded: false,
  customCatalogsLoading: false,
})

export const mutations = {
  SET_CUSTOM_CATALOG(state, catalog) {
    state.customCatalog = catalog
  },

  SET_CUSTOM_CATALOGS(state, catalogs) {
    state.customCatalogs = catalogs
    state.customCatalogsLoaded = true
    state.customCatalogsLoading = false
  },

  SET_CUSTOM_CATALOGS_LOADING(state, loading) {
    state.customCatalogsLoading = loading
  },

  ADD_CUSTOM_CATALOG(state, catalog) {
    state.customCatalogs.push(catalog)
  },

  UPDATE_CUSTOM_CATALOG(state, updatedCatalog) {
    const index = state.customCatalogs.findIndex(
      (c) => c.id === updatedCatalog.id
    )
    if (index !== -1) {
      state.customCatalogs.splice(index, 1, updatedCatalog)
    }
  },

  REMOVE_CUSTOM_CATALOG(state, catalogId) {
    state.customCatalogs = state.customCatalogs.filter(
      (c) => c.id !== catalogId
    )
  },

  SET_CUSTOMER(state, customer) {
    state.customer = customer
  },
}

export const actions = {
  setCustomCatalog({ commit }, catalog) {
    commit('SET_CUSTOM_CATALOG', catalog)
  },

  setCustomCatalogs({ commit }, catalogs) {
    commit('SET_CUSTOM_CATALOGS', catalogs)
  },

  setCustomCatalogsLoading({ commit }, loading) {
    commit('SET_CUSTOM_CATALOGS_LOADING', loading)
  },

  addCustomCatalog({ commit }, catalog) {
    commit('ADD_CUSTOM_CATALOG', catalog)
  },

  updateCustomCatalog({ commit }, updatedCatalog) {
    commit('UPDATE_CUSTOM_CATALOG', updatedCatalog)
  },

  removeCustomCatalog({ commit }, catalogId) {
    commit('REMOVE_CUSTOM_CATALOG', catalogId)
  },

  setCustomer({ commit }, customer) {
    commit('SET_CUSTOMER', customer)
  },
}

export const getters = {
  getCustomCatalog: (state) => state.customCatalog,
  getCustomCatalogs: (state) => state.customCatalogs,
  getCustomCatalogsLoaded: (state) => state.customCatalogsLoaded,
  getCustomCatalogsLoading: (state) => state.customCatalogsLoading,
  getCustomCatalogCount: (state) => state.customCatalogs.length,
  getCustomer: (state) => state.customer,
  getCustomerId: (state) => state.customer.id || null,
  getCustomCatalogToken: (state) => {
    return state.customCatalog.token || null
  },
}
