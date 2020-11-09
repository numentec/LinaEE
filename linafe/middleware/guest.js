export default function ({ redirect, store, route }) {
  const ruta = route.path
  if (store.getters['sistema/loggedIn'] && ruta.includes('/login')) {
    redirect('/')
  }
}
