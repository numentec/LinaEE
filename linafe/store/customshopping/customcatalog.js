export const namespaced = true

// Mock data for custom catalog items
// This data is used to simulate a custom catalog in the store
const BRANDSDATA = ['1', '2', '3', '4', '5', '187', '188', '189', '190', '191']
const IMAGES = [
  'http://192.168.1.55:8001/media/images/bifavoritos/prev3.gif',
  '/shoppingcart/H23100256A.jpg',
  '/shoppingcart/H23100133A.jpg',
  '/shoppingcart/H22200482A.jpg',
  '/shoppingcart/W231013199.jpg',
  '/shoppingcart/W231013210.jpg',
  '/shoppingcart/HBS01401N-B.jpg',
  '/shoppingcart/VLCSMLORG.jpg',
]

function getRandomBrand() {
  const randomIndex = Math.floor(Math.random() * BRANDSDATA.length)
  return BRANDSDATA[randomIndex]
}

function makeItems(name) {
  const items = []
  for (let i = 0; i < 100; i++) {
    items.push({
      id: `SKU${i}`,
      image: IMAGES[Math.floor(Math.random() * IMAGES.length)],
      name: `${name} ${i}`,
      price: Math.floor(Math.random() * 1000),
      description: `Description for ${name} ${i}`,
      instock: Math.floor(Math.random() * 100),
      brand: getRandomBrand(),
      token: `token-${i}`,
    })
  }

  return new Promise((resolve) => {
    resolve({ data: items })
  })
}
// End of mock data

export const state = () => ({
  customer: {},
  customCatalog: {},
  customCatalogs: [],
  customCatalogsLoaded: false,
  customCatalogsLoading: false,

  searchCustomCatalog: '',
  countFilteredCustomCatalog: 0,
  breadcrumbs: [],
  isListView: false,
  isLoading: false,

  brands: [],
  selected_brands: [],
})

export const mutations = {
  SET_LOADING_STATUS(state) {
    state.isLoading = !state.isLoading
  },
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

  SET_SEARCH_CUSTOM_CATALOG(state, search) {
    state.searchCustomCatalog = search
    localStorage.setItem('lina_searchCustomCatalog', JSON.stringify(search))
  },

  SET_COUNT_FILTERED_CUSTOM_CATALOG(state, count) {
    state.countFilteredCustomCatalog = count
    localStorage.setItem(
      'lina_countFilteredCustomCatalog',
      JSON.stringify(count)
    )
  },
  SET_SELECTED_BRANDS(state, brands) {
    state.selected_brands = brands
    localStorage.setItem('lina_cusSelectedBrands', JSON.stringify(brands))
  },
  SET_BREADCRUMBS(state, breadcrumbs) {
    state.breadcrumbs = breadcrumbs
    localStorage.setItem(
      'lina_cusbreadcrumbs',
      JSON.stringify(state.breadcrumbs)
    ) // Save to local storage
  },
  SET_IS_LIST_VIEW(state, isListView) {
    state.isListView = isListView
    localStorage.setItem('lina_isListView', JSON.stringify(isListView))
  },
}

export const actions = {
  nuxtClientInit({ commit }) {
    if (process.client) {
      const selectedBrands =
        JSON.parse(localStorage.getItem('lina_selectedBrands')) || []
      commit('SET_SELECTED_BRANDS', selectedBrands)

      const searchDepartment =
        JSON.parse(localStorage.getItem('lina_searchCustomCatalog')) || ''
      commit('SET_SEARCH_CUSTOM_CATALOG', searchDepartment)

      const breadcrumbs =
        JSON.parse(localStorage.getItem('lina_cusbreadcrumbs')) || []
      commit('SET_BREADCRUMBS', breadcrumbs)

      const isListView =
        JSON.parse(localStorage.getItem('lina_isListView')) || false
      commit('SET_LIST_VIEW', isListView)

      const countFilteredCustomCatalog =
        JSON.parse(localStorage.getItem('lina_countFilteredCustomCatalog')) || 0
      commit('SET_COUNT_FILTERED_CUSTOM_CATALOG', countFilteredCustomCatalog)
    }
  },

  setIsLoading({ commit }) {
    commit('SET_LOADING_STATUS')
  },

  async fetchItems({ commit, dispatch }, payload) {
    commit('SET_LOADING_STATUS')

    let mutC = ''

    try {
      // Construir endpoint dependiendo de si existe token
      const { endpoint, mutCatalog } = payload.token
        ? {
            endpoint: `catalog/by-customer/${payload.ulid}/${payload.token}`,
            mutCatalog: 'SET_CUSTOM_CATALOG',
          }
        : {
            endpoint: `catalog/by-customer/${payload.ulid}`,
            mutCatalog: 'SET_CUSTOM_CATALOGS',
          }

      mutC = mutCatalog

      const response = await this.$axios.get(endpoint)

      // La estructura de respuesta incluye customer y catalogs
      if (mutCatalog === 'SET_CUSTOM_CATALOGS') {
        commit('SET_CUSTOMER', response.data.customer)
      }

      // Los catálogos están en response.data.catalogs
      const catalogs = response.data.catalogs || response.data || []
      commit(mutCatalog, catalogs)

      // Ejecutar acción de otro módulo Vuex
      if (catalogs.items) {
        await dispatch('shoppingcart/products/setProducts', catalogs.items, {
          root: true,
        })
      }
      commit('SET_LOADING_STATUS')

      // return {
      //   items: catalogs,
      //   customer: response.data.customer,
      //   total_catalogs: response.data.total_catalogs || catalogs.length,
      // }
    } catch (error) {
      commit(mutC, [])
      // eslint-disable-next-line no-console
      console.error('Error fetching items:', error)
      throw error
    }
  },

  // Función temporal para generar datos de prueba para los productos
  async fetchData({ commit, dispatch }, payload) {
    // commit('SET_LOADING_STATUS')

    // Simulate an API call
    const { data } = await makeItems(payload.name)
    commit('SET_LOADING_STATUS')

    commit('SET_CUSTOM_CATALOGS', data)
    commit('SET_LOADING_STATUS')
    return { items: data }
  },

  setCustomCatalog({ commit }, catalog) {
    commit('SET_CUSTOM_CATALOG', catalog)
  },

  setCustomCatalogs({ commit }, catalogs) {
    commit('SET_CUSTOM_CATALOGS', catalogs)
  },

  setCustomCatalogsLoading({ commit }, loading) {
    commit('SET_CUSTOM_CATALOGS_LOADING', loading)
  },

  setCountFilteredCC({ commit }, count) {
    commit('SET_COUNT_FILTERED_CUSTOM_CATALOG', count)
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

  setSelectedBrands({ commit }, brands) {
    commit('SET_SELECTED_BRANDS', brands)
  },
}

export const getters = {
  getCustomCatalog: (state) => state.customCatalog,
  getAllCustomCatalogs: (state) => state.customCatalogs,
  getTotalCatalogs: (state) => state.customCatalogs.length,
  getCustomCatalogById: (state) => (id) =>
    state.customCatalogs.find((cc) => cc.id === id),
  getCustomCatalogsLoaded: (state) => state.customCatalogsLoaded,
  getCustomCatalogsLoading: (state) => state.customCatalogsLoading,
  getCustomCatalogCount: (state) => state.customCatalogs.length,
  getCustomer: (state) => state.customer,
  getCustomerId: (state) => state.customer.id || null,
  getCustomerULID: (state) => state.customer.ulid || '',
  getCustomCatalogToken: (state) => {
    return state.customCatalog.token || null
  },
  getSearchCustomCatalog: (state) => state.searchCustomCatalog,
  getCountFilteredCustomCatalog: (state) => state.countFilteredCustomCatalog,
  getBreadcrumbs: (state) => state.breadcrumbs,
  isListView: (state) => state.isListView,
  getIsLoading: (state) => state.isLoading,

  getBrands: (state) => state.brands,
  getSelectedBrands: (state) => state.selected_brands,
}
