/* eslint-disable no-console */
import CustomStore from 'devextreme/data/custom_store'
export const namespaced = true

export const state = () => ({
  listCli: [], // Clientes
  listVen: [], // Vendedores
  listMar: [], // Marcas
  listBod: [], // Ubicaciones (Bodegas)
  listCla1: [], // Departamentos
  listCla2: [], // Categorías
  listCla3: [], // Sub categorías
  listClax: [], // Categorías extra
  listed: false,
  error: null,
  variants: [],
  variants_tallas: [],
  variants_colors: [],
  fotos: {},
  loadingView: false,
  slidecurkey: '',
})

export const mutations = {
  SET_LIST_CLI(state, payload) {
    state.listCli = payload
  },
  SET_LIST_VEN(state, payload) {
    state.listVen = payload
  },
  SET_LIST_MAR(state, payload) {
    state.listMar = payload
  },
  SET_LIST_BOD(state, payload) {
    state.listBod = payload
  },
  SET_LIST_CLA1(state, payload) {
    state.listCla1 = payload
  },
  SET_LIST_CLA2(state, payload) {
    state.listCla2 = payload
  },
  SET_LIST_CLA3(state, payload) {
    state.listCla3 = payload
  },
  SET_LIST_CLAX(state, payload) {
    state.listClax = payload
  },
  SET_LISTED(state, payload) {
    state.listed = payload
  },
  SET_ERROR(state, payload) {
    state.error = payload
  },
  SET_VARIANTS(state, payload) {
    state.variants = payload
  },
  SET_VARIANTS_TALLAS(state, payload) {
    state.variants_tallas = payload
  },
  SET_VARIANTS_COLORS(state, payload) {
    state.variants_colors = payload
  },
  SET_FOTOS(state, payload) {
    state.fotos = payload
  },
  SET_LOADING_VIEW(state, payload) {
    state.loadingView = payload
  },
  SET_SLIDECURKEY(state, payload) {
    state.slidecurkey = payload
  },
}

export const actions = {
  setListCli({ commit }, payload) {
    commit('SET_LIST_CLI', payload)
  },
  setListVen({ commit }, payload) {
    commit('SET_LIST_VEN', payload)
  },
  setListMarca({ commit }, payload) {
    commit('SET_LIST_MAR', payload)
  },
  setListBod({ commit }, payload) {
    commit('SET_LIST_BOD', payload)
  },
  setListCla1({ commit }, payload) {
    commit('SET_LIST_CLA1', payload)
  },
  setListCla2({ commit }, payload) {
    commit('SET_LIST_CLA2', payload)
  },
  setListCla3({ commit }, payload) {
    commit('SET_LIST_CLA3', payload)
  },
  setListClax({ commit }, payload) {
    commit('SET_LIST_CLAX', payload)
  },
  setLists({ commit, error }) {
    Promise.all([
      this.$axios.get('linabi/clists/', { params: { p01: 'CLI' } }),
      this.$axios.get('linabi/clists/', { params: { p01: 'VEN' } }),
      this.$axios.get('linabi/clists/', { params: { p01: 'MAR' } }),
      this.$axios.get('linabi/clists/', { params: { p01: 'BOD' } }),
      this.$axios.get('linabi/clists/', { params: { p01: 'CL1' } }),
      this.$axios.get('linabi/clists/', { params: { p01: 'CL2' } }),
      this.$axios.get('linabi/clists/', { params: { p01: 'CL3' } }),
      this.$axios.get('linabi/clists/', { params: { p01: 'CLX' } }),
    ])
      .then((responses) => {
        commit('SET_LIST_CLI', responses[0].data)
        commit('SET_LIST_VEN', responses[1].data)
        commit('SET_LIST_MAR', responses[2].data)
        commit('SET_LIST_BOD', responses[3].data)
        commit('SET_LIST_CLA1', responses[4].data)
        commit('SET_LIST_CLA2', responses[5].data)
        commit('SET_LIST_CLA3', responses[6].data)
        commit('SET_LIST_CLAX', responses[7].data)
        commit('SET_LISTED', true)
      })
      .catch((errs) => {
        commit('SET_LISTED', false)
        let error = {}
        if (errs.response) {
          error = {
            statusCode: errs.response.status,
            message: errs.response.data.detail,
          }
        } else {
          error = {
            statusCode: 503,
            message: 'No se pudo cargar las listas comunes',
          }
        }
        commit('SET_ERROR', error)
      })
  },

  setVariants({ commit }, payload) {
    commit('SET_VARIANTS', payload)
  },

  setVariantsTallas({ commit }, payload) {
    commit('SET_VARIANTS_TALLAS', payload)
  },

  setVariantsColors({ commit }, payload) {
    commit('SET_VARIANTS_COLORS', payload)
  },

  setFotos({ commit }, payload) {
    commit('SET_FOTOS', payload)
  },

  async fetchVariants({ commit }, payload) {
    const sku = payload.sku.toString()
    const cv = { name: payload.cv.toString() }

    if (cv.name === 'COLORES') {
      cv.endpoint = 'linabi/coloresbc'
    } else {
      cv.endpoint = 'linabi/tallasbc'
    }

    cv.mutation = 'SET_VARIANTS'

    return await this.$axios
      .get(cv.endpoint, {
        params: { sku },
      })
      .then((response) => {
        commit(cv.mutation, response.data)
        return response.data
      })
  },

  async fetchVariantsX({ commit }, payload) {
    const sku = payload.sku.toString()
    // Cuurent variant (cv) can be 1 for TALLAS, 2 for COLORES and 3 for both
    const cv = payload.cv.toString()

    const vv = { vt: [], vc: [] }
    let endpoints = []

    if (cv === '1') {
      endpoints = ['linabi/tallasbc']
    }

    if (cv === '2') {
      endpoints = ['linabi/coloresbc']
    }

    if (cv === '3') {
      endpoints = ['linabi/tallasbc', 'linabi/coloresbc']
    }

    await this.$axios
      .all(
        endpoints.map((endpoint) =>
          this.$axios.get(endpoint, {
            params: { sku },
          })
        )
      )
      .then((response) => {
        if (cv === '1') {
          commit('SET_VARIANTS_TALLAS', response[0].data)
          vv.vt = response[0].data
        }

        if (cv === '2') {
          commit('SET_VARIANTS_COLORS', response[0].data)
          vv.vc = response[0].data
        }

        if (cv === '3') {
          commit('SET_VARIANTS_TALLAS', response[0].data)
          vv.vt = response[0].data
          commit('SET_VARIANTS_COLORS', response[1].data)
          vv.vc = response[1].data
        }

        return vv
      })
  },

  async storeImages({ commit }, payload) {
    const ax = this.$axios.create({
      baseURL: this.$config.fotosURL,
      headers: {
        common: {
          Accept: 'image/*, application/json, text/plain, */*',
        },
      },
    })
    const ff = {}
    await payload.forEach(async (rowKey) => {
      const imgfile = rowKey + this.$config.fotosExt
      await ax
        .get(imgfile, {
          responseType: 'arraybuffer',
        })
        .then((response) => {
          const b64Img = Buffer.from(response.data, 'binary').toString('base64')
          const objKey = 'key' + rowKey
          ff[objKey] = b64Img
        })
        .catch((err) => {
          if (err.response.status === 404) {
          }
        })
    })

    commit('SET_FOTOS', ff)
    return ff
  },

  async imgDownload({ commit }, payload) {
    const ax = this.$axios.create({
      baseURL: this.$config.fotosURL,
      headers: {
        common: {
          Accept: 'image/*, application/json, text/plain, */*',
        },
      },
    })
    const imgfile = payload + this.$config.fotosExt
    return await ax
      .get(imgfile, {
        responseType: 'arraybuffer',
      })
      .then((response) => {
        return Buffer.from(response.data, 'binary').toString('base64')
      })
      .catch((err) => {
        if (err.response.status === 404) {
          return null
        }
      })
  },

  fetchTemplates({ commit }) {
    const ax = this.$axios

    // commit('SET_LOADING_STATUS')

    async function load() {
      return await ax
        .get('linabi/xlsxtemplates/')
        .then((response) => response.data)
    }

    const store = new CustomStore({
      key: 'id',
      load,
    })

    // commit('SET_LOADING_STATUS')

    return store
  },

  setError({ commit }, payload) {
    commit('SET_ERROR', payload)
  },

  setLoadingView({ commit }, payload) {
    commit('SET_LOADING_VIEW', payload)
  },

  setSlidecurkey({ commit }, payload) {
    commit('SET_SLIDECURKEY', payload)
  },
}

export const getters = {
  getListCli(state) {
    return state.listCli
  },
  getListVen(state) {
    return state.listVen
  },
  getListMar(state) {
    return state.listMar
  },
  getListBod(state) {
    return state.listBod
  },
  getListCla1(state) {
    return state.listCla1
  },
  getListCla2(state) {
    return state.listCla2
  },
  getListCla3(state) {
    return state.listCla3
  },
  getListClx1(state) {
    return state.listClax.filter((obj) => obj.TIPO === 'C1')
  },
  getListClx2(state) {
    return state.listClax.filter((obj) => obj.TIPO === 'C2')
  },
  getListClx3(state) {
    return state.listClax.filter((obj) => obj.TIPO === 'C3')
  },
  getAllVariants(state) {
    return async (sku) => {
      return await this.$axios
        .get('linabi/tallasbc', {
          params: { sku },
        })
        .then((response) => response.data)
    }
  },
  getVariants(state) {
    return state.variants
  },
  getAllVariantsTallas(state) {
    return async (sku) => {
      return await this.$axios
        .get('linabi/tallasbc', {
          params: { sku },
        })
        .then((response) => response.data)
    }
  },
  getVariantsTallas(state) {
    return state.variants_tallas
  },
  getAllVariantsColors(state) {
    return async (sku) => {
      return await this.$axios
        .get('linabi/colorsbc', {
          params: { sku },
        })
        .then((response) => response.data)
    }
  },
  getVariantsColors(state) {
    return state.variants_colors
  },
  getFotos(state) {
    return state.fotos
  },
  getLoadingView(state) {
    return state.loadingView
  },
  getSlidecurkey(state) {
    return state.slidecurkey
  },
}
