export default function ({ $axios }, inject) {
  const api = {
    getCatalog(id) {
      return $axios.$get(`catalog/api/catalogos/${id}/`)
    },
    getPublicCatalog(token) {
      return $axios.$get(`catalog/api/public/catalogos/${token}/`)
    },
  }

  inject('api', api)
}
