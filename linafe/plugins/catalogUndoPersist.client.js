const STORAGE_KEY = 'linaee.catalogUndoHistory.v1'

function safeParse(json, fallback) {
  try {
    return JSON.parse(json)
  } catch (e) {
    return fallback
  }
}

function normalizeHistoryMap(input) {
  const src = input && typeof input === 'object' ? input : {}
  const out = {}

  Object.entries(src).forEach(([catalogId, value]) => {
    const item = value && typeof value === 'object' ? value : {}

    const past = Array.isArray(item.past) ? item.past.filter(Boolean) : []
    const future = Array.isArray(item.future) ? item.future.filter(Boolean) : []

    if (!past.length && !future.length) return

    out[String(catalogId)] = {
      past,
      future,
    }
  })

  return out
}

export default ({ store }) => {
  const raw = localStorage.getItem(STORAGE_KEY)
  const saved = safeParse(raw, {})
  const normalized = normalizeHistoryMap(saved)

  store.commit(
    'catalogo/catalogos/LOAD_CATALOG_UNDO_HISTORY_FROM_STORAGE',
    normalized
  )

  let t = null
  store.subscribe((mutation, state) => {
    if (!mutation.type.startsWith('catalogo/catalogos/')) return

    if (mutation.type !== 'catalogo/catalogos/SET_CATALOG_UNDO_HISTORY') return

    if (t) clearTimeout(t)
    t = setTimeout(() => {
      const all =
        state.catalogo &&
        state.catalogo.catalogos &&
        state.catalogo.catalogos.undoHistoryByCatalogId
          ? state.catalogo.catalogos.undoHistoryByCatalogId
          : {}

      localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify(normalizeHistoryMap(all))
      )
    }, 200)
  })
}
