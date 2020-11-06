export default function authLina({ redirect, store, route }) {
  const ruta = route.path
  if (ruta.includes('/lina')) {
    if (!store.getters['sistema/loggedIn']) {
      redirect('/lina/login')
    } else if (ruta === '/lina/login') {
      redirect('/lina')
    }
  }
}
