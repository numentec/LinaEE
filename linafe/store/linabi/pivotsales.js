import CustomStore from 'devextreme/data/custom_store'

export const namespaced = true

export const state = () => ({
  row: '',
  curStore: [],
  period: [],
  isLoading: false,
})

export const mutations = {
  SET_ROW(state, payload) {
    state.row = payload
  },
  SET_CUR_STORE(state, payload) {
    state.curStore = payload
  },
  SET_LOADING_STATUS(state) {
    state.isLoading = !state.isLoading
  },
  SET_PERIOD(state, payload) {
    state.period = payload
  },
}

export const actions = {
  setRow({ commit }, payload) {
    commit('SET_ROW', payload)
  },
  setPeriod({ commit }, payload) {
    commit('SET_PERIOD', payload)
  },
  setCurStore({ commit }, payload) {
    commit('SET_CUR_STORE', payload)
  },
  setIsLoading({ commit }) {
    commit('SET_LOADING_STATUS')
  },
  renewStore(context, curparams = null) {
    context.commit('SET_LOADING_STATUS')

    const ax = this.$axios

    async function load() {
      return await ax
        .get('linabi/extbidashboard/', {
          params: curparams,
        })
        .then((response) => response.data)
    }

    const store = new CustomStore({
      key: 'ID',
      load,
      onLoaded: (data) => {
        context.commit('SET_CUR_STORE', data)
      },
    })

    context.commit('SET_LOADING_STATUS')

    return store
  },
}

export const getters = {
  getRow(state) {
    return state.row
  },
  getPeriod(state) {
    return state.period
  },
  isLoading(state) {
    return state.isLoading
  },
}
