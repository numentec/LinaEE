// store/catalogos.js
import { mockCatalogos } from '~/mock/catalogos'

function ensurePages(catalog) {
  if (Array.isArray(catalog.pages) && catalog.pages.length) return catalog

  const pages = [
    {
      id: 'page_1',
      name: 'Página 1',
      layout: 'grid_2x4',
      items: [],
    },
  ]

  return {
    ...catalog,
    pages,
    pages_count: catalog.pages_count || 1,
  }
}

/**
 * Estado:
 * - items: lista de catálogos
 * - currentId: id del catálogo "activo" (editor)
 */

export const namespaced = true

export const state = () => ({
  items: [],
  currentId: null,
})

export const getters = {
  all(state) {
    return state.items
  },
  byId: (state) => (id) => {
    return state.items.find((c) => c.id === id) || null
  },
  current(state, getters) {
    if (!state.currentId) return null
    return getters.byId(state.currentId)
  },
}

export const mutations = {
  SET_ITEMS(state, items) {
    state.items = (items || []).map(ensurePages)
  },
  ADD_ITEM(state, item) {
    state.items.unshift(item)
  },
  SET_CURRENT_ID(state, id) {
    state.currentId = id
  },
  UPDATE_ITEM(state, { id, patch }) {
    const idx = state.items.findIndex((c) => c.id === id)
    if (idx === -1) return
    state.items.splice(idx, 1, { ...state.items[idx], ...patch })
  },
  ADD_PRODUCTS_TO_PAGE(state, { catalogId, pageId, products }) {
    const cIdx = state.items.findIndex((c) => c.id === catalogId)
    if (cIdx === -1) return

    const catalog = state.items[cIdx]
    const pIdx = (catalog.pages || []).findIndex((p) => p.id === pageId)
    if (pIdx === -1) return

    const page = catalog.pages[pIdx]
    const current = Array.isArray(page.items) ? page.items : []

    const now = new Date().toISOString()

    const merged = [...current, ...products]

    const updatedCatalog = {
      ...catalog,
      pages: catalog.pages.map((p) => {
        if (p.id !== pageId) return p
        return { ...p, items: merged }
      }),
      updated_at: now,
    }

    state.items.splice(cIdx, 1, updatedCatalog)
  },
}

function generateId() {
  // Suficiente para el MVP. Luego lo reemplazas por ULID/ID del backend.
  return `cat_${Date.now().toString(36)}_${Math.random()
    .toString(36)
    .slice(2, 7)}`
}

export const actions = {
  init({ state, commit }) {
    if (state.items.length) return

    const normalized = (mockCatalogos || []).map(ensurePages)

    commit('SET_ITEMS', normalized)
  },

  createCatalog({ commit }, { name, template, orientation, companyId }) {
    const now = new Date().toISOString()

    const item = {
      id: generateId(),
      company_id: companyId || 'cia_01',
      name: name || 'Nuevo catálogo',
      template: template || 'minimal',
      orientation: orientation || 'portrait',
      status: 'draft',
      pages_count: 1,
      updated_at: now,
      // En el MVP guardamos páginas “dummy” para el editor
      pages: [
        {
          id: 'page_1',
          name: 'Página 1',
          layout: 'grid_2x4', // luego lo hacemos real
          items: [],
        },
      ],
    }

    commit('ADD_ITEM', item)
    commit('SET_CURRENT_ID', item.id)
    return item
  },

  setCurrent({ commit }, id) {
    commit('SET_CURRENT_ID', id)
  },

  addProductsToPage({ commit }, { catalogId, pageId, products }) {
    commit('ADD_PRODUCTS_TO_PAGE', { catalogId, pageId, products })
  },
}
