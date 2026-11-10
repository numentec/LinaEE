// Páginas públicas que no deben recordarse como destino después del login
const PUBLIC_SHARED_PATHS = ['/portal/shared-order']

export default ({ app }) => {
  app.router.beforeEach((to, from, next) => {
    if (process.client) {
      const isToLogin = to.path && to.path.startsWith('/login')
      const isFromLogin = from.path && from.path.startsWith('/login')

      if (!isFromLogin && from.path) {
        localStorage.setItem('lina_prevPath', from.path)
      }

      const isSharedPage = PUBLIC_SHARED_PATHS.some(
        (prefix) => to.path && to.path.startsWith(prefix)
      )

      if (!isToLogin && !isSharedPage && to.fullPath) {
        // localStorage.setItem('lina_lastRoute', to.fullPath)
        localStorage.setItem('lina_lastPath', to.fullPath)
      }
    }
    next()
  })
}
