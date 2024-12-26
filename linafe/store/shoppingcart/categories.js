// import CustomStore from 'devextreme/data/custom_store'
export const namespaced = true

const BRANDSDATA = ['Brand 1', 'Brand 2', 'Brand 3', 'Brand 4', 'Brand 5']
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

function getRandomSubarray(arr, size) {
  const shuffled = arr.slice(0)
  let i = arr.length
  let temp, index
  while (i--) {
    index = Math.floor((i + 1) * Math.random())
    temp = shuffled[index]
    shuffled[index] = shuffled[i]
    shuffled[i] = temp
  }
  return shuffled.slice(0, size)
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
      brands: getRandomSubarray(BRANDSDATA, 3),
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
  products: [],
  selected_brands: [],
  search_department: '',
  search_category: '',
  search_subcategory: '',
  search_product: '',
})

export const mutations = {
  SET_DEPARTMENTS(state, departments) {
    state.departments = departments
  },
  SET_CATEGORIES(state, categories) {
    state.categories = categories
  },
  SET_SUBCATEGORIES(state, subcategories) {
    state.subcategories = subcategories
  },
  SET_PRODUCTS(state, products) {
    state.products = products
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
  },
  SET_SEARCH_DEPARTMENT(state, department) {
    state.search_department = department
  },
  SET_SEARCH_CATEGORY(state, category) {
    state.search_category = category
  },
  SET_SEARCH_SUBCATEGORY(state, subcategory) {
    state.search_subcategory = subcategory
  },
  SET_SEARCH_PRODUCT(state, search) {
    state.search_product = search
  },
}

export const actions = {
  async fetchItems({ commit, dispatch }, payload) {
    // commit('SET_LOADING_STATUS')

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
    }

    return await this.$axios
      .get('shoppingcart/catsbrands/', {
        params: endpointParams,
      })
      .then((response) => {
        commit(curMutation, response.data)
        // commit('SET_LOADING_STATUS')
        return { items: response.data }
      })
  },

  // Función temporal para generar datos de prueba para los productos
  async fetchData({ commit, dispatch }, payload) {
    // commit('SET_LOADING_STATUS')

    // Simulate an API call
    const { data } = await makeItems(payload.name)

    switch (payload.name) {
      case 'Department':
        commit('SET_DEPARTMENTS', data)
        break
      case 'Category':
        commit('SET_CATEGORIES', data)
        break
      case 'Subcategory':
        commit('SET_SUBCATEGORIES', data)
        break
      case 'Product':
        commit('SET_PRODUCTS', data)
        break
    }

    return { items: data }
  },

  addCategory({ commit }, category) {
    commit('ADD_CATEGORY', category)
  },
  removeCategory({ commit }, categoryId) {
    commit('REMOVE_CATEGORY', categoryId)
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
  setSearchProduct({ commit }, search) {
    commit('SET_SEARCH_PRODUCT', search)
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

  getSelectedBrands: (state) => state.selected_brands,
  getSearchDepartment: (state) => state.search_department,
  getSearchCategory: (state) => state.search_category,
  getSearchSubcategory: (state) => state.search_subcategory,
  getSearchProduct: (state) => state.search_product,
}
