export const getters = {
  isAuthenticated(state) {
    return state.auth.loggedIn
  },

  loggedInUser(state) {
    return state.auth.user
  },
}

export const actions = {
  async nuxtClientInit({ commit, dispatch }) {
    if (process.client) {
      const error = localStorage.getItem('lina_error')
      if (error) {
        await commit('sistema/SET_ERROR', JSON.parse(error))
      }
      const users = localStorage.getItem('lina_users')
      if (users) {
        commit('sistema/SET_USERS', JSON.parse(users))
      }
      const isLoading = localStorage.getItem('lina_isLoading')
      if (isLoading) {
        commit('sistema/SET_LOADING_STATUS', JSON.parse(isLoading))
      }
      const cias = localStorage.getItem('lina_cias')
      if (cias) {
        commit('sistema/SET_CIAS', JSON.parse(cias))
      }
      const curCia = localStorage.getItem('lina_curCia')
      if (curCia) {
        commit('sistema/SET_CURCIA', JSON.parse(curCia))
      }
      const showBottomNav = localStorage.getItem('lina_showBottomNav')
      if (showBottomNav) {
        commit('sistema/SET_SHOWBOTTOMNAV', JSON.parse(showBottomNav))
      }

      if (localStorage.getItem('lina_selProdsBy')) {
        await dispatch('shoppingcart/categories/nuxtClientInit')
      }

      if (localStorage.getItem('lina_cart')) {
        await dispatch('shoppingcart/cart/nuxtClientInit')
      }

      if (localStorage.getItem('lina_cartImages')) {
        await dispatch('shoppingcart/products/nuxtClientInit')
      }
    }
  },
}
