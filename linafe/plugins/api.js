export default function ({ $axios }, inject) {
  const api = {
    // retrive one catalog by id
    getCatalog(id) {
      return $axios.$get(`catalog/api/catalogos/${id}/`)
    },

    // retrive one public catalog by token
    getPublicCatalog(token) {
      return $axios.$get(`catalog/api/public/catalogos/${token}/`)
    },

    // retrive all catalogs
    getCatalogs() {
      return $axios.$get('catalog/api/catalogs/')
    },

    // retrive all public catalogs
    getPublicCatalogs() {
      return $axios.$get('catalog/api/public/catalogs/')
    },
  }

  inject('api', api)
}
