export const namespaced = true

function updateCartState(cartstate) {
  localStorage.setItem('lina_cart', JSON.stringify(cartstate))
}

const initCart = {
  cartCustomer: {},
  total: 0,
  items: [],
}

export const state = () => ({
  cart: initCart,
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
    if (!customer) {
      customer = {}
    }
    state.cart.cartCustomer = customer
    updateCartState(state.cart)
  },

  SET_CUSTOMERID(state, id) {
    state.cart.cartCustomer.id = id
  },
  SET_CUSTOMERNAME(state, name) {
    state.cart.cartCustomer.name = name
  },
  SET_CUSTOMEREMAIL(state, email) {
    state.cart.cartCustomer.email = email
  },
  SET_CUSTOMERTEL(state, tel) {
    state.cart.cartCustomer.tel = tel
  },
  SET_TOTAL(state, total) {
    state.cart.total = total
  },

  ADD_TO_CART(state, product) {
    state.cart.items.push(product)
    updateCartState(state.cart)
  },
  UPDATE_ITEM(state, item) {
    state.cart.items[item.index].quantity = item.quantity
    state.cart.items[item.index].price = item.price
    updateCartState(state.cart)
  },
  REMOVE_ITEM_ID(state, productId) {
    state.cart.items = state.cart.items.filter((item) => item.id !== productId)
    updateCartState(state.cart)
  },

  REMOVE_ITEM_INDEX(state, index) {
    state.cart.items.splice(index, 1)
    updateCartState(state.cart)
  },
  CLEAR_CART(state) {
    state.cart = {
      cartCustomer: {},
      total: 0,
      items: [],
    }
    localStorage.removeItem('lina_cart')
  },
  DECREASE_QUANTITY(state, index) {
    if (state.cart.items[index].quantity > 1) {
      state.cart.items[index].quantity--
    } else {
      state.cart.items.splice(index, 1)
    }
    updateCartState(state.cart)
  },
  INCREASE_QUANTITY(state, index) {
    state.cart.items[index].quantity++
    updateCartState(state.cart)
  },
}

export const actions = {
  nuxtClientInit({ commit }) {
    if (process.client) {
      const objcart = JSON.parse(localStorage.getItem('lina_cart')) || {
        cart: {},
      }

      commit('SET_CART', objcart.cart)
    }
  },

  setCartCustomer({ commit }, customer) {
    commit('SET_CART_CUSTOMER', customer)
  },
  addToCart({ state, commit }, item) {
    const itemIndex = state.cart.items.findIndex(
      (cartitem) => cartitem.id === item.id
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
  removeItemID({ commit }, productId) {
    commit('REMOVE_ITEM_ID', productId)
  },
  removeItemIndex({ commit }, index) {
    commit('REMOVE_ITEM_INDEX', index)
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
  getCartCustomer(state) {
    return state.cart.cartCustomer
  },

  getCartItems: (state) => state.cart.items || [],
  getCartItemCount: (state) => state.cart.items?.length || 0,
  getCartProductCount: (state) => {
    if ((state.cart.items?.length ?? 0) === 0) return 0
    return state.cart.items.reduce((total, item) => total + item.quantity, 0)
  },
  getCartTotalPrice: (state) =>
    state.cart.items?.reduce(
      (total, item) => total + item.price * item.quantity,
      0
    ) || 0,

  getCartItemQuantity: (state) => (index) =>
    state.cart.items[index]?.quantity || 0,
  getItemQuantityById: (state) => (id) => {
    const item = state.cart.items.find((item) => item.id === id)
    return item ? item.quantity : 0
  },
  getItemTotalById: (state) => (id) => {
    const item = state.cart.items.find((item) => item.id === id)
    return item ? item.price * item.quantity : 0
  },
  getCartTotalItems: (state) => state.cart.items.length || 0,
}
