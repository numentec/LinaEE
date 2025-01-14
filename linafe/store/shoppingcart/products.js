export const namespaced = true

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
  isLoading: false,
})

export const mutations = {
  SET_PRODUCTS(state, products) {
    state.products = products
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
  SET_LOADING_STATUS(state) {
    state.isLoading = !state.isLoading
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

  async fetchProducts({ commit, rootGetters }) {
    commit('SET_LOADING_STATUS')

    const selectedBrands =
      rootGetters['shoppingcart/categories/getSelectedBrands']
    const selectProductsBy =
      rootGetters['shoppingcart/categories/getSelectProductsBy']

    const brands = selectedBrands.length > 0 ? selectedBrands.join(',') : ''

    const endpointParams = {
      ...selectProductsBy,
      brands, // '1,2,3,4,5,187,188,189,190,191',
      cia: '01',
    }

    return await this.$axios
      .get('shoppingcart/products/', {
        params: endpointParams,
      })
      .then((response) => {
        commit('SET_PRODUCTS', response.data)
        commit('SET_LOADING_STATUS')
      })
  },

  // Función temporal para generar datos de prueba para los productos
  async fetchData({ commit, dispatch }, payload) {
    // commit('SET_LOADING_STATUS')

    // Simulate an API call
    const { data } = await makeItems(payload.name)
    commit('SET_PRODUCTS', data)
  },

  setSearchProduct({ commit }, search) {
    commit('SET_SEARCH_PRODUCT', search)
  },

  addImage({ commit }, { id, url }) {
    commit('ADD_IMAGE', { id, url })
  },

  setIsLoading({ commit }) {
    commit('SET_LOADING_STATUS')
  },
}

export const getters = {
  getAllProducts: (state) => state.products,
  getProductById: (state) => (id) => state.products.find((p) => p.id === id),
  getSearchProduct: (state) => state.search_product,
  getImages: (state) => state.images,
  getImage: (state) => (id) => state.images[id],
}
