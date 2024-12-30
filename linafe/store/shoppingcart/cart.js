export const namespaced = true

export const state = () => ({
  cart: [],
  products: [],
  cartCustomer: { id: 1, name: 'John Doe', email: 'jdoe@numen.pa' },
})

export const mutations = {
  SET_PRODUCTS(state, products) {
    state.products = products
  },
  SET_CART_CUSTOMER(state, customer) {
    state.cartCustomer = customer
  },
  ADD_TO_CART(state, product) {
    state.cart.push(product)
  },
  UPDATE_CART(state, item) {
    state.cart[item.index].quantity = item.qty
    state.cart[item.index].price = item.price
  },
  REMOVE_FROM_CART(state, productId) {
    state.cart = state.cart.filter((item) => item.product.id !== productId)
  },
  CLEAR_CART(state) {
    state.cart = []
  },
  DECREASE_QUANTITY(state, index) {
    if (state.cart[index].quantity > 1) {
      state.cart[index].quantity--
    } else {
      state.cart.splice(index, 1)
    }
  },
  INCREASE_QUANTITY(state, index) {
    state.cart[index].quantity++
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
  setProducts({ commit }, products) {
    commit('SET_PRODUCTS', products)
  },
  setCartCustomer({ commit }, customer) {
    commit('SET_CART_CUSTOMER', customer)
  },
  addToCart({ state, commit }, item) {
    const itemIndex = state.cart.findIndex(
      (cartitem) => cartitem.product.id === item.product.id
    )

    if (itemIndex > -1) {
      commit('UPDATE_CART', {
        index: itemIndex,
        qty: item.quantity,
        price: item.price,
      })

      return
    }

    commit('ADD_TO_CART', item)
  },
  // addToCart({ commit }, product) {
  //   commit('ADD_TO_CART', product)
  // },
  removeFromCart({ commit }, productId) {
    commit('REMOVE_FROM_CART', productId)
  },
  clearCart({ commit }) {
    commit('CLEAR_CART')
  },
  decreaseQuantity({ commit }, index) {
    commit('DECREASE_QUANTITY', index)
  },
  increaseQuantity({ commit }, index) {
    commit('INCREASE_QUANTITY', index)
  },
}

export const getters = {
  getAllProducts: (state) => state.products,
  getProductById: (state) => (id) =>
    state.products.find((product) => product.id === id),
  getCartCustomer: (state) => state.cartCustomer,
  getCartItems: (state) => state.cart,
  getCartItemCount: (state) => state.cart.length,
  getCartProductCount: (state) => {
    if (state.cart.length === 0) return 0
    return state.cart.reduce((total, item) => total + item.quantity, 0)
  },
  getCartTotalPrice: (state) =>
    state.cart.reduce((total, item) => total + item.price * item.quantity, 0),
  getCartItemQuantity: (state) => (index) => state.cart[index].quantity,
}
