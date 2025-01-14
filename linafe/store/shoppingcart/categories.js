// import CustomStore from 'devextreme/data/custom_store'
export const namespaced = true

export const state = () => ({
  departments: [],
  categories: [],
  subcategories: [],
  brands: [],
  selected_brands: [],
  search_department: '',
  search_category: '',
  search_subcategory: '',
  viewconf: [],
  select_products_by: {
    depto: '0',
    cat: '0',
    scat: '0',
  },
  customers: [],
  isLoading: false,
  breadcrumbs: [],
})

export const mutations = {
  SET_LOADING_STATUS(state) {
    state.isLoading = !state.isLoading
  },
  SET_DEPARTMENTS(state, departments) {
    state.departments = departments
  },
  SET_CATEGORIES(state, categories) {
    state.categories = categories
  },
  SET_SUBCATEGORIES(state, subcategories) {
    state.subcategories = subcategories
  },
  SET_BRANDS(state, brands) {
    state.brands = brands
  },
  ADD_CATEGORY(state, category) {
    state.categories.push(category)
  },
  REMOVE_CATEGORY(state, categoryId) {
    state.categories = state.categories.filter(
      (category) => category.id !== categoryId
    )
  },
  SET_SELECTED_BRANDS(state, brands) {
    state.selected_brands = brands
    localStorage.setItem('lina_selectedBrands', JSON.stringify(brands))
  },
  SET_SEARCH_DEPARTMENT(state, department) {
    state.search_department = department
    localStorage.setItem('lina_searchDepartment', JSON.stringify(department))
  },
  SET_SEARCH_CATEGORY(state, category) {
    state.search_category = category
    localStorage.setItem('lina_searchCategory', JSON.stringify(category))
  },
  SET_SEARCH_SUBCATEGORY(state, subcategory) {
    state.search_subcategory = subcategory
    localStorage.setItem('lina_searchSubcategory', JSON.stringify(subcategory))
  },
  SET_VIEWCONF(state, viewconf) {
    state.viewconf = viewconf
  },
  SET_SELECT_PRODUCTS_BY(state, selectProductsBy) {
    state.select_products_by = selectProductsBy
    localStorage.setItem('lina_selProdsBy', JSON.stringify(selectProductsBy))
  },
  SET_SELECT_PRODUCTS_BY_ELEMENT(state, { key, value }) {
    state.select_products_by[key] = value
    localStorage.setItem(
      'lina_selProdsBy',
      JSON.stringify(state.select_products_by)
    )
  },
  SET_CUSTOMERS(state, customers) {
    state.customers = customers
  },
  SET_BREADCRUMBS(state, breadcrumbs) {
    state.breadcrumbs = breadcrumbs
    // console.log('Breadcrumbs:', state.breadcrumbs)
    localStorage.setItem('lina_breadcrumbs', JSON.stringify(state.breadcrumbs)) // Save to local storage
  },
}

export const actions = {
  nuxtClientInit({ commit }) {
    if (process.client) {
      const selectedBrands =
        JSON.parse(localStorage.getItem('lina_selectedBrands')) || []
      commit('SET_SELECTED_BRANDS', selectedBrands)

      const searchDepartment =
        JSON.parse(localStorage.getItem('lina_searchDepartment')) || ''
      commit('SET_SEARCH_DEPARTMENT', searchDepartment)

      const searchCategory =
        JSON.parse(localStorage.getItem('lina_searchCategory')) || ''
      commit('SET_SEARCH_CATEGORY', searchCategory)

      const searchSubcategory =
        JSON.parse(localStorage.getItem('lina_searchSubcategory')) || ''
      commit('SET_SEARCH_SUBCATEGORY', searchSubcategory)

      const selProdsBy = JSON.parse(
        localStorage.getItem('lina_selProdsBy')
      ) || {
        depto: '0',
        cat: '0',
        scat: '0',
      }
      commit('SET_SELECT_PRODUCTS_BY', selProdsBy)

      const breadcrumbs =
        JSON.parse(localStorage.getItem('lina_breadcrumbs')) || []
      commit('SET_BREADCRUMBS', breadcrumbs)
    }
  },

  setIsLoading({ commit }) {
    commit('SET_LOADING_STATUS')
  },
  async fetchItems({ commit, dispatch }, payload) {
    commit('SET_LOADING_STATUS')

    let curMutation = ''
    let endpointParams = {}

    switch (payload.name) {
      case 'Department':
        curMutation = 'SET_DEPARTMENTS'
        endpointParams = { p01: 'DEPTO', p02: '01' }
        break
      case 'Category':
        curMutation = 'SET_CATEGORIES'
        endpointParams = { p01: 'CAT', p02: '01' }
        break
      case 'Subcategory':
        curMutation = 'SET_SUBCATEGORIES'
        endpointParams = { p01: 'SCAT', p02: '01' }
        break
      case 'Product':
        curMutation = 'SET_PRODUCTS'
        endpointParams = { p01: 'PROD', p02: '01' }
        break
      case 'Brand':
        curMutation = 'SET_BRANDS'
        endpointParams = { p01: 'BRAND', p02: '01' }
        break
    }

    return await this.$axios
      .get('shoppingcart/catsbrands/', {
        params: endpointParams,
      })
      .then((response) => {
        commit(curMutation, response.data)
        commit('SET_LOADING_STATUS')
        return { items: response.data }
      })
  },

  addCategory({ commit }, category) {
    commit('ADD_CATEGORY', category)
  },
  removeCategory({ commit }, categoryId) {
    commit('REMOVE_CATEGORY', categoryId)
  },
  setBrands({ commit }, brands) {
    commit('SET_BRANDS', brands)
  },
  setSelectedBrands({ commit }, brands) {
    commit('SET_SELECTED_BRANDS', brands)
  },
  setSearchDepartment({ commit }, department) {
    commit('SET_SEARCH_DEPARTMENT', department)
  },
  setSearchCategory({ commit }, category) {
    commit('SET_SEARCH_CATEGORY', category)
  },
  setSearchSubcategory({ commit }, subcategory) {
    commit('SET_SEARCH_SUBCATEGORY', subcategory)
  },
  setViewConf({ commit }, viewconf) {
    commit('SET_VIEWCONF', viewconf)
  },
  setSelectProductsBy({ commit }, selectProductsBy) {
    commit('SET_SELECT_PRODUCTS_BY', selectProductsBy)
  },
  setSelectProductsByElement({ commit }, { key, value }) {
    commit('SET_SELECT_PRODUCTS_BY_ELEMENT', { key, value })
  },
  setCustomers({ commit }, customers) {
    commit('SET_CUSTOMERS', customers)
  },
  setBreadcrumbs({ commit }, breadcrumbs) {
    commit('SET_BREADCRUMBS', breadcrumbs)
  },
}

export const getters = {
  getAllDepartments: (state) => state.departments,
  getDepartmentById: (state) => (id) =>
    state.departments.find((department) => department.id === id),

  getAllCategories: (state) => state.categories,
  getCategoryById: (state) => (id) =>
    state.categories.find((category) => category.id === id),

  getAllSubcategories: (state) => state.subcategories,
  getSubcategoryById: (state) => (id) =>
    state.subcategories.find((subcategory) => subcategory.id === id),

  getBrands: (state) => state.brands,
  getSelectedBrands: (state) => state.selected_brands,
  getSearchDepartment: (state) => state.search_department,
  getSearchCategory: (state) => state.search_category,
  getSearchSubcategory: (state) => state.search_subcategory,
  getViewConf: (state) => state.viewconf,
  getViewConfElement: (state) => (name, element) => {
    const conf = state.viewconf.find((conf) => conf.configkey === name)

    return conf ? `/shoppingcart/categories/${conf[element]}` : null
  },
  getSelectProductsBy: (state) => state.select_products_by,
  getSelectProductsByElement: (state) => (key) => state.select_products_by[key],
  getCustomers: (state) => state.customers,
  getCustomerById: (state) => (id) =>
    state.customers.find((customer) => customer.id === id),
  getIsLoading: (state) => state.isLoading,
  getBreadcrumbs: (state) => state.breadcrumbs,
}
