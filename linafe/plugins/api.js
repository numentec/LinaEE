export default function ({ $axios }, inject) {
  const api = {
    getCatalog(id) {
      return $axios.$get(`/api/catalogos/${id}/`)
    },
    getPublicCatalog(token) {
      return $axios.$get(`/api/public/catalogos/${token}/`)
    },
  }

  inject('api', api)
}
