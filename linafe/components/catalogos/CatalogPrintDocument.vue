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
          <img
            v-if="page.cover && page.cover.logo_url"
            class="cover-logo"
            :src="page.cover.logo_url"
            alt=""
          />

          <div class="cover-title" :style="{ color: titleColorClass }">
            {{ (page.cover && page.cover.title) || doc.name }}
          </div>

          <div
            v-if="page.cover && page.cover.subtitle"
            class="cover-subtitle"
            :style="{ color: titleColorClass }"
          >
            {{ page.cover.subtitle }}
          </div>
        </div>
      </div>

      <!-- GRID -->
      <div
        v-else-if="isGridPage(page)"
        class="content content-grid"
        :class="pageClass(page)"
        :style="contentStyle(page)"
      >
        <div class="content-grid-inner" :style="gridStyle(page)">
          <div
            v-for="item in page.items"
            :key="item.product_id || item.sku"
            class="product-card"
            :class="cardStyleClass"
            :style="productCardStyle(page)"
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

              <div
                v-if="showDescription && item.description"
                class="description"
              >
                {{ item.description }}
              </div>

              <div v-if="showPrice" class="price">
                {{ formatPrice(item.price) }}
              </div>

              <div v-if="showMinMax" class="minmax">
                <span v-if="item.min_qty !== null"
                  >Min: {{ item.min_qty }}</span
                >
                <span v-if="item.min_qty !== null && item.max_qty !== null">
                  &emsp;·&emsp;
                </span>
                <span v-if="item.max_qty !== null"
                  >Max: {{ item.max_qty }}</span
                >
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Listado -->

      <!-- Destacado o Hero -->
      <div
        v-else-if="
          page.layout &&
          page.layout.startsWith('hero') &&
          page.hero &&
          page.hero.slots &&
          page.hero.slots.length > 0
        "
        class="hero-wrap"
      >
        <div
          v-for="(slot, idx) in resolvedHeroSlots(page)"
          :key="slot.product_key || idx"
          class="hero-item"
        >
          <div
            class="hero-item-top"
            :class="page.layout === 'hero_2' ? 'hero-2' : 'hero-1'"
          >
            <div class="hero-media">
              <img
                v-if="slot.main_url"
                class="hero-img"
                :src="slot.main_url"
                alt=""
              />
              <div v-else class="hero-img hero-img-empty">Sin imagen</div>
            </div>

            <div class="hero-body">
              <div v-if="slot.product" class="hero-brand">
                {{ showBrand ? slot.product.brand_name : '' }}
              </div>

              <div v-if="slot.product" class="hero-sku">
                {{ showSku ? slot.product.sku : '' }}
              </div>

              <div v-if="slot.product" class="hero-title">
                {{
                  slot.product.name ||
                  slot.product.product_name ||
                  slot.product.description ||
                  ''
                }}
              </div>

              <div v-if="slot.product && showDescription" class="hero-desc">
                {{ slot.product.description }}
              </div>

              <div v-if="slot.product && showPrice" class="hero-meta">
                Precio: {{ formatPrice(slot.product.price) }}
              </div>

              <div v-if="slot.product && showMinMax" class="hero-meta">
                Min: {{ slot.product.min_qty }} · Max:
                {{ slot.product.max_qty }}
              </div>

              <div v-if="!slot.product" class="hero-empty">
                Configura HERO en Propiedades
              </div>
            </div>
          </div>
          <div
            v-if="slot.gallery_urls && slot.gallery_urls.length"
            class="hero-thumbs"
          >
            <img
              v-for="u in slot.gallery_urls"
              :key="u"
              class="hero-thumb"
              :src="u"
              alt=""
            />
          </div>
        </div>
      </div>

      <div
        v-else-if="page.layout && page.layout.startsWith('hero')"
        class="unknown-layout"
      >
        Esta sección destacada no está disponible todavía. Completa su
        configuración para mostrarla.
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
import { computeCatalogLayout } from '@/utils/catalogLayout'

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
      const vv = v !== '' ? `overlay-${v}` : ''
      return vv
    },

    titleColorClass() {
      const v = this.doc && this.doc.theme ? this.doc.theme.primary : '#FFFFFF'
      return v
    },

    cardStyleClass() {
      const v = this.doc && this.doc.theme ? this.doc.theme.card_style : ''
      return v === 'outlined' ? 'card-outlined' : 'card-flat'
    },

    isLandscape() {
      return this.doc && this.doc.orientation === 'landscape'
    },
  },

  methods: {
    pageClass(page) {
      return {
        cover: page.layout === 'cover',
        'layout-grid-2': page.layout === 'grid_2',
        'layout-grid-3': page.layout === 'grid_3',
        landscape: this.isLandscape,
        portrait: !this.isLandscape,
      }
    },

    pageMetrics(page) {
      return computeCatalogLayout({
        layout: page && page.layout ? page.layout : 'grid_2',
        orientation: this.isLandscape ? 'landscape' : 'portrait',
        settings: this.doc && this.doc.settings ? this.doc.settings : {},
        surface: 'pdf',
      })
    },

    isGridPage(page) {
      return !!(page && (page.layout === 'grid_2' || page.layout === 'grid_3'))
    },

    contentStyle(page) {
      if (!this.isGridPage(page)) return {}

      const metrics = this.pageMetrics(page)

      return {
        height: `${metrics.contentHeight}px`,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'flex-start',
      }
    },

    gridStyle(page) {
      if (!this.isGridPage(page)) return {}

      const metrics = this.pageMetrics(page)

      return {
        width: `${metrics.effectivePageWidth}px`,
        maxWidth: `${metrics.effectivePageWidth}px`,
        display: 'grid',
        gridTemplateColumns: `repeat(${metrics.columns}, 1fr)`,
        gridTemplateRows: `repeat(${metrics.rowsPerPage}, ${metrics.cardHeight}px)`,
        columnGap: `${metrics.columnGap || 8}px`,
        rowGap: `${metrics.rowGap || 8}px`,
        alignContent: 'start',
      }
    },

    productCardStyle(page) {
      if (!this.isGridPage(page)) return {}

      const metrics = this.pageMetrics(page)

      return {
        height: `${metrics.cardHeight}px`,
        minHeight: `${metrics.cardHeight}px`,
        maxHeight: `${metrics.cardHeight}px`,
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

    productKey(p) {
      if (!p) return ''
      if (p.product_id) return `id:${p.product_id}`
      if (p.sku) return `sku:${p.sku}`
      return ''
    },

    buildProductIndex(pageItems) {
      const index = {}
      const items = Array.isArray(pageItems) ? pageItems : []
      items.forEach((item) => {
        const key = this.productKey(item)
        if (key && !index[key]) index[key] = item
      })
      return index
    },

    resolveProductByKey(key, productIndex) {
      const k = String(key || '')
      if (!k) return null
      return (productIndex && productIndex[k]) || null
    },

    resolvedHeroSlots(page) {
      const hero = page && page.hero ? page.hero : null
      const slots = hero && Array.isArray(hero.slots) ? hero.slots : []
      if (!slots.length) return []

      const productIndex = this.buildProductIndex(page && page.items)

      return slots.map((slot) => {
        const product = this.resolveProductByKey(
          slot && slot.product_key,
          productIndex
        )
        return {
          ...slot,
          product,
        }
      })
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

/* Padding interno
.print-page {
  padding: var(--margin-top) var(--margin-right) var(--margin-bottom)
    var(--margin-left);
}
*/

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
}

.cover-subtitle {
  margin-top: 6mm;
  font-size: 14pt;
  opacity: 0.95;
}

.cover-logo {
  margin-top: 10mm;
  max-height: 22mm;
  max-width: 80mm;
  object-fit: contain;
}

/* =======================
   GRID a 2 o  3 columnas
   ======================= */
.content-grid {
  width: 100%;
  align-content: start;
}

.content-grid-inner {
  box-sizing: border-box;
}

/* Card styles */
.product-card {
  box-sizing: border-box;
  padding: 3.5mm;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
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
  flex: 0 0 72px;
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
  margin-top: 0;
  display: grid;
  gap: 1.2mm;
  align-content: start;
}

.row-top {
  display: flex;
  justify-content: space-between;
  gap: 2mm;
  align-items: baseline;
  margin-left: inherit;
  margin-right: inherit;
}

.brand,
.sku,
.price,
.minmax {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.brand {
  font-size: 8.5pt;
  color: var(--muted);
}

.sku {
  font-size: 10pt;
  font-weight: 700;
}

.price {
  font-size: 8pt;
  color: var(--muted);
}

.description {
  font-size: 10pt;
  color: var(--muted);
  line-height: 1.15;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
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

/* =======================
   HERO
   ======================= */
.hero-wrap {
  display: grid;
  grid-gap: 12px;
}

.hero-item {
  border: 1px solid rgba(0, 0, 0, 0.12);
  border-radius: 6px;
  padding: 12px;
}

.hero-item-top {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 12px;
}

.hero-media {
  display: grid;
  gap: 8px;
}

.hero-img {
  width: 100%;
  height: 260px;
  object-fit: contain;
  background: #fff;
  border-radius: 6px;
}

.hero-img-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.7;
}

.hero-thumbs {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 6px;
}

.hero-thumb {
  width: 100%;
  height: 124px;
  object-fit: cover;
  border-radius: 6px;
  border: 1px solid rgba(0, 0, 0, 0.12);
}

.hero-body {
  display: grid;
  align-content: start;
  gap: 6px;
}

.hero-brand {
  font-size: 12px;
  opacity: 0.8;
}

.hero-sku {
  font-weight: 600;
}

.hero-title {
  font-weight: 600;
}

.hero-desc {
  font-size: 13px;
  opacity: 0.9;
}

.hero-meta {
  margin-top: 6px;
  font-size: 12px;
  opacity: 0.85;
}

.hero-empty {
  font-size: 12px;
  opacity: 0.75;
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
