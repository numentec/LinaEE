const STORAGE_KEY = 'linaee.pdfJobs.v1'

function safeParse(json, fallback) {
  try {
    return JSON.parse(json)
  } catch (e) {
    return fallback
  }
}

function stripRuntimeFields(items) {
  const out = {}
  for (const [jobId, job] of Object.entries(items || {})) {
    // Quitamos timers/flags no serializables
    const { _timer, _polling, ...rest } = job || {}
    out[jobId] = rest
  }
  return out
}

export default ({ store }) => {
  // ================
  // 1) REHYDRATE
  // ================
  const raw = localStorage.getItem(STORAGE_KEY)
  const saved = safeParse(raw, null)

  if (saved && typeof saved === 'object') {
    store.commit('catalogo/catalogos/LOAD_PDF_JOBS_FROM_STORAGE', saved)

    // Limpieza opcional (24h)
    store.commit('catalogo/catalogos/CLEANUP_OLD_PDF_JOBS', { maxAgeHours: 24 })
  }

  // ================
  // 2) RESUME POLLING
  // ================
  const activeJobs = store.getters['catalogo/catalogos/pdfJobsActive']
  for (const j of activeJobs) {
    store.dispatch('catalogo/catalogos/exportPdfPoll', { jobId: j.jobId })
  }

  // ================
  // 3) SI YA ESTÁ LISTO Y NO DESCARGADO -> NOTIF + DESCARGA
  // (esto cubre el caso: job terminó mientras el usuario estaba fuera)
  // ================
  const all = Object.values(store.state.catalogo.catalogos.pdfJobs.items || {})
  const readyNotDownloaded = all.filter(
    (j) => j && j.status === 'success' && j.downloadUrl && !j.downloadedAt
  )

  for (const j of readyNotDownloaded) {
    store.dispatch('catalogo/catalogos/uiToast', {
      type: 'success',
      text: 'Tu PDF ya estaba listo.',
      actionText: 'Descargar ahora',
      actionJobId: j.jobId,
    })
    // store.dispatch('catalogo/catalogos/exportPdfDownload', { jobId: j.jobId })
  }

  // ================
  // 4) PERSIST ON MUTATIONS (debounced)
  // ================
  let t = null
  store.subscribe((mutation, state) => {
    // Persistimos solo cuando toca pdfJobs o toast (toast no hace falta, pero no molesta)
    if (!mutation.type.startsWith('catalogo/catalogos/')) return

    const touchesPdfJobs =
      mutation.type.includes('PDF_JOB') ||
      mutation.type.includes('LOAD_PDF_JOBS_FROM_STORAGE') ||
      mutation.type.includes('CLEANUP_OLD_PDF_JOBS')

    if (!touchesPdfJobs) return

    if (t) clearTimeout(t)
    t = setTimeout(() => {
      const items = state.catalogo.catalogos.pdfJobs.items
      const serializable = stripRuntimeFields(items)
      localStorage.setItem(STORAGE_KEY, JSON.stringify(serializable))
    }, 250)
  })
}
