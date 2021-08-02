/* eslint-disable no-console */
import CustomStore from 'devextreme/data/custom_store'
export const namespaced = true

export const state = () => ({
  listCli: [], // Clientes
  listVen: [], // Vendedores
  listMar: [], // Marcas
  listCla1: [], // Departamentos
  listCla2: [], // Categorías
  listCla3: [], // Sub categorías
  listClax: [], // Categorías extra
  listed: false,
  error: null,
  variants: [],
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
      this.$axios.get('linabi/clists', { params: { p01: 'CLI' } }),
      this.$axios.get('linabi/clists', { params: { p01: 'VEN' } }),
      this.$axios.get('linabi/clists', { params: { p01: 'MAR' } }),
      this.$axios.get('linabi/clists', { params: { p01: 'CL1' } }),
      this.$axios.get('linabi/clists', { params: { p01: 'CL2' } }),
      this.$axios.get('linabi/clists', { params: { p01: 'CL3' } }),
      this.$axios.get('linabi/clists', { params: { p01: 'CLX' } }),
    ])
      .then((responses) => {
        commit('SET_LIST_CLI', responses[0].data)
        commit('SET_LIST_VEN', responses[1].data)
        commit('SET_LIST_MAR', responses[2].data)
        commit('SET_LIST_CLA1', responses[3].data)
        commit('SET_LIST_CLA2', responses[4].data)
        commit('SET_LIST_CLA3', responses[5].data)
        commit('SET_LIST_CLAX', responses[6].data)
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

  setFotos({ commit }, payload) {
    commit('SET_FOTOS', payload)
  },

  async fetchVariants({ commit }, payload) {
    const sku = payload.sku.toString()
    return await this.$axios
      .get('linabi/tallasbc', {
        params: { sku },
      })
      .then((response) => {
        commit('SET_VARIANTS', response.data)
        return response.data
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
