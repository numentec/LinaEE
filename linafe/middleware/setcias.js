export default async function ({ $auth, $axios, store, error }) {
  if ($auth.loggedIn) {
    try {
      await $axios.get('cias/').then((response) => {
        const cias = response.data
        const curC = cias.find((c) => c.default === true)

        store.dispatch('sistema/setCias', cias)
        store.dispatch('sistema/setCurCia', curC)
      })
    } catch (err) {
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
