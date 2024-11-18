// import CustomStore from 'devextreme/data/custom_store'
export const namespaced = true

export const state = () => ({
  categories: [],
  selected_brands: [],
  search_department: '',
  search_category: '',
  search_subcategory: '',
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
}

export const actions = {
  fetchCategories({ commit }) {
    // Simulate an API call
    const categories = [
      { id: 1, name: 'Electronics' },
      { id: 2, name: 'Books' },
      { id: 3, name: 'Clothing' },
    ]
    commit('SET_CATEGORIES', categories)
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
}

export const getters = {
  allCategories: (state) => state.categories,
  categoryById: (state) => (id) =>
    state.categories.find((category) => category.id === id),
  getSelectedBrands: (state) => state.selected_brands,
  getSearchDepartment: (state) => state.search_department,
  getSearchCategory: (state) => state.search_category,
  getSearchSubcategory: (state) => state.search_subcategory,
}
