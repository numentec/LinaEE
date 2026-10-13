export default async function ({
  $auth,
  $axios,
  store,
  error,
  redirect,
  route,
}) {
  if ($auth && $auth.loggedIn) {
    try {
      const response = await $axios.get('cias/')
      const cias = response.data
      const curC = cias.find((c) => c.default === true)

      store.dispatch('sistema/setCias', cias)
      store.dispatch('sistema/setCurCia', curC)
    } catch (err) {
      if (err.response && err.response.status === 401) {
        if ($auth && typeof $auth.reset === 'function') {
          $auth.reset()
        }
        if (store) {
          store.commit('sistema/USER_LOGOUT')
        }
        const targetPath = route ? route.fullPath || route.path : '/'
        return redirect(`/login?redirect=${encodeURIComponent(targetPath)}`)
      }

      if (err.response) {
        error({
          statusCode: err.response.status,
          message: err.response.data.detail,
        })
      } else {
        error({
          statusCode: 503,
          message: 'No se pudo cargar la lista de compañías. Intente luego',
        })
      }
    }
  }
}
