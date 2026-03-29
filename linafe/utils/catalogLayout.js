export function countVisibleInfoLines(settings = {}) {
  let lines = 0

  if (settings.show_brand) lines += 1
  if (settings.show_sku) lines += 1
  if (settings.show_description) lines += 2
  if (settings.show_price) lines += 1
  if (settings.show_min_max) lines += 1

  return lines
}

export function normalizeAutoGridLayout(layout) {
  if (layout === 'grid_3') return 'grid_3'
  return 'grid_2'
}

export function computeCatalogLayout({
  layout,
  orientation = 'portrait',
  settings = {},
  pageWidth = 700,
  surface = 'canvas', // 'canvas' o 'pdf'
}) {
  if (layout === 'hero_1') {
    return {
      layout,
      columns: 1,
      rowsPerPage: 1,
      capacity: 1,
      pageWidth,
      pageHeight: Math.round(
        pageWidth * (orientation === 'landscape' ? 8.5 / 11 : 11 / 8.5)
      ),
      contentWidth: 0,
      contentHeight: 0,
      cardWidth: 0,
      cardHeight: 0,
    }
  }

  if (layout === 'hero_2') {
    return {
      layout,
      columns: 1,
      rowsPerPage: 2,
      capacity: 2,
      pageWidth,
      pageHeight: Math.round(
        pageWidth * (orientation === 'landscape' ? 8.5 / 11 : 11 / 8.5)
      ),
      contentWidth: 0,
      contentHeight: 0,
      cardWidth: 0,
      cardHeight: 0,
    }
  }

  if (layout === 'list_compact') {
    return {
      layout,
      columns: 1,
      rowsPerPage: 6,
      capacity: 6,
      pageWidth,
      pageHeight: Math.round(
        pageWidth * (orientation === 'landscape' ? 8.5 / 11 : 11 / 8.5)
      ),
      contentWidth: 0,
      contentHeight: 0,
      cardWidth: 0,
      cardHeight: 0,
    }
  }

  const normalizedLayout = normalizeAutoGridLayout(layout)
  const isLandscape = orientation === 'landscape'

  const pageHeight = Math.round(pageWidth * (isLandscape ? 8.5 / 11 : 11 / 8.5))

  // Ajustes calibrados visualmente para alinear canvas y PDF
  const landscapeWidthCompensation = isLandscape
    ? surface === 'pdf'
      ? 200
      : 96
    : 0

  // const horizontalPadding = orientation === 'landscape' ? 56 : 48
  const horizontalPadding = 48
  const verticalPadding = 40
  const columnGap = 8
  const rowGap = 8

  const contentWidth = pageWidth - horizontalPadding * 2
  const contentHeight = pageHeight - verticalPadding * 2

  const columns = normalizedLayout === 'grid_3' ? 3 : 2

  const cardWidth =
    columns > 1
      ? Math.floor((contentWidth - columnGap * (columns - 1)) / columns)
      : contentWidth

  const visibleInfoLines = countVisibleInfoLines(settings)
  const imageBlockHeight = settings.show_images ? 88 : 0
  const baseTextHeight = 24
  const lineHeight = 18
  const cardContentPadding = 10

  /* Ajuste visual para eliminar espacio muerto al final de la card.
     Valor calibrado empíricamente para mantener consistencia en grid. */
  // const cardBottomSlackCompensation = 14
  const cardBottomSlackCompensation = columns === 3 ? 16 : 14

  const textHeight = baseTextHeight + visibleInfoLines * lineHeight

  const rawCardHeight =
    Math.max(settings.show_images ? imageBlockHeight : 56, textHeight) +
    cardContentPadding

  const cardHeight = Math.max(56, rawCardHeight - cardBottomSlackCompensation)

  const rowsPerPage = Math.max(
    1,
    Math.floor((contentHeight + rowGap) / (cardHeight + rowGap))
  )

  return {
    layout: normalizedLayout,
    pageWidth,
    effectivePageWidth: pageWidth + landscapeWidthCompensation,
    pageHeight,
    contentWidth,
    contentHeight,
    columns,
    cardWidth,
    cardHeight,
    rowsPerPage,
    capacity: columns * rowsPerPage,
    visibleInfoLines,
    horizontalPadding,
    verticalPadding,
    columnGap,
    rowGap,
    landscapeWidthCompensation,
  }
}
