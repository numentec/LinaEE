// Plugin para control de inactividad de usuario en cliente
// Si el usuario pasa un periodo prolongado de inactividad, se cierra la sesión limpiamente.

const INACTIVITY_TIMEOUT_MS = 60 * 60 * 1000 // 60 minutos de inactividad
const CHECK_INTERVAL_MS = 60 * 1000 // Comprobación cada 1 minuto
const ACTIVITY_STORAGE_KEY = 'lina_last_activity'

export default (context) => {
  if (!process.client) return

  const { store, redirect, route, app } = context

  const getAuth = () =>
    context.$auth || (app && app.$auth) || (window.$nuxt && window.$nuxt.$auth)

  const isUserLoggedIn = () => {
    const auth = getAuth()
    if (auth && typeof auth.loggedIn !== 'undefined') {
      return Boolean(auth.loggedIn)
    }
    if (store && store.state && store.state.auth) {
      return Boolean(store.state.auth.loggedIn)
    }
    try {
      const token = localStorage.getItem('auth._token.local')
      return Boolean(token && token !== 'false')
    } catch (e) {
      return false
    }
  }

  const updateActivity = () => {
    try {
      localStorage.setItem(ACTIVITY_STORAGE_KEY, Date.now().toString())
    } catch (e) {}
  }

  const logoutDueToInactivity = () => {
    const auth = getAuth()
    if (auth && typeof auth.reset === 'function') {
      try {
        auth.reset()
      } catch (e) {}
    }
    if (store) {
      try {
        store.commit('sistema/USER_LOGOUT')
      } catch (e) {}
    }
    try {
      for (const key in localStorage) {
        if (key.startsWith('lina_') || key.startsWith('auth.')) {
          localStorage.removeItem(key)
        }
      }
      localStorage.removeItem(ACTIVITY_STORAGE_KEY)
    } catch (e) {}

    const currentRoute =
      route ||
      (app && app.router && app.router.currentRoute) ||
      (window.$nuxt && window.$nuxt.$route)
    const currentPath =
      (currentRoute && (currentRoute.fullPath || currentRoute.path)) ||
      (window.location && window.location.pathname) ||
      '/'

    if (!currentPath.startsWith('/login')) {
      if (typeof redirect === 'function') {
        redirect(`/login?redirect=${encodeURIComponent(currentPath)}`)
      } else if (window.location) {
        window.location.href = `/login?redirect=${encodeURIComponent(
          currentPath
        )}`
      }
    }
  }

  const checkInactivity = () => {
    if (!isUserLoggedIn()) return

    const lastActivityStr = localStorage.getItem(ACTIVITY_STORAGE_KEY)
    if (!lastActivityStr) {
      updateActivity()
      return
    }

    const lastActivity = parseInt(lastActivityStr, 10)
    const now = Date.now()

    if (now - lastActivity > INACTIVITY_TIMEOUT_MS) {
      logoutDueToInactivity()
    }
  }

  const init = () => {
    // Registrar eventos de interacción de usuario para refrescar la marca de actividad
    const userEvents = [
      'mousemove',
      'keydown',
      'mousedown',
      'touchstart',
      'scroll',
    ]
    let throttleTimer = null

    const onUserInteraction = () => {
      if (!throttleTimer) {
        throttleTimer = setTimeout(() => {
          if (isUserLoggedIn()) {
            updateActivity()
          }
          throttleTimer = null
        }, 5000) // Throttle de 5 segundos para evitar escrituras excesivas a localStorage
      }
    }

    userEvents.forEach((event) => {
      window.addEventListener(event, onUserInteraction, { passive: true })
    })

    // Comprobación inicial de inactividad
    if (isUserLoggedIn()) {
      const lastActivityStr = localStorage.getItem(ACTIVITY_STORAGE_KEY)
      if (lastActivityStr) {
        const lastActivity = parseInt(lastActivityStr, 10)
        const now = Date.now()
        if (now - lastActivity > INACTIVITY_TIMEOUT_MS) {
          logoutDueToInactivity()
          return
        }
      }
      updateActivity()
    }

    // Comprobar periódicamente
    setInterval(checkInactivity, CHECK_INTERVAL_MS)
  }

  if (typeof window.onNuxtReady === 'function') {
    window.onNuxtReady(init)
  } else {
    init()
  }
}
