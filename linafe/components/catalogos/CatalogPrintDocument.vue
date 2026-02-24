<template>
  <div v-if="doc" class="print-document">
    <section
      v-for="(page, i) in doc.pages"
      :key="page.id || i"
      class="print-page"
      :class="pageClass(page)"
    >
      <!-- HEADER -->
      <div v-if="page.layout !== 'cover'" class="page-header">
        <span class="header-title">{{ doc.name }}</span>
        <span class="header-page">Página {{ pageNumber(i) }}</span>
      </div>

      <!-- COVER -->
      <div v-if="page.layout == 'cover'" class="cover">
        <div v-if="page.cover && page.cover.hero_url" class="cover-hero">
          <img class="cover-hero-img" :src="page.cover.hero_url" alt="" />
          <div class="cover-overlay" :class="coverOverlayClass"></div>
        </div>

        <div class="cover-content">
          <div class="cover-title">
            {{ (page.cover && page.cover.title) || doc.name }}
          </div>

          <div v-if="page.cover && page.cover.subtitle" class="cover-subtitle">
            {{ page.cover.subtitle }}
          </div>

          <img
            v-if="page.cover && page.cover.logo_url"
            class="cover-logo"
            :src="page.cover.logo_url"
            alt=""
          />
        </div>
      </div>

      <!-- GRID -->
      <div
        v-else-if="page.layout && page.layout.startsWith('grid')"
        class="content"
        :class="pageClass(page)"
      >
        <div
          v-for="item in page.items"
          :key="item.product_id || item.sku"
          class="product-card"
          :class="cardStyleClass"
        >
          <div
            v-if="showImages"
            ref="productImageWrap"
            class="product-image-wrap"
          >
            <img class="product-image" :src="selectImage(item)" alt="" />
          </div>

          <div ref="productInfo" class="product-info">
            <div v-if="showBrand && item.brand_name" class="brand">
              {{ item.brand_name }}
            </div>

            <div v-if="showSku" class="sku">{{ item.sku }}</div>

            <div v-if="showDescription && item.description" class="description">
              {{ item.description }}
            </div>

            <div v-if="showPrice" class="price">
              {{ formatPrice(item.price) }}
            </div>

            <div v-if="showMinMax" class="minmax">
              <span v-if="item.min_qty !== null">Min: {{ item.min_qty }}</span>
              <span v-if="item.min_qty !== null && item.max_qty !== null">
                &emsp;·&emsp;
              </span>
              <span v-if="item.max_qty !== null">Max: {{ item.max_qty }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- FALLBACK -->
      <div v-else class="unknown-layout">
        Layout no soportado: <b>{{ page.layout }}</b>
      </div>

      <!-- FOOTER -->
      <div v-if="page.layout !== 'cover'" class="page-footer">
        {{ doc.name }}
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'CatalogPrintDocument',
  props: {
    doc: { type: Object, required: true },
    pdfMode: { type: Boolean, default: false },
  },

  computed: {
    // Settings seguros (sin optional chaining)
    showPrice() {
      return !!(this.doc && this.doc.settings && this.doc.settings.show_price)
    },
    showBrand() {
      return !!(this.doc && this.doc.settings && this.doc.settings.show_brand)
    },
    showMinMax() {
      return !!(this.doc && this.doc.settings && this.doc.settings.show_min_max)
    },
    showSku() {
      return !!(this.doc && this.doc.settings && this.doc.settings.show_sku)
    },
    showDescription() {
      return !!(
        this.doc &&
        this.doc.settings &&
        this.doc.settings.show_description
      )
    },
    showImages() {
      return !!(this.doc && this.doc.settings && this.doc.settings.show_images)
    },

    coverOverlayClass() {
      const v = this.doc && this.doc.theme ? this.doc.theme.cover_overlay : ''
      return v === 'dark' ? 'overlay-dark' : 'overlay-light'
    },

    cardStyleClass() {
      const v = this.doc && this.doc.theme ? this.doc.theme.card_style : ''
      return v === 'outlined' ? 'card-outlined' : 'card-flat'
    },

    isLandscape() {
      return this.doc && this.doc.orientation === 'landscape'
    },

    gridLayoutClass() {
      if (!this.doc || !this.doc.pages) return ''
      if (this.doc.pages.length < 2) return '' // si no hay página 2, no asumimos layout de grid
      const page = this.doc.pages[1] // asumimos que la página 2 define el layout del grid
      if (!page) return ''
      switch (page.layout) {
        case 'grid_2x3':
          return 'layout-grid-2x3'
        case 'grid_2x4':
          return 'layout-grid-2x4'
        case 'grid_2x5':
          return 'layout-grid-2x5'
        case 'grid_2x6':
          return 'layout-grid-2x6'
        case 'grid_3x3':
          return 'layout-grid-3x3'
        case 'grid_3x4':
          return 'layout-grid-3x4'
        case 'grid_3x5':
          return 'layout-grid-3x5'
        default:
          return 'unknown'
      }
    },
  },

  methods: {
    pageClass(page) {
      return {
        cover: page.layout === 'cover',
        'layout-grid-2x3': page.layout === 'grid_2x3',
        'layout-grid-2x4': page.layout === 'grid_2x4',
        'layout-grid-2x5': page.layout === 'grid_2x5',
        'layout-grid-2x6': page.layout === 'grid_2x6',
        'layout-grid-3x3': page.layout === 'grid_3x3',
        'layout-grid-3x4': page.layout === 'grid_3x4',
        'layout-grid-3x5': page.layout === 'grid_3x5',
        landscape: this.isLandscape,
        portrait: !this.isLandscape,
      }
    },

    pageNumber(index) {
      const hasCover =
        this.doc &&
        this.doc.pages &&
        this.doc.pages[0] &&
        this.doc.pages[0].layout === 'cover'
      return hasCover ? index : index + 1
    },

    selectImage(item) {
      if (item && item.selected_image_url) return item.selected_image_url
      if (item && item.images && item.images.length) {
        const primary = item.images.find((x) => x && x.is_primary)
        return (primary && primary.url) || item.images[0].url || ''
      }
      return ''
    },

    formatPrice(value) {
      if (value == null || value === '') return ''
      const n = Number(value)
      if (Number.isNaN(n)) return String(value)
      return `$${n.toFixed(2)}`
    },
  },
}
</script>

<style>
/* =========================================================
   1) CENTRADO EN PANTALLA (solo visual)
   ========================================================= */
.print-document {
  background: #f2f2f2;
  padding: 10mm 0;
  display: flex;
  flex-direction: column;
  align-items: center; /* ✅ centra las páginas */
  gap: 10mm;
}

/* Cuando imprimes, no queremos fondo gris ni gaps */
@media print {
  .print-document {
    background: #fff !important;
    padding: 0 !important;
    gap: 0 !important;
  }
}

/* --- Tamaños Letter --- */
/**
 * CSS Custom Properties para configuración de impresión de documentos
 * 
 * Define variables globales para el diseño de catálogos en formato imprimible.
 * 
 * Dimensiones de página:
 * - Portrait: 216mm × 279mm (tamaño carta)
 * - Landscape: 279mm × 216mm (tamaño carta apaisado)
 * 
 * Márgenes:
 * - margin-top: Espacio en blanco desde el borde superior de la página (12mm)
 * - margin-bottom: Espacio en blanco desde el borde inferior de la página (12mm)
 * - margin-left: Espacio en blanco desde el borde izquierdo (12mm)
 * - margin-right: Espacio en blanco desde el borde derecho (12mm)
 * 
 * Otros:
 * - gap: Espaciado entre elementos (5mm)
 * - text: Color de texto principal (#111)
 * - muted: Color de texto secundario (#666)
 * - border: Color de bordes (#ddd)
 */
:root {
  --page-width-portrait: 216mm;
  --page-height-portrait: 279mm;

  --page-width-landscape: 279mm;
  --page-height-landscape: 216mm;

  --margin-top: 12mm;
  --margin-bottom: 12mm;
  --margin-left: 12mm;
  --margin-right: 12mm;

  --gap: 3mm;

  --text: #111;
  --muted: #666;
  --border: #ddd;
}

/* =========================================================
   2) @page correcto para imprimir landscape
   Nota: algunos browsers respetan @page solo en @media print
   ========================================================= */
@media print {
  /* Para landscape real */
  @page :left {
    margin: 0;
  }
  @page :right {
    margin: 0;
  }
}

/* No podemos condicionar @page por clase en CSS estándar,
   así que hacemos 2 rutas:
   - (A) CSS de pantalla define dimensiones
   - (B) Para impresión, forzamos landscape con un truco:
       usamos size: Letter landscape y dejamos que el usuario
       o Playwright elija la orientación.
   En tu caso: queremos que Ctrl+P se ponga landscape.
*/
/* @media print {
  @page {
    size: Letter landscape;
    margin: 0;
  }
} */

html,
body {
  margin: 0;
  padding: 0;
  background: #fff;
  color: var(--text);
  font-family: Arial, Helvetica, sans-serif;
}

.print-page {
  position: relative;
  box-sizing: border-box;
  break-after: page;
  overflow: hidden;
  background: #fff; /* visual */
  box-shadow: 0 2mm 6mm rgba(0, 0, 0, 0.15); /* visual */
}

/* Sin sombra al imprimir */
@media print {
  .print-page {
    box-shadow: none !important;
  }
  /* .print-page:last-child {
    page-break-after: auto;
  } */
  .print-page:last-child {
    break-after: auto; /* ✅ evita hoja en blanco final */
  }
}

/* Padding interno */
.print-page {
  padding: var(--margin-top) var(--margin-right) var(--margin-bottom)
    var(--margin-left);
}

/* Dimensiones en pantalla (y en PDF también ayudan) */
.print-page.portrait {
  width: var(--page-width-portrait);
  height: var(--page-height-portrait);
}

.print-page.landscape {
  width: var(--page-width-landscape);
  height: var(--page-height-landscape);
}

/* Header / Footer */
.page-header {
  display: flex;
  justify-content: space-between;
  font-size: 9pt;
  margin-bottom: 5mm;
  color: var(--muted);
}

.page-footer {
  position: absolute;
  left: var(--margin-left);
  right: var(--margin-right);
  bottom: 7mm;
  text-align: center;
  font-size: 8pt;
  color: var(--muted);
}

/* =======================
   COVER
   ======================= */
.cover {
  width: 100%;
  height: 100%;
  position: relative;
  display: grid;
  place-items: center;
}

.cover-hero {
  position: absolute;
  inset: 0;
}

.cover-hero-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cover-overlay {
  position: absolute;
  inset: 0;
}

.overlay-dark {
  background: rgba(0, 0, 0, 0.45);
}
.overlay-light {
  background: rgba(255, 255, 255, 0.35);
}

.cover-content {
  position: relative;
  z-index: 2;
  text-align: center;
  padding: 10mm;
  max-width: 160mm;
}

.cover-title {
  font-size: 30pt;
  font-weight: 700;
  color: #fff;
}

.cover-subtitle {
  margin-top: 6mm;
  font-size: 14pt;
  color: #fff;
  opacity: 0.95;
}

.cover-logo {
  margin-top: 10mm;
  max-height: 22mm;
  max-width: 80mm;
  object-fit: contain;
}

/* =======================
   GRID 2x3
   ======================= */
.content.layout-grid-2x3 {
  height: calc(100% - 18mm);
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(3, 1fr);
  gap: var(--gap);
}

/* =======================
   GRID 2x4
   ======================= */
.content.layout-grid-2x4 {
  height: calc(100% - 18mm);
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(4, 1fr);
  gap: var(--gap);
}

/* =======================
   GRID 2x5
   ======================= */
.content.layout-grid-2x5 {
  height: calc(100% - 18mm);
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(5, 1fr);
  gap: var(--gap);
}

/* =======================
   GRID 2x6
   ======================= */
.content.layout-grid-2x6 {
  height: calc(100% - 18mm);
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(6, 1fr);
  gap: var(--gap);
}

/* =======================
   GRID 3x3
   ======================= */
.content.layout-grid-3x3 {
  height: calc(100% - 18mm);
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(3, 1fr);
  gap: var(--gap);
}

/* =======================
   GRID 3x4
   ======================= */
.content.layout-grid-3x4 {
  height: calc(100% - 18mm);
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(4, 1fr);
  gap: var(--gap);
}

/* =======================
   GRID 3x5
   ======================= */
.content.layout-grid-3x5 {
  height: calc(100% - 18mm);
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(5, 1fr);
  gap: var(--gap);
}

/* Card styles */
.product-card {
  box-sizing: border-box;
  padding: 3.5mm;
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  align-items: stretch;
  gap: var(--gap);
  overflow: hidden;
  background: #fff;
}

.card-outlined {
  border: 1px solid var(--border);
}
.card-flat {
  border: none;
}

.product-image-wrap {
  flex: 0 0 35%;
  height: 100%;
  margin-top: 0;
  display: flex;
  justify-content: flex-end;
  align-items: flex-start;
  overflow: hidden;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: top right;
}

.product-info {
  flex: 1;
  min-width: 0;
  margin-top: 10px;
  display: grid;
  gap: 1.2mm;
}

.row-top {
  display: flex;
  justify-content: space-between;
  gap: 2mm;
  align-items: baseline;
  margin-left: inherit;
  margin-right: inherit;
}

.sku {
  font-size: 10pt;
  font-weight: 700;
  white-space: nowrap;
}

.price {
  font-size: 8pt;
  color: var(--muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 60%;
}

.brand {
  font-size: 8.5pt;
  color: var(--muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.description {
  font-size: 10pt;
  color: var(--muted);
  line-height: 1.15;
  max-height: 22mm;
  overflow: hidden;
}

.minmax {
  display: flex;
  justify-content: flex-start;
  font-size: 8pt;
  color: var(--muted);
}

.unknown-layout {
  font-size: 12pt;
  color: #b00;
}

@media print {
  /* Reserva un “buffer” para evitar que Chrome parta cada página en 2 */
  :root {
    --print-safe-buffer: 14mm;
  }

  .print-page.portrait {
    height: calc(var(--page-height-portrait) - var(--print-safe-buffer));
  }

  .print-page.landscape {
    height: calc(var(--page-height-landscape) - var(--print-safe-buffer));
  }

  /* Mantén el corte de página */
  .print-page {
    break-after: page;
  }

  .print-page:last-child {
    break-after: auto;
  }
}

/* ============================= */
/* PDF MODE (para Playwright)    */
/* ============================= */
body.pdf-mode .print-document {
  background: #fff !important;
  padding: 0 !important;
  gap: 0 !important;
}

body.pdf-mode .print-page {
  box-shadow: none !important;
}

/* Opcional: si estabas usando el buffer para Ctrl+P,
   lo desactivamos en modo pdf para maximizar área. */
@media print {
  body.pdf-mode :root {
    --print-safe-buffer: 0mm !important;
  }
}
</style>
