// store/catalogos.js
// Mock data (to be replaced with API calls)
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

function ensureSettings(catalog) {
  const settings = catalog.settings || {}
  return {
    ...catalog,
    settings: { ...defaultSettings(), ...settings },
  }
}

function ensureTheme(catalog) {
  const theme = catalog.theme || {}
  return {
    ...catalog,
    theme: { ...defaultTheme(), ...theme },
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

function generateToken() {
  return (
    Math.random().toString(36).slice(2, 10) +
    Math.random().toString(36).slice(2, 10)
  )
}

function defaultSettings() {
  return {
    show_price: true,
    show_brand: true,
    show_min_max: true,
    show_sku: true,
    show_description: true,
    show_images: true,
  }
}

function templatePresets() {
  return {
    minimal: {
      template: 'Minimal',
      settings: {
        show_images: true,
        show_brand: true,
        show_sku: true,
        show_description: true,
        show_price: true,
        show_min_max: true,
      },
      default_layout: 'grid_2x4',
      cover: {
        subtitle: 'Selección recomendada',
        logo_url: '',
        hero_url: '',
      },
    },

    fashion: {
      template: 'Fashion',
      settings: {
        show_images: true,
        show_brand: true,
        show_sku: false,
        show_description: false,
        show_price: true,
        show_min_max: false,
      },
      default_layout: 'grid_3x3',
      cover: {
        subtitle: 'Nueva colección',
        logo_url: '',
        hero_url: '',
      },
    },

    promo: {
      template: 'Promo',
      settings: {
        show_images: true,
        show_brand: true,
        show_sku: true,
        show_description: false,
        show_price: true,
        show_min_max: true,
      },
      default_layout: 'list_compact',
      cover: {
        subtitle: 'Ofertas por tiempo limitado',
        logo_url: '',
        hero_url: '',
      },
    },
  }
}

function defaultTheme() {
  return {
    primary: '#1976d2',
    cover_overlay: 'light',
    card_style: 'outlined',
  }
}

function themePresets() {
  return {
    minimal: {
      primary: '#1976d2',
      cover_overlay: 'light',
      card_style: 'outlined',
    },
    fashion: {
      primary: '#111827',
      cover_overlay: 'dark',
      card_style: 'flat',
    },
    promo: {
      primary: '#b91c1c',
      cover_overlay: 'dark',
      card_style: 'outlined',
    },
  }
}
// ************ End of helpers ************

/**
 * Estado:
 * - items: lista de catálogos
 * - currentId: id del catálogo "activo" (editor)
 */
export const state = () => ({
  items: [],
  currentId: null,
  activePageByCatalogId: {},
  pdfJobs: {
    items: {}, // jobId -> job
  },
  toast: { show: false, text: '', type: 'info' },
})

export const getters = {
  all(state) {
    return state.items
  },
  byId: (state) => (id) => {
    const cid = Number(id)
    return state.items.find((c) => c.id === cid) || null
  },
  current(state, getters) {
    if (!state.currentId) return null
    return getters.byId(state.currentId)
  },
  activePageIndex: (state) => (catalogId) => {
    const idx = state.activePageByCatalogId[catalogId]
    return typeof idx === 'number' ? idx : 0
  },
  byToken: (state) => (token) => {
    return state.items.find((c) => c.share_token === token) || null
  },
  pdfJobsActive: (state) =>
    Object.values(state.pdfJobs.items).filter(
      (j) => j.status === 'queued' || j.status === 'running'
    ),
  pdfJobsActiveByCatalog: (state, getters) => (catalogId) =>
    getters.pdfJobsActive.filter((j) => j.catalogId === catalogId),
  pdfJobById: (state) => (jobId) => state.pdfJobs.items[jobId],
  toast: (state) => state.toast,
}

export const mutations = {
  // SET_ITEMS(state, items) {
  //   state.items = (items || [])
  //     .map(ensurePages)
  //     .map(ensureSettings)
  //     .map(ensureTheme)
  // },
  SET_ITEMS(state, items) {
    state.items = items || []
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
  SET_SHARE_TOKEN(state, { catalogId, token }) {
    const cIdx = state.items.findIndex((c) => c.id === catalogId)
    if (cIdx === -1) return

    const catalog = state.items[cIdx]
    const now = new Date().toISOString()

    const next = {
      ...catalog,
      share_token: token,
      updated_at: now,
    }

    state.items.splice(cIdx, 1, next)
    localStorage.setItem('lina_itemsCatalog', JSON.stringify(state.items))
  },

  UPDATE_SETTINGS(state, { catalogId, patch }) {
    const cIdx = state.items.findIndex((c) => c.id === catalogId)
    if (cIdx === -1) return

    const catalog = state.items[cIdx]
    const now = new Date().toISOString()

    const current = catalog.settings || defaultSettings()
    const settings = { ...defaultSettings(), ...current, ...patch }

    const next = {
      ...catalog,
      settings,
      updated_at: now,
    }

    state.items.splice(cIdx, 1, next)
  },

  APPLY_TEMPLATE(state, { catalogId, key, applyToPages }) {
    const cIdx = state.items.findIndex((c) => c.id === catalogId)
    if (cIdx === -1) return

    const presets = templatePresets()
    const preset = presets[key]
    if (!preset) return

    const catalog = state.items[cIdx]
    const pages = Array.isArray(catalog.pages) ? catalog.pages : []
    const now = new Date().toISOString()

    const currentSettings = catalog.settings || {}
    const nextSettings = { ...currentSettings, ...preset.settings }

    const presetTheme = themePresets()[key] || {}
    const currentTheme = catalog.theme || defaultTheme()
    const nextTheme = { ...currentTheme, ...presetTheme }

    const nextPages = pages.map((p) => {
      if (!p) return p

      if (p.layout === 'cover') {
        const cover = p.cover || {
          title: catalog.name || 'Catálogo',
          subtitle: '',
          logo_url: '',
          hero_url: '',
        }

        return {
          ...p,
          cover: {
            ...cover,
            ...preset.cover,
            title: cover.title || catalog.name || 'Catálogo',
          },
        }
      }

      if (applyToPages) {
        return { ...p, layout: preset.default_layout }
      }

      return p
    })

    const next = {
      ...catalog,
      template: preset.template,
      settings: nextSettings,
      pages: nextPages,
      updated_at: now,
      theme: nextTheme,
    }

    state.items.splice(cIdx, 1, next)
  },

  UPDATE_THEME(state, { catalogId, patch }) {
    const cIdx = state.items.findIndex((c) => c.id === catalogId)
    if (cIdx === -1) return

    const catalog = state.items[cIdx]
    const now = new Date().toISOString()

    const current = catalog.theme || defaultTheme()
    const theme = { ...defaultTheme(), ...current, ...patch }

    const next = {
      ...catalog,
      theme,
      updated_at: now,
    }

    state.items.splice(cIdx, 1, next)
  },

  UPSERT_PDF_JOB(state, payload) {
    const prev = state.pdfJobs.items[payload.jobId] || {}
    state.pdfJobs.items = {
      ...state.pdfJobs.items,
      [payload.jobId]: { ...prev, ...payload },
    }
  },

  STOP_PDF_JOB_POLLING(state, jobId) {
    const job = state.pdfJobs.items[jobId]
    if (!job) return

    if (job._timer) clearInterval(job._timer)

    state.pdfJobs.items = {
      ...state.pdfJobs.items,
      [jobId]: { ...job, _timer: null, _polling: false },
    }
  },

  SHOW_TOAST(state, payload) {
    state.toast = { show: true, ...payload }
  },

  HIDE_TOAST(state) {
    state.toast.show = false
  },
}

export const actions = {
  nuxtClientInit({ commit }) {
    if (process.client) {
      const itemsCatalog =
        JSON.parse(localStorage.getItem('lina_itemsCatalog')) || []
      commit('SET_ITEMS', itemsCatalog)
    }
  },

  init({ state, commit }) {
    const itemsCatalog =
      JSON.parse(localStorage.getItem('lina_itemsCatalog')) || []

    if (itemsCatalog.length > 0) commit('SET_ITEMS', itemsCatalog)

    if (state.items.length) return

    const normalized = (mockCatalogos || [])
      .map(ensurePages)
      .map(ensureSettings)
      .map(ensureTheme)

    commit('SET_ITEMS', normalized)
  },

  setItems({ commit }, items) {
    commit('SET_ITEMS', items)
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

    const cover = pages.find((p) => p && p.layout === 'cover') || null
    const contentPages = pages.filter((p) => !(p && p.layout === 'cover'))

    const all = contentPages.reduce((acc, p) => {
      const items = Array.isArray(p.items) ? p.items : []
      return acc.concat(items)
    }, [])

    if (!all.length) {
      // Si no hay items, igual preservamos la portada y al menos 1 página vacía
      const nextPages = []

      if (cover) nextPages.push(cover)

      nextPages.push({
        id: 'page_1',
        name: 'Página 1',
        layout: layout || 'grid_2x4',
        items: [],
      })

      commit('SET_PAGES', { catalogId, pages: nextPages })
      return
    }

    const chunks = chunkArray(all, capacity)

    const distributed = chunks.map((items, idx) => {
      const n = idx + 1
      return {
        id: `page_${n}`,
        name: `Página ${n}`,
        layout: layout || 'grid_2x4',
        items,
      }
    })

    const nextPages = cover ? [cover, ...distributed] : distributed

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

  ensureShareToken({ getters, commit }, { catalogId }) {
    const catalog = getters.byId(catalogId)
    if (!catalog) return ''

    if (catalog.share_token) return catalog.share_token

    const token = generateToken()
    commit('SET_SHARE_TOKEN', { catalogId, token })
    return token
  },

  regenerateShareToken({ commit }, { catalogId }) {
    const token = generateToken()
    commit('SET_SHARE_TOKEN', { catalogId, token })
    return token
  },

  updateSettings({ commit }, { catalogId, patch }) {
    commit('UPDATE_SETTINGS', { catalogId, patch })
  },

  applyTemplate({ commit }, { catalogId, key, applyToPages }) {
    commit('APPLY_TEMPLATE', { catalogId, key, applyToPages })
  },

  updateTheme({ commit }, { catalogId, patch }) {
    commit('UPDATE_THEME', { catalogId, patch })
  },

  async exportPdfStart({ commit, dispatch }, { catalogId, totalPages }) {
    // POST export
    const { data } = await this.$axios.post(
      `catalog/api/catalogs/${catalogId}/export-pdf/`
    )

    const jobId = data.job_id

    commit('UPSERT_PDF_JOB', {
      jobId,
      catalogId,
      status: data.status || 'queued',
      progress: 0,
      totalPages: totalPages || null,
      downloadUrl: null,
      error: '',
      startedAt: Date.now(),
      finishedAt: null,
      isEstimated: true,
      _polling: false,
      _timer: null,
    })

    dispatch('exportPdfPoll', { jobId })
    return jobId
  },

  exportPdfEstimateProgress({ state, commit }, { jobId }) {
    const job = state.pdfJobs.items[jobId]
    if (!job) return
    if (job.status === 'success' || job.status === 'failed') return

    const elapsedSec = (Date.now() - (job.startedAt || Date.now())) / 1000

    // Curva suave: sube rápido al inicio, se frena cerca de 90%
    const raw = 100 * (1 - Math.exp(-elapsedSec / 8))
    const capped = Math.min(raw, 90)

    const next = Math.max(job.progress || 0, Math.floor(capped))
    commit('UPSERT_PDF_JOB', { jobId, progress: next })
  },

  async exportPdfPoll({ state, commit, dispatch }, { jobId }) {
    const job = state.pdfJobs.items[jobId]
    if (!job) return
    if (job._polling) return

    commit('UPSERT_PDF_JOB', { jobId, _polling: true })

    const tick = async () => {
      try {
        const { data } = await this.$axios.get(`catalog/api/pdf-jobs/${jobId}/`)

        commit('UPSERT_PDF_JOB', {
          jobId,
          status: data.status,
          downloadUrl: data.download_url || null,
          error: data.error || '',
        })

        dispatch('exportPdfEstimateProgress', { jobId })

        if (data.status === 'success' && data.download_url) {
          commit('UPSERT_PDF_JOB', {
            jobId,
            progress: 100,
            finishedAt: Date.now(),
          })

          commit('STOP_PDF_JOB_POLLING', jobId)

          dispatch('uiToast', {
            type: 'success',
            text: 'Tu PDF está listo. Descargando…',
          })
          dispatch('exportPdfDownload', { jobId })
        }

        if (data.status === 'failed') {
          commit('STOP_PDF_JOB_POLLING', jobId)
          dispatch('uiToast', {
            type: 'error',
            text: `Falló la generación del PDF: ${
              state.pdfJobs.items[jobId]?.error || 'error desconocido'
            }`,
          })
        }
      } catch (e) {
        // No rompemos el polling por fallos transitorios
        dispatch('exportPdfEstimateProgress', { jobId })
      }
    }

    const timer = setInterval(tick, 1500)
    commit('UPSERT_PDF_JOB', { jobId, _timer: timer })

    await tick()
  },

  exportPdfStopPolling({ commit }, { jobId }) {
    commit('STOP_PDF_JOB_POLLING', jobId)
  },

  exportPdfDownload_AuthCookie({ state }, { jobId }) {
    const job = state.pdfJobs.items[jobId]
    if (!job || !job.downloadUrl) return

    // Si tu backend requiere auth por cookie, esto funciona bien.
    // Si dependes de Authorization header, usa descarga por blob (te la doy si la necesitas).
    window.location.href = job.downloadUrl
  },

  async exportPdfDownload({ state, commit, dispatch }, { jobId }) {
    const job = state.pdfJobs.items[jobId]
    if (!job || !job.downloadUrl) return

    try {
      // 1) Descarga binaria con axios (mantiene Authorization header vía interceptor)
      console.log('Iniciando descarga de PDF desde', job.downloadUrl)
      const res = await this.$axios.request({
        url: job.downloadUrl,
        method: 'GET',
        responseType: 'blob',
        // Opcional: si el backend tarda en preparar stream
        timeout: 120000,
      })

      const blob = new Blob([res.data], { type: 'application/pdf' })

      // 2) Determina filename (ideal: desde Content-Disposition)
      const cd =
        (res.headers &&
          (res.headers['content-disposition'] ||
            res.headers['Content-Disposition'])) ||
        ''
      const filename =
        extractFilenameFromContentDisposition(cd) ||
        `catalogo-${job.catalogId}.pdf`

      // 3) Fuerza descarga en el navegador
      const objectUrl = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = objectUrl
      a.download = filename
      document.body.appendChild(a)
      a.click()
      a.remove()
      window.URL.revokeObjectURL(objectUrl)

      // (Opcional) marca job como descargado
      commit('UPSERT_PDF_JOB', { jobId, downloadedAt: Date.now() })
    } catch (e) {
      dispatch('uiToast', {
        type: 'error',
        text: 'No se pudo descargar el PDF.',
      })
    }

    // Helper local (para no depender de libs)
    function extractFilenameFromContentDisposition(contentDisposition) {
      if (!contentDisposition) return null

      // filename*=UTF-8''...
      const m1 = contentDisposition.match(/filename\*\s*=\s*UTF-8''([^;]+)/i)
      if (m1 && m1[1])
        return decodeURIComponent(m1[1].trim().replace(/["']/g, ''))

      // filename="..."
      const m2 = contentDisposition.match(/filename\s*=\s*("?)([^";]+)\1/i)
      if (m2 && m2[2]) return m2[2].trim()

      return null
    }
  },

  uiToast({ commit }, payload) {
    commit('SHOW_TOAST', payload)
    setTimeout(() => commit('HIDE_TOAST'), 4000)
  },
}
