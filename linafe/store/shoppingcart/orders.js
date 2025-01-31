export const namespaced = true

function updateOrderState(orderstate) {
  localStorage.setItem('lina_order', JSON.stringify(orderstate))
}

export const state = () => ({
  orders: [],
  currentIndex: 0,
  currentID: 0,
  isLoading: false,
})

export const mutations = {
  SET_ORDERS(state, orders) {
    state.orders = orders
    updateOrderState(orders)
  },
  ADD_ORDER(state, order) {
    const curlength = state.orders.push(order)

    state.currentIndex = curlength - 1
    state.currentID = order.id

    updateOrderState(state.orders)
  },
  SET_CURRENT_INDEX(state, index) {
    state.currentIndex = index
  },
  SET_CURRENT_ID(state, id) {
    state.currentID = id
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
  setCurrentID({ commit }, id) {
    commit('SET_CURRENT_ID', id)
  },
  setCurrentIndex({ commit }, index) {
    commit('SET_CURRENT_INDEX', index)
  },
  setIsLoading({ commit }) {
    commit('SET_ISLOADING')
  },

  async fetchOrders({ commit }) {
    commit('SET_ISLOADING')

    try {
      const response = await this.$axios.get('shoppingcart/extorder/')
      commit('SET_ORDERS', response.data)
      commit('SET_CURRENT_INDEX', 0)
      commit('SET_ISLOADING')
    } catch (error) {
      commit('SET_ISLOADING')
      // Lanzar la excepción para que pueda ser capturada en asyncData
      throw error
    }
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
      await dispatch('shoppingcart/cart/clearCart', null, { root: true })

      commit('SET_ISLOADING')
    } catch (error) {
      console.error('Error during checkout:', error)
    }
  },
}

export const getters = {
  getOrders: (state) => state.orders,
  getOrdersCount: (state) => state.orders.length || 0,
  getOrderByid: (state) => (id) =>
    state.orders.find((order) => order.id === id),
  getOrderByIndex: (state) => (index) => state.orders[index],
  getOrdersByCustomer: (state) => (customerId) =>
    state.orders.filter((order) => order.customer_id === customerId),
  getOrderTotalByID: (state) => (id) => {
    const order = state.orders.find((order) => order.id === id)
    return order
      ? order.items.reduce((acc, item) => acc + item.price * item.quantity, 0)
      : 0
  },
  getOrderTotalByIndex: (state) => (index) => {
    const order = state.orders[index]
    return order ? order.total : 0
  },
  getCurrentOrderTotal: (state) => {
    const order = state.orders[state.currentIndex]
    return order ? order.total : 0
  },

  getCurrentOrder: (state) => state.orders[state.currentIndex],
  getCurrentIndex: (state) => state.currentIndex,
  getCurrentID: (state) => state.currentID,
  getLoadingStatus: (state) => state.isLoading,
}
