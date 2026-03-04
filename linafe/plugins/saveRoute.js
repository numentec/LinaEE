export default ({ app }) => {
  app.router.beforeEach((to, from, next) => {
    if (process.client) {
      const isToLogin = to.path && to.path.startsWith('/login')
      const isFromLogin = from.path && from.path.startsWith('/login')

      if (!isFromLogin && from.path) {
        localStorage.setItem('lina_prevPath', from.path)
      }

      if (!isToLogin && to.fullPath) {
        // localStorage.setItem('lina_lastRoute', to.fullPath)
        localStorage.setItem('lina_lastPath', to.fullPath)
      }
    }
    next()
  })
}
