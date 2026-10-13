export default function (context) {
  const { $axios, store, redirect, route, app } = context

  $axios.onError((error) => {
    const code = parseInt(error.response && error.response.status)

    // Si el error es 401 (Unauthorized / Token inválido o expirado)
    if (code === 401) {
      // Si el error ocurrió intentando iniciar sesión en /login, dejamos que el formulario de login maneje el error
      const requestUrl =
        error.config && error.config.url ? error.config.url : ''
      if (requestUrl.includes('login/')) {
        return Promise.reject(error)
      }

      if (process.client) {
        // Limpiar todas las claves de lina_* y auth.* en localStorage
        try {
          for (const key in localStorage) {
            if (key.startsWith('lina_') || key.startsWith('auth.')) {
              localStorage.removeItem(key)
            }
          }
        } catch (e) {}
      }

      // Resetear estado del módulo de auth de forma segura si está presente
      const auth =
        context.$auth ||
        (app && app.$auth) ||
        (process.client && window.$nuxt && window.$nuxt.$auth)

      if (auth && typeof auth.reset === 'function') {
        try {
          auth.reset()
        } catch (e) {}
      }

      // Limpiar datos de usuario en store del sistema
      if (store) {
        try {
          store.commit('sistema/USER_LOGOUT')
        } catch (e) {}
      }

      // Redirigir a login si no estamos ya allí
      const currentRoute =
        route ||
        (app && app.router && app.router.currentRoute) ||
        (process.client && window.$nuxt && window.$nuxt.$route)
      const currentPath =
        (currentRoute && (currentRoute.fullPath || currentRoute.path)) ||
        (process.client && window.location && window.location.pathname) ||
        '/'

      if (!currentPath.startsWith('/login')) {
        if (typeof redirect === 'function') {
          redirect(`/login?redirect=${encodeURIComponent(currentPath)}`)
        } else if (process.client && window.location) {
          window.location.href = `/login?redirect=${encodeURIComponent(
            currentPath
          )}`
        }
      }

      return Promise.resolve(false)
    }

    return Promise.reject(error)
  })
}
