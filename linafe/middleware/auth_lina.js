export default function ({ $auth, redirect, route }) {
  const publicRoutes = ['/login', '/portal', '/public', '/aboutlina'] // Rutas públicas
  // If the user is not logged in and the route is not public, redirect to login
  // if (!$auth.loggedIn && !publicRoutes.includes(route.path)) {
  //   return redirect('/login')
  // }
  console.log('Auth Middleware Linafe', $auth.loggedIn, route.path)
  if (!$auth.loggedIn && !publicRoutes.some((r) => route.path.startsWith(r))) {
    return redirect('/login')
  }
}
