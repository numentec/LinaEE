export const namespaced = true

function updateOrderState(orderstate) {
  localStorage.setItem('lina_order', JSON.stringify(orderstate))
}

export const state = () => ({
  orders: [],
  currentIndex: 0,
  currentID: 0,
  lastCreatedID: 0,
  justCreated: false,
  isLoading: false,
  filterCriteria: '',
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
    state.lastCreatedID = order.id
    state.justCreated = true

    updateOrderState(state.orders)
  },
  SET_CURRENT_INDEX(state, index) {
    state.currentIndex = index
  },
  SET_CURRENT_ID(state, id) {
    state.currentID = id
  },

  SET_LAST_CREATED_ID(state, id) {
    state.lastCreatedID = id
  },

  SET_JUST_CREATED(state) {
    state.justCreated = !state.justCreated
  },

  SET_ISLOADING(state) {
    state.isLoading = !state.isLoading
  },

  SET_FILTER_CRITERIA(state, criteria) {
    state.filterCriteria = criteria
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
  setJustCreated({ commit }) {
    commit('SET_JUST_CREATED')
  },
  setLastCreatedID({ commit }, id) {
    commit('SET_LAST_CREATED_ID', id)
  },

  setFilterCriteria({ commit }, criteria) {
    commit('SET_FILTER_CRITERIA', criteria)
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
      customer_id: cart.carCustomer?.id || 0,
      customer_name: cart.cartCustomer?.name || '',
      customer_email: cart.cartCustomer?.email || '',
      customr_cel: cart.cartCustomer?.tel || '',
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
      commit('SET_ISLOADING')
      // Lanzar la excepción para que pueda ser capturada en asyncData
      throw error
    }
  },
}

export const getters = {
  // getOrders: (state) => state.orders,
  getOrders: (state) => {
    const filter = state.filterCriteria
    return state.orders.filter((order) => {
      const matchesCustomerName = filter
        ? order.customer_name.toLowerCase().includes(filter.toLowerCase())
        : true
      const matchesID = filter
        ? order.id.toString().toLowerCase().includes(filter.toLowerCase())
        : true

      return matchesCustomerName || matchesID
    })
  },

  getOrdersCount: (state, getters) => getters.getOrders.length || 0,
  getOrderByid: (state) => (id) =>
    state.orders.find((order) => order.id === id),
  getOrderByIndex: (state, getters) => (index) => getters.getOrders[index],
  getIndexByOrderID: (state, getters) => (id) =>
    getters.getOrders.findIndex((order) => order.id === id),
  getOrdersByCustomer: (state, getters) => (customerId) =>
    getters.getOrders.filter((order) => order.customer_id === customerId),
  getOrderTotalByID: (state, getters) => (id) => {
    const order = getters.getOrders.find((order) => order.id === id)
    return order
      ? order.items.reduce((acc, item) => acc + item.price * item.quantity, 0)
      : 0
  },
  getOrderTotalByIndex: (state, getters) => (index) => {
    const order = getters.getOrders[index]
    return order ? order.total : 0
  },
  getCurrentOrderTotal: (state, getters) => {
    const order = getters.getOrders[state.currentIndex]
    return order ? order.total : 0
  },

  getCurrentOrder: (state, getters) => getters.getOrders[state.currentIndex],
  getCurrentIndex: (state) => state.currentIndex,
  getCurrentID: (state) => state.currentID,
  getLastCreatedID: (state) => state.lastCreatedID,
  getJustCreated: (state) => state.justCreated,
  getLoadingStatus: (state) => state.isLoading,
}
