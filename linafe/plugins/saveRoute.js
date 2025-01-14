export default ({ app }) => {
  app.router.beforeEach((to, from, next) => {
    if (process.client) {
      localStorage.setItem('lina_lastRoute', to.fullPath)
    }
    next()
  })
}
