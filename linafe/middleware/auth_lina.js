export default function authLina({ redirect, store, route }) {
  const ruta = route.path
  if (!store.getters['sistema/loggedIn']) {
    redirect('/login')
  } else if (ruta.includes('/login')) {
    redirect('/')
  }
}
