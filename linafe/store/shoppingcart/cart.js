export const namespaced = true

function updateCartState(cartstate) {
  // console.log('***** updateCartState *****', cartstate)
  localStorage.setItem('lina_cart', JSON.stringify(cartstate))
}

export const state = () => ({
  cart: [],
  cartCustomer: {
    id: 0,
    name: 'nocli',
    email: 'noemail@numen.pa',
  },
})

/* El estado de cart se inicializa con los datos almacenados en localStorage.
  Se le da seguimiento con el plugin cartState.js
*/
export const mutations = {
  SET_CART(state, cart) {
    state.cart = cart
    updateCartState(cart)
  },

  SET_CART_CUSTOMER(state, customer) {
    state.cartCustomer = customer
    localStorage.setItem('lina_cartCustomer', JSON.stringify(customer))
  },
  ADD_TO_CART(state, product) {
    state.cart.push(product)
    updateCartState(state.cart)
  },
  UPDATE_ITEM(state, item) {
    state.cart[item.index].quantity = item.quantity
    state.cart[item.index].price = item.price
    updateCartState(state.cart)
  },
  REMOVE_FROM_CART(state, productId) {
    state.cart = state.cart.filter((item) => item.product.id !== productId)
    updateCartState(state.cart)
  },
  REMOVE_ITEM(state, index) {
    state.cart.splice(index, 1)
    updateCartState(state.cart)
  },
  CLEAR_CART(state) {
    state.cart = []
    localStorage.removeItem('lina_cart')
  },
  DECREASE_QUANTITY(state, index) {
    if (state.cart[index].quantity > 1) {
      state.cart[index].quantity--
    } else {
      state.cart.splice(index, 1)
    }
    updateCartState(state.cart)
  },
  INCREASE_QUANTITY(state, index) {
    state.cart[index].quantity++
    updateCartState(state.cart)
  },
}

export const actions = {
  nuxtClientInit({ commit }) {
    if (process.client) {
      const objcart = JSON.parse(localStorage.getItem('lina_cart')) || {
        cart: [],
        cartCustomer: { id: 0, name: 'nocli', email: 'noemail@numen.pa' },
      }

      commit('SET_CART', objcart.cart)
      commit('SET_CART_CUSTOMER', objcart.cartCustomer)

      // const cartCustomer = JSON.parse(
      //   localStorage.getItem('lina_cartCustomer')
      // ) || {
      //   id: 0,
      //   name: 'nocli',
      //   email: 'noemail@numen.pa',
      // }
      // commit('SET_CART_CUSTOMER', cartCustomer)
    }
  },

  setCartCustomer({ commit }, customer) {
    commit('SET_CART_CUSTOMER', customer)
  },
  addToCart({ state, commit }, item) {
    const itemIndex = state.cart.findIndex(
      (cartitem) => cartitem.product.id === item.product.id
    )

    if (itemIndex > -1) {
      commit('UPDATE_ITEM', {
        index: itemIndex,
        quantity: item.quantity,
        price: item.price,
      })

      return
    }

    commit('ADD_TO_CART', item)
  },
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
  getItemQuantityById: (state) => (id) => {
    const item = state.cart.find((item) => item.product.id === id)
    return item ? item.quantity : 0
  },
}
