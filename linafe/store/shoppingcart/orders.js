import JSZip from 'jszip'
import saveAs from 'file-saver'

export const namespaced = true

function updateOrderState(orderstate) {
  localStorage.setItem('lina_order', JSON.stringify(orderstate))
}

// Construye el payload de una orden a partir del carrito
function buildOrderPayload(cart) {
  return {
    customer_id: cart.cartCustomer?.id || '0',
    customer_name: cart.cartCustomer?.name || '',
    customer_email: cart.cartCustomer?.email || '',
    customer_cel: cart.cartCustomer?.tel || '',
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
}

// Descarga un archivo generado por el backend para una orden
async function downloadOrderFile(axios, { url, params, type, filename }) {
  const response = await axios.get(url, {
    responseType: 'blob', // Importante para manejar archivos binarios
    params,
  })

  saveAs(new Blob([response.data], { type }), filename)
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
  // Reemplaza una orden existente y la marca para que ordersview se posicione en ella
  REPLACE_ORDER(state, order) {
    const index = state.orders.findIndex((o) => o.id === order.id)
    if (index > -1) {
      state.orders.splice(index, 1, order)
    } else {
      state.orders.push(order)
    }

    state.currentID = order.id
    state.lastCreatedID = order.id
    state.justCreated = true

    updateOrderState(state.orders)
  },
  UPDATE_ORDER_STATUS(state, { id, status }) {
    const order = state.orders.find((order) => order.id === id)
    if (order) {
      order.status = status
      updateOrderState(state.orders)
    }
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

    const newOrder = buildOrderPayload(rootState.shoppingcart.cart.cart)

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

  // Actualiza la orden ligada al carrito (Keep selling) con el contenido del carrito
  async updateOrder({ commit, dispatch, rootState }) {
    commit('SET_ISLOADING')

    const cart = rootState.shoppingcart.cart.cart

    try {
      const response = await this.$axios.put(
        `shoppingcart/extorder/${cart.orderId}/`,
        buildOrderPayload(cart)
      )

      commit('REPLACE_ORDER', response.data)
      await dispatch('shoppingcart/cart/clearCart', null, { root: true })

      commit('SET_ISLOADING')
    } catch (error) {
      commit('SET_ISLOADING')
      throw error
    }
  },

  async updateOrderStatus({ commit }, payload) {
    const { id, status } = payload

    try {
      const response = await this.$axios.patch(
        `shoppingcart/extorderonly/${id}/`,
        { status }
      )
      commit('UPDATE_ORDER_STATUS', { id, status: response.data.status })
    } catch (error) {
      console.error('Error updating order status:', error)
      throw error
    }
  },

  async csvDownload({ commit }, orderid) {
    try {
      await downloadOrderFile(this.$axios, {
        url: `shoppingcart/orders/${orderid}/csv/`,
        type: 'text/csv',
        filename: `order_${orderid}.csv`,
      })
    } catch (error) {
      console.error('Error downloading CSV:', error)
      throw error // Maneja el error según sea necesario
    }
  },

  async pdfDownload({ commit }, payload) {
    const { orderid, printImages } = payload // Desestructura el orderid del payload

    try {
      await downloadOrderFile(this.$axios, {
        url: `shoppingcart/orders/${orderid}/pdf/`,
        params: printImages === true ? { print_images: '1' } : {},
        type: 'application/pdf',
        filename: `order_${orderid}.pdf`,
      })
    } catch (error) {
      console.error('Error downloading PDF:', error)
      throw error // Maneja el error según sea necesario
    }
  },

  // Excel con imágenes por defecto; printImages = false las omite
  async xlsxDownload({ commit }, payload) {
    const { orderid, printImages = true } = payload

    try {
      await downloadOrderFile(this.$axios, {
        url: `shoppingcart/orders/${orderid}/xlsx/`,
        params: printImages ? {} : { print_images: '0' },
        type:
          'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        filename: `order_${orderid}.xlsx`,
      })
    } catch (error) {
      console.error('Error downloading Excel:', error)
      throw error
    }
  },

  async imagesZipDownload({ rootGetters }, payload) {
    const { orderid, items } = payload
    const zip = new JSZip()
    const usedNames = new Set()

    // Descarga una imagen; devuelve null si falla para omitirla del zip
    const downloadImage = async (url) => {
      try {
        const response = await fetch(url)
        return response.ok ? await response.arrayBuffer() : null
      } catch (error) {
        return null
      }
    }

    try {
      const promises = (items || [])
        .filter((item) => item.image)
        .map(async (item) => {
          const url =
            rootGetters['shoppingcart/products/getImage'](item.id) ||
            this.$config.fotosURL + item.image

          const data = await downloadImage(url)
          if (!data) return false

          // Nombre del archivo dentro del zip (evita duplicados)
          let filename = item.image.split('/').pop()
          if (usedNames.has(filename)) {
            filename = `${item.sku}_${filename}`
          }
          usedNames.add(filename)

          zip.file(filename, data, { binary: true })
          return true
        })

      const results = await Promise.all(promises)

      if (!results.some(Boolean)) {
        throw new Error('No images to download')
      }

      const content = await zip.generateAsync({ type: 'blob' })
      saveAs(content, `order_${orderid}_images.zip`)
    } catch (error) {
      console.error('Error downloading images:', error)
      throw error // Maneja el error según sea necesario
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
