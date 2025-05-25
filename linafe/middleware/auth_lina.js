export default function ({ $auth, redirect, route }) {
  const publicRoutes = ['/login', '/portal', '/public', '/aboutlina'] // Rutas públicas
  // If the user is not logged in and the route is not public, redirect to login
  if (!$auth.loggedIn && !publicRoutes.includes(route.path)) {
    return redirect('/login')
  }
}
