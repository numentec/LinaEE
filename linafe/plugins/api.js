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

    ensureShareToken(id) {
      return $axios.$post(`catalog/api/catalogs/${id}/ensure-share-token/`)
    },

    regenerateShareToken(id) {
      return $axios.$post(`catalog/api/catalogs/${id}/regenerate-share-token/`)
    },

    // retrive all public catalogs
    getPublicCatalogs() {
      return $axios.$get('catalog/api/public/catalogs/')
    },

    // retrive one public catalog by token
    getPublicCatalog(token) {
      return $axios.$get(`catalog/api/public/catalogs/${token}/`)
    },

    // retrive one order (read only) by its public token
    getPublicOrder(token) {
      return $axios.$get(`saleapp/public/orders/${token}/`)
    },
  }

  inject('api', api)
}
