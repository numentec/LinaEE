export default function ({ $auth, redirect, route }) {
  const publicPrefixes = ['/login', '/portal', '/public', '/aboutlina']

  const isPublic = publicPrefixes.some((r) => route.path.startsWith(r))
  if (isPublic) return

  if (!$auth.loggedIn) {
    const targetPath = route.fullPath || route.path || '/'
    return redirect(`/login?redirect=${encodeURIComponent(targetPath)}`)
  }
}

// PRIMERA ALTERNATIVA PROBADA, PERO NO FUNCIONA BIEN CON LA LÓGICA DE LOGIN ACTUAL (GUARDA USUARIO EN LOCALSTORAGE Y NO EN VUEX HASTA QUE SE CARGA LA PÁGINA DE LOGIN)
// export default function ({ $auth, store, redirect, route }) {
//   const publicRoutes = ['/portal', '/public', '/aboutlina'] // Rutas públicas
//   if (!process.server && !publicRoutes.includes(route.path)) {
//     const curuser = localStorage.getItem('curuser')
//     if (curuser) {
//       const cu = JSON.parse(curuser)
//       store.dispatch('sistema/setUserData', cu).then(() => {
//         if (cu.homelink) {
//           // this.$router.push(cu.homelink)
//           redirect(cu.homelink)
//         } else {
//           // this.$router.push('/')
//           redirect('/')
//         }
//       })
//     }
//   }
// }

// MIDDLEWARE QUE PRETENDÍA PERMITIR USUARIO GUEST
// export default function ({ redirect, store, route }) {
//   const ruta = route.path
//   if (store.getters['sistema/loggedIn'] && ruta.includes('/login')) {
//     redirect('/')
//   }
// }
