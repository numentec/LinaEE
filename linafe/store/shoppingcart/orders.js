export const namespaced = true

function updateOrderState(orderstate) {
  localStorage.setItem('lina_order', JSON.stringify(orderstate))
}

export const state = () => ({
  orders: [],
  isLoading: false,
})

export const mutations = {
  SET_ORDERS(state, orders) {
    state.orders = orders
    updateOrderState(orders)
  },
  ADD_ORDER(state, order) {
    state.orders.push(order)
  },
  SET_ISLOADING(state) {
    state.isLoading = !state.isLoading
  },
}

export const actions = {
  nuxtClientInit({ commit }) {
    if (process.client) {
      const obj = JSON.parse(localStorage.getItem('lina_orders')) || {
        orders: [],
      }

      commit('SET_ORDERS', obj.orders)
    }
  },
  setOrders({ commit }, orders) {
    commit('SET_ORDERS', orders)
  },
  addOrder({ commit }, order) {
    commit('ADD_ORDER', order)
  },
  setIsLoading({ commit }) {
    commit('SET_ISLOADING')
  },

  async createOrder({ commit, dispatch, rootState }) {
    commit('SET_ISLOADING')

    const cart = rootState.shoppingcart.cart.cart

    const newOrder = {
      customer_id: cart.customerID,
      customer_name: cart.customerName,
      customer_email: cart.customerEmail,
      customr_cel: cart.customerTel,
      total: cart.items
        .reduce((acc, item) => acc + parseFloat(item.price * item.quantity), 0)
        .toFixed(2),
      items: cart.items.map((item) => ({
        sku: item.id,
        name: item.name,
        price: item.price,
        quantity: item.quantity,
      })),
    }

    try {
      const response = await this.$axios.post(
        'shoppingcart/extorder/',
        newOrder
      )

      commit('ADD_ORDER', response.data)
      // commit('CLEAR_CART')
      await dispatch('shoppingcart/cart/clearCart', null, { root: true })

      commit('SET_ISLOADING')

      return response.data.id
    } catch (error) {
      console.error('Error during checkout:', error)
    }
  },
}

export const getters = {
  getOrders: (state) => state.orders,
  getOrderByid: (state) => (id) =>
    state.orders.find((order) => order.id === id),
  getOrderByIndex: (state) => (index) => state.orders[index],
  getOrdersByCustomer: (state) => (customerId) =>
    state.orders.filter((order) => order.customer_id === customerId),
  getOrderTotal: (state) => (id) => {
    const order = state.orders.find((order) => order.id === id)
    return order
      ? order.items.reduce((acc, item) => acc + item.price * item.quantity, 0)
      : 0
  },
  getLoadingStatus: (state) => state.isLoading,
}
