export const namespaced = true

export const state = () => ({
  cart: [],
  products: [],
  search_product: '',
})

export const mutations = {
  SET_PRODUCTS(state, products) {
    state.products = products
  },
  SET_SEARCH_PRODUCT(state, search) {
    state.search_product = search
  },
  ADD_TO_CART(state, product) {
    state.cart.push(product)
  },
  REMOVE_FROM_CART(state, productId) {
    state.cart = state.cart.filter((product) => product.id !== productId)
  },
  CLEAR_CART(state) {
    state.cart = []
  },
}

export const actions = {
  fetchProducts({ commit }) {
    // Simulate an API call
    const products = [
      { id: 1, name: 'Electronics', price: 100, quantity: 1 },
      { id: 2, name: 'Books', price: 50, quantity: 1 },
      { id: 3, name: 'Clothing', price: 25, quantity: 1 },
    ]
    commit('SET_PRODUCTS', products)
  },
  setSearchProduct({ commit }, search) {
    commit('SET_SEARCH_PRODUCT', search)
  },
  setProducts({ commit }, products) {
    commit('SET_PRODUCTS', products)
  },
  addToCart({ commit }, product) {
    commit('ADD_TO_CART', product)
  },
  removeFromCart({ commit }, productId) {
    commit('REMOVE_FROM_CART', productId)
  },
  clearCart({ commit }) {
    commit('CLEAR_CART')
  },
}

export const getters = {
  filteredProducts: (state) => {
    return state.products.filter((product) =>
      product.name.toLowerCase().includes(state.search_product.toLowerCase())
    )
  },
  getAllProducts: (state) => state.products,
  getSearchedProduct: (state) => state.search_product,
  getCartItems: (state) => state.cart,
  getCartItemCount: (state) => state.cart.length,
  getCartTotalPrice: (state) =>
    state.cart.reduce((total, item) => total + item.price * item.quantity, 0),
}
