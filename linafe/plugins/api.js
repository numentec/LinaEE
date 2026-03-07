export default function ({ $axios }, inject) {
  const api = {
    createCatalog(payload) {
      return $axios.$post('/catalog/api/catalogs/', payload)
    },

    // retrive all catalogs
    getCatalogs() {
      return $axios.$get('catalog/api/catalogs/')
    },

    // retrive one catalog by id
    getCatalog(id) {
      return $axios.$get(`catalog/api/catalogs/${id}/`)
    },

    // Duplicate a catalog by id
    duplicateCatalog(id) {
      return $axios.$post(`catalog/api/catalogs/${id}/duplicate/`)
    },

    updateCatalog(id, payload) {
      return $axios.$patch(`catalog/api/catalogs/${id}/`, payload)
    },

    // retrive all public catalogs
    getPublicCatalogs() {
      return $axios.$get('catalog/api/public/catalogs/')
    },

    // retrive one public catalog by token
    getPublicCatalog(token) {
      return $axios.$get(`catalog/api/public/catalogs/${token}/`)
    },
  }

  inject('api', api)
}
