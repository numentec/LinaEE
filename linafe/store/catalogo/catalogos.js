// store/catalogos.js
import { mockCatalogos } from '~/mock/catalogos'

export const namespaced = true

// ************ Actions and mutations helpers ************
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

function chunkArray(arr, size) {
  const out = []
  for (let i = 0; i < arr.length; i += size) {
    out.push(arr.slice(i, i + size))
  }
  return out
}

function generateId() {
  // Suficiente para el MVP. Luego lo reemplazas por ULID/ID del backend.
  return `cat_${Date.now().toString(36)}_${Math.random()
    .toString(36)
    .slice(2, 7)}`
}

function nextPageNumber(pages) {
  const nums = (pages || [])
    .map((p) => String(p.id || ''))
    .map((id) => {
      const m = id.match(/page_(\d+)/)
      return m ? Number(m[1]) : 0
    })

  const max = nums.length ? Math.max(...nums) : 0
  return max + 1
}

function clonePage(page, newId, newName) {
  const items = Array.isArray(page.items) ? page.items : []

  return {
    id: newId,
    name: newName,
    layout: page.layout || 'grid_2x4',
    items: items.map((x) => ({ ...x })),
  }
}

/**
 * Estado:
 * - items: lista de catálogos
 * - currentId: id del catálogo "activo" (editor)
 */
export const state = () => ({
  items: [],
  currentId: null,
  activePageByCatalogId: {},
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
  activePageIndex: (state) => (catalogId) => {
    const idx = state.activePageByCatalogId[catalogId]
    return typeof idx === 'number' ? idx : 0
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
  SET_PAGES(state, { catalogId, pages }) {
    const cIdx = state.items.findIndex((c) => c.id === catalogId)
    if (cIdx === -1) return

    const catalog = state.items[cIdx]
    const now = new Date().toISOString()

    const next = {
      ...catalog,
      pages,
      pages_count: pages.length,
      updated_at: now,
    }

    state.items.splice(cIdx, 1, next)
  },
  SET_ACTIVE_PAGE_INDEX(state, { catalogId, pageIndex }) {
    state.activePageByCatalogId = {
      ...state.activePageByCatalogId,
      [catalogId]: pageIndex,
    }
  },
  SET_PAGE_LAYOUT(state, { catalogId, pageId, layout }) {
    const cIdx = state.items.findIndex((c) => c.id === catalogId)
    if (cIdx === -1) return

    const catalog = state.items[cIdx]
    const pages = Array.isArray(catalog.pages) ? catalog.pages : []
    const pIdx = pages.findIndex((p) => p.id === pageId)
    if (pIdx === -1) return

    const now = new Date().toISOString()

    const nextPages = pages.map((p) => {
      if (p.id !== pageId) return p
      return { ...p, layout }
    })

    const next = {
      ...catalog,
      pages: nextPages,
      updated_at: now,
    }

    state.items.splice(cIdx, 1, next)
  },

  ADD_EMPTY_PAGE(state, { catalogId, layout }) {
    const cIdx = state.items.findIndex((c) => c.id === catalogId)
    if (cIdx === -1) return

    const catalog = state.items[cIdx]
    const pages = Array.isArray(catalog.pages) ? catalog.pages : []

    const n = nextPageNumber(pages)
    const id = `page_${n}`

    const page = {
      id,
      name: `Página ${n}`,
      layout: layout || 'grid_2x4',
      items: [],
    }

    const now = new Date().toISOString()

    const next = {
      ...catalog,
      pages: [...pages, page],
      pages_count: (catalog.pages_count || pages.length) + 1,
      updated_at: now,
    }

    state.items.splice(cIdx, 1, next)
  },

  DUPLICATE_PAGE(state, { catalogId, pageIndex }) {
    const cIdx = state.items.findIndex((c) => c.id === catalogId)
    if (cIdx === -1) return

    const catalog = state.items[cIdx]
    const pages = Array.isArray(catalog.pages) ? catalog.pages : []
    if (!pages.length) return
    if (pageIndex < 0 || pageIndex >= pages.length) return

    const src = pages[pageIndex]
    const n = pages.length + 1
    const newId = `page_${n}`
    const newName = `${src.name || `Página ${pageIndex + 1}`} (copia)`

    const copy = clonePage(src, newId, newName)

    const nextPages = [
      ...pages.slice(0, pageIndex + 1),
      copy,
      ...pages.slice(pageIndex + 1),
    ]

    const now = new Date().toISOString()

    const next = {
      ...catalog,
      pages: nextPages,
      pages_count: nextPages.length,
      updated_at: now,
    }

    state.items.splice(cIdx, 1, next)

    const active = state.activePageByCatalogId[catalogId]
    const isNum = typeof active === 'number'

    if (isNum && active > pageIndex) {
      state.activePageByCatalogId = {
        ...state.activePageByCatalogId,
        [catalogId]: active + 1,
      }
    }
  },

  DELETE_PAGE(state, { catalogId, pageIndex }) {
    const cIdx = state.items.findIndex((c) => c.id === catalogId)
    if (cIdx === -1) return

    const catalog = state.items[cIdx]
    const pages = Array.isArray(catalog.pages) ? catalog.pages : []
    if (!pages.length) return
    if (pageIndex < 0 || pageIndex >= pages.length) return

    let nextPages = pages.filter((_, idx) => idx !== pageIndex)

    if (!nextPages.length) {
      nextPages = [
        {
          id: 'page_1',
          name: 'Página 1',
          layout: 'grid_2x4',
          items: [],
        },
      ]
    }

    const now = new Date().toISOString()

    const next = {
      ...catalog,
      pages: nextPages,
      pages_count: nextPages.length,
      updated_at: now,
    }

    state.items.splice(cIdx, 1, next)

    const active = state.activePageByCatalogId[catalogId]
    const isNum = typeof active === 'number'
    if (!isNum) return

    let nextActive = active

    if (active === pageIndex) {
      nextActive = Math.max(0, pageIndex - 1)
    } else if (active > pageIndex) {
      nextActive = active - 1
    }

    if (nextActive >= nextPages.length) nextActive = nextPages.length - 1

    state.activePageByCatalogId = {
      ...state.activePageByCatalogId,
      [catalogId]: nextActive,
    }
  },

  MOVE_PAGE(state, { catalogId, fromIndex, toIndex }) {
    const cIdx = state.items.findIndex((c) => c.id === catalogId)
    if (cIdx === -1) return

    const catalog = state.items[cIdx]
    const pages = Array.isArray(catalog.pages) ? catalog.pages : []
    if (!pages.length) return
    if (fromIndex < 0 || fromIndex >= pages.length) return
    if (toIndex < 0 || toIndex >= pages.length) return
    if (fromIndex === toIndex) return

    const nextPages = [...pages]
    const tmp = nextPages[fromIndex]
    nextPages[fromIndex] = nextPages[toIndex]
    nextPages[toIndex] = tmp

    const now = new Date().toISOString()

    const next = {
      ...catalog,
      pages: nextPages,
      pages_count: nextPages.length,
      updated_at: now,
    }

    state.items.splice(cIdx, 1, next)

    const active = state.activePageByCatalogId[catalogId]
    const isNum = typeof active === 'number'
    if (!isNum) return

    let nextActive = active

    if (active === fromIndex) nextActive = toIndex
    else if (active === toIndex) nextActive = fromIndex

    state.activePageByCatalogId = {
      ...state.activePageByCatalogId,
      [catalogId]: nextActive,
    }
  },

  RENAME_PAGE(state, { catalogId, pageId, name }) {
    const cIdx = state.items.findIndex((c) => c.id === catalogId)
    if (cIdx === -1) return

    const catalog = state.items[cIdx]
    const pages = Array.isArray(catalog.pages) ? catalog.pages : []
    const pIdx = pages.findIndex((p) => p.id === pageId)
    if (pIdx === -1) return

    const now = new Date().toISOString()

    const nextPages = pages.map((p) => {
      if (p.id !== pageId) return p
      return { ...p, name }
    })

    const next = {
      ...catalog,
      pages: nextPages,
      updated_at: now,
    }

    state.items.splice(cIdx, 1, next)
  },

  ENSURE_COVER_PAGE(state, { catalogId }) {
    const cIdx = state.items.findIndex((c) => c.id === catalogId)
    if (cIdx === -1) return

    const catalog = state.items[cIdx]
    const pages = Array.isArray(catalog.pages) ? catalog.pages : []

    const hasCover = pages.some((p) => p.id === 'cover')
    if (hasCover) return

    const cover = {
      id: 'cover',
      name: 'Portada',
      layout: 'cover',
      items: [],
      cover: {
        title: catalog.name || 'Catálogo',
        subtitle: '',
        logo_url: '',
        hero_url: '',
      },
    }

    const nextPages = [cover, ...pages]

    const now = new Date().toISOString()

    const next = {
      ...catalog,
      pages: nextPages,
      pages_count: nextPages.length,
      updated_at: now,
    }

    state.items.splice(cIdx, 1, next)

    const active = state.activePageByCatalogId[catalogId]
    const isNum = typeof active === 'number'

    if (isNum) {
      state.activePageByCatalogId = {
        ...state.activePageByCatalogId,
        [catalogId]: active + 1,
      }
    }
  },

  UPDATE_COVER(state, { catalogId, patch }) {
    const cIdx = state.items.findIndex((c) => c.id === catalogId)
    if (cIdx === -1) return

    const catalog = state.items[cIdx]
    const pages = Array.isArray(catalog.pages) ? catalog.pages : []

    const nextPages = pages.map((p) => {
      if (p.id !== 'cover') return p

      const cover = p.cover || {
        title: catalog.name || 'Catálogo',
        subtitle: '',
        logo_url: '',
        hero_url: '',
      }

      return {
        ...p,
        cover: { ...cover, ...patch },
      }
    })

    const now = new Date().toISOString()

    const next = {
      ...catalog,
      pages: nextPages,
      updated_at: now,
    }

    state.items.splice(cIdx, 1, next)
  },
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

  autoDistribute({ getters, commit }, { catalogId, layout, capacity }) {
    const catalog = getters.byId(catalogId)
    if (!catalog) return

    const pages = Array.isArray(catalog.pages) ? catalog.pages : []
    const all = pages.reduce((acc, p) => {
      const items = Array.isArray(p.items) ? p.items : []
      return acc.concat(items)
    }, [])

    if (!all.length) return

    const chunks = chunkArray(all, capacity)

    const nextPages = chunks.map((items, idx) => {
      const n = idx + 1
      return {
        id: `page_${n}`,
        name: `Página ${n}`,
        layout,
        items,
      }
    })

    commit('SET_PAGES', { catalogId, pages: nextPages })
  },

  setActivePage({ commit }, { catalogId, pageIndex }) {
    commit('SET_ACTIVE_PAGE_INDEX', { catalogId, pageIndex })
  },

  setPageLayout({ commit }, { catalogId, pageId, layout }) {
    commit('SET_PAGE_LAYOUT', { catalogId, pageId, layout })
  },

  addEmptyPage({ getters, commit }, { catalogId, layout }) {
    const catalog = getters.byId(catalogId)
    if (!catalog) return 0

    const pages = Array.isArray(catalog.pages) ? catalog.pages : []
    const nextIndex = pages.length

    commit('ADD_EMPTY_PAGE', { catalogId, layout })

    return nextIndex
  },

  duplicatePage({ commit }, { catalogId, pageIndex }) {
    commit('DUPLICATE_PAGE', { catalogId, pageIndex })
  },

  deletePage({ commit }, { catalogId, pageIndex }) {
    commit('DELETE_PAGE', { catalogId, pageIndex })
  },

  movePage({ commit }, { catalogId, fromIndex, toIndex }) {
    commit('MOVE_PAGE', { catalogId, fromIndex, toIndex })
  },

  renamePage({ commit }, { catalogId, pageId, name }) {
    commit('RENAME_PAGE', { catalogId, pageId, name })
  },

  ensureCoverPage({ commit }, { catalogId }) {
    commit('ENSURE_COVER_PAGE', { catalogId })
  },

  updateCover({ commit }, { catalogId, patch }) {
    commit('UPDATE_COVER', { catalogId, patch })
  },
}
