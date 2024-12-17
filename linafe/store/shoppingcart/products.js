// import CustomStore from 'devextreme/data/custom_store'
export const namespaced = true

export const state = () => ({
  products: [],
  cart: [],
  search_product: '',
})

export const mutations = {
  SET_PRODUCTS(state, products) {
    state.products = products
  },
  ADD_TO_CART(state, product) {
    state.cart.push(product)
  },
  REMOVE_FROM_CART(state, productId) {
    state.cart = state.cart.filter((product) => product.id !== productId)
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
  addToCart({ commit }, product) {
    commit('ADD_TO_CART', product)
  },
  removeFromCart({ commit }, productId) {
    commit('REMOVE_FROM_CART', productId)
  },
  setSearchProduct({ commit }, product) {
    commit('SET_SEARCH_PRODUCT', product)
  },
}

export const getters = {
  cartItems: (state) => {
    return state.cart
  },
  getAllProducts: (state) => state.products,
  productById: (state) => (id) =>
    state.products.find((product) => product.id === id),
  getSearchProduct: (state) => state.search_product,
}
