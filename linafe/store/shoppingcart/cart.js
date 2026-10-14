export const namespaced = true

function updateCartState(cartstate) {
  localStorage.setItem('lina_cart', JSON.stringify(cartstate))
}

// orderId: id de la orden que originó el carrito (Keep selling).
// Si existe, el checkout actualiza esa orden en vez de crear una nueva.
const initCart = () => ({
  cartCustomer: {},
  total: 0,
  items: [],
  orderId: null,
})

// Convierte un item de orden (backend) al formato de item del carrito
function orderItemToCartItem(item) {
  return {
    id: item.sku,
    name: item.name,
    description: '',
    quantity: Number(item.quantity),
    price: Number(item.price),
    image: item.image,
  }
}

export const state = () => ({
  cart: initCart(),
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
  SET_ORDER_ID(state, id) {
    state.cart = { ...state.cart, orderId: id }
    updateCartState(state.cart)
  },
  CLEAR_CART(state) {
    state.cart = initCart()
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

  // Keep selling: carga una orden en el carrito, ligándolo a ella.
  // Si el carrito actual no está ligado a una orden, sus items se suman a los
  // de la orden (mismo SKU: se suman cantidades y se conserva el precio de la orden).
  // El cliente de la orden siempre prevalece.
  // Devuelve { merged, customerReplaced } para informar al usuario.
  loadFromOrder({ state, commit }, order) {
    const items = (order.items || []).map(orderItemToCartItem)
    const prevCart = state.cart || initCart()
    let merged = 0

    if (!prevCart.orderId) {
      for (const cartItem of prevCart.items || []) {
        const orderItem = items.find((item) => item.id === cartItem.id)
        if (orderItem) {
          orderItem.quantity += Number(cartItem.quantity)
        } else {
          items.push({ ...cartItem })
        }
        merged++
      }
    }

    const prevCustomerId = prevCart.cartCustomer?.id
    const customerReplaced =
      !prevCart.orderId &&
      !!prevCustomerId &&
      String(prevCustomerId) !== String(order.customer_id)

    commit('SET_CART', {
      cartCustomer: {
        id: order.customer_id,
        name: order.customer_name,
        email: order.customer_email,
        tel: order.customer_cel,
      },
      total: 0,
      items,
      orderId: order.id,
    })

    return { merged, customerReplaced }
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

  getCartOrderId: (state) => state.cart.orderId || null,
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
