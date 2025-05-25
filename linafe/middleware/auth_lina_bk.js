export default function ({ $auth, store, redirect, route }) {
  const publicRoutes = ['/portal', '/public', '/aboutlina'] // Rutas públicas
  if (!process.server && !publicRoutes.includes(route.path)) {
    const curuser = localStorage.getItem('curuser')
    if (curuser) {
      const cu = JSON.parse(curuser)
      store.dispatch('sistema/setUserData', cu).then(() => {
        if (cu.homelink) {
          // this.$router.push(cu.homelink)
          redirect(cu.homelink)
        } else {
          // this.$router.push('/')
          redirect('/')
        }
      })
    }
  }
}
