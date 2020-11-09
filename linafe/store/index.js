export const getters = {
  isAuthenticated(state) {
    return state.auth.loggedIn
  },

  loggedInUser(state) {
    return state.auth.user
  },
}

// export const actions = {
//   nuxtServerInit() {
//     if (!process.server) {
//       const userString = localStorage.getItem('curuser')
//       if (userString) {
//         const userData = JSON.parse(userString)
//         this.$store.commit('sistema/SET_USER_DATA', userData)
//       }
//     }
//   },
// }

// const cookieparser = process.server ? require('cookieparser') : undefined

// export const actions = {
//   nuxtServerInit({ commit }, { req }) {
//     let auth = null
//     if (req.headers.cookie) {
//       const parsed = cookieparser.parse(req.headers.cookie)
//       try {
//         auth = JSON.parse(parsed.auth)
//       } catch (err) {
//         // No valid cookie found
//       }
//     }
//     commit('setAuth', auth)
//   },
// }
