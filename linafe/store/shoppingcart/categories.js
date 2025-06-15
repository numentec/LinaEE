// import CustomStore from 'devextreme/data/custom_store'
export const namespaced = true

const BRANDSDATA = ['1', '2', '3', '4', '5', '187', '188', '189', '190', '191']
const IMAGES = [
  'http://192.168.1.55:8001/media/images/bifavoritos/prev3.gif',
  '/shoppingcart/H23100256A.jpg',
  '/shoppingcart/H23100133A.jpg',
  '/shoppingcart/H22200482A.jpg',
  '/shoppingcart/W231013199.jpg',
  '/shoppingcart/W231013210.jpg',
  '/shoppingcart/HBS01401N-B.jpg',
  '/shoppingcart/VLCSMLORG.jpg',
]

function getRandomBrand() {
  const randomIndex = Math.floor(Math.random() * BRANDSDATA.length)
  return BRANDSDATA[randomIndex]
}

function makeItems(name) {
  const items = []
  for (let i = 0; i < 100; i++) {
    items.push({
      id: `SKU${i}`,
      image: IMAGES[Math.floor(Math.random() * IMAGES.length)],
      name: `${name} ${i}`,
      price: Math.floor(Math.random() * 1000),
      description: `Description for ${name} ${i}`,
      instock: Math.floor(Math.random() * 100),
      brand: getRandomBrand(),
      token: `token-${i}`,
    })
  }

  return new Promise((resolve) => {
    resolve({ data: items })
  })
}

export const state = () => ({
  departments: [],
  categories: [],
  subcategories: [],
  brands: [],
  selected_brands: [],
  search_department: '',
  search_category: '',
  search_subcategory: '',
  countFilteredDep: 0,
  countFilteredCat: 0,
  countFilteredSubcat: 0,
  viewconf: [],
  select_products_by: {
    depto: '0',
    cat: '0',
    scat: '0',
  },
  customers: [],
  isLoading: false,
  breadcrumbs: [],
  isListView: false,
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
  SET_COUNT_FILTERED_DEP(state, count) {
    state.countFilteredDep = count
    localStorage.setItem('lina_countFilteredDep', JSON.stringify(count))
  },
  SET_COUNT_FILTERED_CAT(state, count) {
    state.countFilteredCat = count
    localStorage.setItem('lina_countFilteredCat', JSON.stringify(count))
  },
  SET_COUNT_FILTERED_SUBCAT(state, count) {
    state.countFilteredSubcat = count
    localStorage.setItem('lina_countFilteredSubcat', JSON.stringify(count))
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
  SET_LIST_VIEW(state, isListView) {
    state.isListView = isListView
    localStorage.setItem('lina_isListView', JSON.stringify(isListView))
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

      const isListView =
        JSON.parse(localStorage.getItem('lina_isListView')) || false
      commit('SET_LIST_VIEW', isListView)

      const countFilteredDep =
        JSON.parse(localStorage.getItem('lina_countFilteredDep')) || 0
      commit('SET_COUNT_FILTERED_DEP', countFilteredDep)

      const countFilteredCat =
        JSON.parse(localStorage.getItem('lina_countFilteredCat')) || 0
      commit('SET_COUNT_FILTERED_CAT', countFilteredCat)

      const countFilteredSubcat =
        JSON.parse(localStorage.getItem('lina_countFilteredSubcat')) || 0
      commit('SET_COUNT_FILTERED_SUBCAT', countFilteredSubcat)
    }
  },

  setIsLoading({ commit }) {
    commit('SET_LOADING_STATUS')
  },

  async fetchItems({ commit, state }, payload) {
    commit('SET_LOADING_STATUS')

    let curMutation = ''
    let endpointParams = {}

    switch (payload.name) {
      case 'Department':
      case 'Catalog':
        curMutation = 'SET_DEPARTMENTS'
        endpointParams = { type: 'DEPTO', cia: '01' }
        break
      case 'Category':
        curMutation = 'SET_CATEGORIES'
        endpointParams = {
          type: 'CAT',
          cia: '01',
          dep: state.select_products_by.depto || 'ALL',
        }
        break
      case 'Subcategory':
        curMutation = 'SET_SUBCATEGORIES'
        endpointParams = {
          type: 'SCAT',
          cia: '01',
          dep: state.select_products_by.depto || 'ALL',
          cat: state.select_products_by.cat || 'ALL',
        }
        break
      case 'Product':
        curMutation = 'SET_PRODUCTS'
        endpointParams = { type: 'PROD', cia: '01' }
        break
      case 'Brand':
        curMutation = 'SET_BRANDS'
        endpointParams = { type: 'BRAND', cia: '01' }
        break
      case 'Cliente':
        curMutation = 'SET_CUSTOMERS'
        endpointParams = { type: 'CLI', cia: '01' }
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

  // Función temporal para generar datos de prueba para los productos
  async fetchData({ commit, dispatch }, payload) {
    // commit('SET_LOADING_STATUS')

    // Simulate an API call
    const { data } = await makeItems(payload.name)
    commit('SET_LOADING_STATUS')

    let curMutation = ''

    switch (payload.name) {
      case ('Department', 'Catalog'):
        curMutation = 'SET_DEPARTMENTS'
        break
      case 'Category':
        curMutation = 'SET_CATEGORIES'
        break
      case 'Subcategory':
        curMutation = 'SET_SUBCATEGORIES'
        break
      case 'Product':
        curMutation = 'SET_PRODUCTS'
        break
      case 'Brand':
        curMutation = 'SET_BRANDS'
        break
    }

    commit(curMutation, data)
    commit('SET_LOADING_STATUS')
    return { items: data }
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
  setCountFilteredDep({ commit }, count) {
    commit('SET_COUNT_FILTERED_DEP', count)
  },
  setCountFilteredCat({ commit }, count) {
    commit('SET_COUNT_FILTERED_CAT', count)
  },
  setCountFilteredSubcat({ commit }, count) {
    commit('SET_COUNT_FILTERED_SUBCAT', count)
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
  setListView({ commit }, isListView) {
    commit('SET_LIST_VIEW', isListView)
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

  getCountFilteredDep: (state) => state.countFilteredDep,
  getCountFilteredCat: (state) => state.countFilteredCat,
  getCountFilteredSubcat: (state) => state.countFilteredSubcat,

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

  isListView: (state) => state.isListView,
}
