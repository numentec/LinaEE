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

function makeItems(name, link) {
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
      link,
    })
  }

  return new Promise((resolve) => {
    resolve({ data: items })
  })
}

export const state = () => ({
  categories: [],
  selected_brands: [],
  search_department: '',
  search_category: '',
  search_subcategory: '',
  search_product: '',
})

export const mutations = {
  SET_CATEGORIES(state, categories) {
    state.categories = categories
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
  async fetchItems({ commit }, payload) {
    // Simulate an API call
    const { data } = await makeItems(payload.name, payload.link)

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
  allCategories: (state) => state.categories,
  categoryById: (state) => (id) =>
    state.categories.find((category) => category.id === id),
  getSelectedBrands: (state) => state.selected_brands,
  getSearchDepartment: (state) => state.search_department,
  getSearchCategory: (state) => state.search_category,
  getSearchSubcategory: (state) => state.search_subcategory,
  getSearchProduct: (state) => state.search_product,
}
