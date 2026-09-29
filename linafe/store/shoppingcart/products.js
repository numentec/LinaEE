export const namespaced = true

const BRANDSDATA = ['1', '2', '3', '4', '5', '187', '188', '189', '190', '191']
const IMAGES = [
  '/shoppingcart/H23100256A.jpg',
  '/shoppingcart/H23100133A.jpg',
  '/shoppingcart/H22200482A.jpg',
  '/shoppingcart/W231013199.jpg',
  '/shoppingcart/W231013210.jpg',
  '/shoppingcart/HBS01401N-B.jpg',
  '/shoppingcart/VLCSMLORG.jpg',
]
const STOCK_FILTER_FIELDS = ['instock', 'intransit', 'infuture']

function emptyStockFilters() {
  return STOCK_FILTER_FIELDS.reduce((filters, field) => {
    filters[field] = { operator: '', value: '', valueTo: '' }
    return filters
  }, {})
}

function normalizeStockFilters(filters) {
  const normalized = emptyStockFilters()

  STOCK_FILTER_FIELDS.forEach((field) => {
    const criterion = (filters && filters[field]) || {}
    normalized[field] = {
      operator: criterion.operator || '',
      value:
        criterion.value === undefined || criterion.value === null
          ? ''
          : criterion.value,
      valueTo:
        criterion.valueTo === undefined || criterion.valueTo === null
          ? ''
          : criterion.valueTo,
    }
  })

  return normalized
}

function stockFilterParams(filters) {
  const params = {}

  STOCK_FILTER_FIELDS.forEach((field) => {
    const criterion = filters[field]
    if (!criterion.operator) return

    params[`${field}_operator`] = criterion.operator
    params[`${field}_value`] = criterion.value
    if (criterion.operator === 'between') {
      params[`${field}_value_to`] = criterion.valueTo
    }
  })

  return params
}

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
    })
  }

  return new Promise((resolve) => {
    resolve({ data: items })
  })
}

function updateImagesState(imgstate) {
  localStorage.setItem('lina_cartImages', JSON.stringify(imgstate))
}

export const state = () => ({
  products: [],
  images: {}, // Almacenar las URLs de las imágenes de los productos
  search_product: '',
  countFilteredProducts: 0,
  isLoading: false,
  itemImages: [],
  countProds: 0,
  // Estados para paginación e infinite scrolling
  currentPage: 1,
  pageSize: 20,
  hasNextPage: false,
  totalPages: 0,
  isLoadingMore: false,
  allDataLoaded: false,
  stockFilters: emptyStockFilters(),
  productRequestId: 0,
})

export const mutations = {
  SET_PRODUCTS(state, products) {
    state.products = products
  },
  BEGIN_PRODUCTS_REQUEST(state, filters) {
    state.productRequestId += 1
    state.stockFilters = normalizeStockFilters(filters)
    state.products = []
    state.currentPage = 1
    state.hasNextPage = false
    state.totalPages = 0
    state.allDataLoaded = false
    state.isLoading = true
    state.isLoadingMore = false
  },
  ADD_PRODUCTS(state, products) {
    // Para infinite scrolling - agregar productos a la lista existente
    state.products = [...state.products, ...products]
  },
  RESET_PRODUCTS(state) {
    state.products = []
    state.currentPage = 1
    state.allDataLoaded = false
  },
  SET_IMAGES(state, images) {
    state.images = images
    updateImagesState(state.images)
  },
  ADD_IMAGE(state, { id, url }) {
    state.images = { ...state.images, [id]: url }
    updateImagesState(state.images)
  },
  SET_SEARCH_PRODUCT(state, search) {
    state.search_product = search
    localStorage.setItem('lina_searchProduct', JSON.stringify(search))
  },
  SET_COUNT_FILTERED_PRODUCTS(state, count) {
    state.countFilteredProducts = count
  },
  SET_LOADING_STATUS(state) {
    state.isLoading = !state.isLoading
  },
  SET_IS_LOADING(state, status) {
    state.isLoading = status
  },
  SET_ITEM_IMAGES(state, itemImages) {
    state.itemImages = itemImages
  },
  SET_COUNT_PRODS(state, countProds) {
    state.countProds = countProds
  },
  SET_PAGINATION_DATA(state, paginationData) {
    state.currentPage = paginationData.current_page
    state.hasNextPage = !!paginationData.next
    state.totalPages = paginationData.total_pages
    state.allDataLoaded = !paginationData.has_next
  },
  SET_LOADING_MORE(state, status) {
    state.isLoadingMore = status
  },
  INCREMENT_PAGE(state) {
    state.currentPage += 1
  },
  SET_PAGE_SIZE(state, size) {
    state.pageSize = size
  },
}

export const actions = {
  nuxtClientInit({ commit }) {
    if (process.client) {
      const images = JSON.parse(localStorage.getItem('lina_cartImages')) || {}
      commit('SET_IMAGES', images)

      const searchProduct =
        JSON.parse(localStorage.getItem('lina_searchProduct')) || ''
      commit('SET_SEARCH_PRODUCT', searchProduct)
    }
  },

  async fetchProducts(
    { commit, rootGetters, state },
    { page = 1, resetData = true, filters } = {}
  ) {
    if (resetData) {
      commit(
        'BEGIN_PRODUCTS_REQUEST',
        filters === undefined ? state.stockFilters : filters
      )
    } else {
      commit('SET_LOADING_MORE', true)
    }
    const requestId = state.productRequestId

    const selectedBrands =
      rootGetters['shoppingcart/categories/getSelectedBrands']
    const selectProductsBy =
      rootGetters['shoppingcart/categories/getSelectProductsBy']

    const brands = selectedBrands.length > 0 ? selectedBrands.join(',') : ''

    const endpointParams = {
      ...selectProductsBy,
      brands,
      cia: '01',
      page,
      page_size: state.pageSize,
      ...stockFilterParams(state.stockFilters),
    }

    try {
      const response = await this.$axios.get('shoppingcart/products/', {
        params: endpointParams,
      })

      const { results, count, page_info: pageInfo } = response.data
      if (requestId !== state.productRequestId) return response.data

      if (resetData) {
        commit('SET_PRODUCTS', results)
      } else {
        commit('ADD_PRODUCTS', results)
      }

      commit('SET_COUNT_PRODS', count)
      commit('SET_PAGINATION_DATA', {
        current_page: pageInfo.current_page,
        total_pages: pageInfo.total_pages,
        next: response.data.next,
        has_next: pageInfo.has_next,
      })

      if (resetData) {
        commit('SET_IS_LOADING', false)
      } else {
        commit('SET_LOADING_MORE', false)
      }

      return response.data
    } catch (error) {
      if (requestId === state.productRequestId) {
        if (resetData) {
          commit('SET_IS_LOADING', false)
        } else {
          commit('SET_LOADING_MORE', false)
        }
      }
      throw error
    }
  },

  async loadMoreProducts({ commit, dispatch, state, rootGetters }) {
    // Evitar múltiples cargas simultáneas
    if (state.isLoading || state.isLoadingMore || state.allDataLoaded) {
      return
    }

    const nextPage = state.currentPage + 1

    return await dispatch('fetchProducts', {
      page: nextPage,
      resetData: false,
    })
  },

  // Función temporal para generar datos de prueba para los productos
  async fetchData({ commit, dispatch }, payload) {
    // commit('SET_LOADING_STATUS')

    // Simulate an API call
    const { data } = await makeItems(payload.name)
    commit('SET_PRODUCTS', data)
  },

  // One product images
  async fetchItemImages({ commit }, src) {
    if (src.imgID === 'no_image') {
      commit('SET_ITEM_IMAGES', [src.imgSrc])
      return
    }

    await this.$axios
      .get(`shoppingcart/itemimages/${src.imgID}`)
      .then((response) => {
        const itemImages = response.data || []

        itemImages.push(src.imgSrc)

        commit('SET_ITEM_IMAGES', itemImages)
      })
      .catch(() => {
        commit('SET_ITEM_IMAGES', [src.imgSrc])
      })
  },

  setProducts({ commit }, products) {
    commit('SET_PRODUCTS', products)
  },

  setSearchProduct({ commit }, search) {
    commit('SET_SEARCH_PRODUCT', search)
  },

  setCountFilteredProducts({ commit }, count) {
    commit('SET_COUNT_FILTERED_PRODUCTS', count)
  },

  addImage({ commit }, { id, url }) {
    commit('ADD_IMAGE', { id, url })
  },

  setIsLoading({ commit }) {
    commit('SET_LOADING_STATUS')
  },

  setitemImages({ commit }, itemImages) {
    commit('SET_ITEM_IMAGES', itemImages)
  },

  setcountProds({ commit }, countProds) {
    commit('SET_COUNT_PRODS', countProds)
  },

  setPageSize({ commit }, size) {
    commit('SET_PAGE_SIZE', size)
  },
}

export const getters = {
  getAllProducts: (state) => state.products,
  getProductById: (state) => (id) => state.products.find((p) => p.id === id),
  getSearchProduct: (state) => state.search_product,
  getCountFilteredProducts: (state) => state.countFilteredProducts,
  getImages: (state) => state.images,
  getImage: (state) => (id) => state.images[id],
  getIsLoading: (state) => state.isLoading,
  getItemImages: (state) => state.itemImages,
  getCountProds: (state) => state.countProds,
  // Nuevos getters para paginación
  getCurrentPage: (state) => state.currentPage,
  getHasNextPage: (state) => state.hasNextPage,
  getTotalPages: (state) => state.totalPages,
  getIsLoadingMore: (state) => state.isLoadingMore,
  getAllDataLoaded: (state) => state.allDataLoaded,
  getPageSize: (state) => state.pageSize,
  getStockFilters: (state) => state.stockFilters,
}
