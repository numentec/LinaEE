// import CustomStore from 'devextreme/data/custom_store'
export const namespaced = true

export const state = () => ({
  products: [],
  search_product: '',
})

export const mutations = {
  SET_PRODUCTS(state, products) {
    state.products = products
  },
  ADD_PRODUCT(state, product) {
    state.products.push(product)
  },
  REMOVE_PRODUCT(state, productId) {
    state.products = state.products.filter(
      (product) => product.id !== productId
    )
  },
  SET_SEARCH_PRODUCT(state, product) {
    state.search_product = product
  },
}

export const actions = {
  fetchProducts({ commit }) {
    // Simulate an API call
    const products = [
      { id: 1, name: 'Electronics' },
      { id: 2, name: 'Books' },
      { id: 3, name: 'Clothing' },
    ]
    commit('SET_PRODUCTS', products)
  },
  addProduct({ commit }, product) {
    commit('ADD_PRODUCT', product)
  },
  removeProduct({ commit }, productId) {
    commit('REMOVE_CATEGORY', productId)
  },
  setSearchProduct({ commit }, product) {
    commit('SET_SEARCH_PRODUCT', product)
  },
}

export const getters = {
  getAllProducts: (state) => state.products,
  productById: (state) => (id) =>
    state.products.find((product) => product.id === id),
  getSearchProduct: (state) => state.search_product,
}
