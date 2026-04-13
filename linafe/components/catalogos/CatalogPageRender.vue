<template>
  <div :style="pageVars">
    <v-sheet class="pa-6" outlined :style="paperStyle">
      <template v-if="isCover">
        <div class="cover">
          <div
            v-if="coverHeroUrl"
            class="cover-hero"
            :style="{ backgroundImage: `url('${coverHeroUrl}')` }"
          />
          <div class="cover-overlay" :class="coverOverlayClass">
            <div class="cover-content">
              <v-img
                v-if="coverLogoUrl"
                ref="img-cover"
                class="cover-logo"
                :src="coverLogoUrl"
                alt=""
                contain
              />
              <div class="cover-title">{{ coverTitle }}</div>
              <div v-if="coverSubtitle" class="cover-subtitle">
                {{ coverSubtitle }}
              </div>
            </div>
          </div>
        </div>
      </template>

      <template v-else>
        <div v-if="isHero" class="hero-wrap">
          <div v-for="(s, idx) in heroSlots" :key="idx" class="hero-item">
            <!-- HERO 1 & 2: Layout horizontal (imagen | contenido) -->
            <template
              v-if="page.layout === 'hero_1' || page.layout === 'hero_2'"
            >
              <div
                class="hero-item-top"
                :class="page.layout === 'hero_2' ? 'hero-2' : 'hero-1'"
              >
                <div class="hero-media">
                  <img
                    v-if="s.main_url"
                    class="hero-img"
                    :src="s.main_url"
                    alt=""
                  />
                  <div v-else class="hero-img hero-img-empty">Sin imagen</div>
                </div>

                <div class="hero-body">
                  <div v-if="s.product" class="hero-brand">
                    {{
                      settings && settings.show_brand
                        ? s.product.brand_name
                        : ''
                    }}
                  </div>

                  <div v-if="s.product" class="hero-sku">
                    {{ settings && settings.show_sku ? s.product.sku : '' }}
                  </div>

                  <div v-if="s.product" class="hero-title">
                    {{
                      s.product.name ||
                      s.product.product_name ||
                      s.product.description ||
                      ''
                    }}
                  </div>

                  <div
                    v-if="s.product && settings && settings.show_description"
                    class="hero-desc"
                  >
                    {{ s.product.description }}
                  </div>

                  <div
                    v-if="s.product && settings && settings.show_price"
                    class="hero-meta"
                  >
                    Precio: {{ s.product.price }}
                  </div>
                  <div
                    v-if="s.product && settings && settings.show_min_max"
                    class="hero-meta"
                  >
                    Min: {{ s.product.min_qty }} · Max: {{ s.product.max_qty }}
                  </div>

                  <div v-if="!s.product" class="hero-empty">
                    Configura HERO en Propiedades
                  </div>
                </div>
              </div>
              <div
                v-if="s.gallery_urls && s.gallery_urls.length"
                class="hero-thumbs"
              >
                <img
                  v-for="u in s.gallery_urls"
                  :key="u"
                  class="hero-thumb"
                  :src="u"
                  alt=""
                  @click.stop="
                    $emit('thumb-clicked', { slotIndex: idx, url: u })
                  "
                />
              </div>
            </template>

            <!-- HERO 3: Layout portrait (logo + imagen|thumbs | info) -->
            <template v-if="page.layout === 'hero_3'">
              <div class="hero3-header">
                <v-img
                  v-if="coverLogoUrl"
                  class="hero3-logo"
                  :src="coverLogoUrl"
                  alt=""
                  contain
                />
              </div>

              <div class="hero3-middle">
                <div class="hero3-media">
                  <img
                    v-if="s.main_url"
                    class="hero3-main-img"
                    :src="s.main_url"
                    alt=""
                  />
                  <div v-else class="hero3-main-img hero-img-empty">
                    Sin imagen
                  </div>
                </div>

                <div
                  v-if="s.gallery_urls && s.gallery_urls.length"
                  class="hero3-thumbs"
                >
                  <img
                    v-for="(u, ti) in s.gallery_urls.slice(0, 3)"
                    :key="ti"
                    class="hero3-thumb"
                    :src="u"
                    alt=""
                    @click.stop="
                      $emit('thumb-clicked', { slotIndex: idx, url: u })
                    "
                  />
                </div>
              </div>

              <div class="hero3-footer">
                <div v-if="s.product" class="hero-brand">
                  {{
                    settings && settings.show_brand ? s.product.brand_name : ''
                  }}
                </div>

                <div v-if="s.product" class="hero-sku">
                  {{ settings && settings.show_sku ? s.product.sku : '' }}
                </div>

                <div v-if="s.product" class="hero-title">
                  {{
                    s.product.name ||
                    s.product.product_name ||
                    s.product.description ||
                    ''
                  }}
                </div>

                <div
                  v-if="s.product && settings && settings.show_description"
                  class="hero-desc"
                >
                  {{ s.product.description }}
                </div>

                <div
                  v-if="s.product && settings && settings.show_price"
                  class="hero-meta"
                >
                  Precio: {{ s.product.price }}
                </div>
                <div
                  v-if="s.product && settings && settings.show_min_max"
                  class="hero-meta"
                >
                  Min: {{ s.product.min_qty }} · Max: {{ s.product.max_qty }}
                </div>

                <div v-if="!s.product" class="hero-empty">
                  Configura HERO en Propiedades
                </div>
              </div>
            </template>

            <!-- HERO 4: Layout landscape (logo + info | 2 imágenes grandes) -->
            <template v-if="page.layout === 'hero_4'">
              <div class="hero4-header">
                <div class="hero4-logo-section">
                  <v-img
                    v-if="coverLogoUrl"
                    class="hero4-logo"
                    :src="coverLogoUrl"
                    alt=""
                    contain
                  />
                </div>

                <div class="hero4-info-section">
                  <div v-if="s.product" class="hero-brand">
                    {{
                      settings && settings.show_brand
                        ? s.product.brand_name
                        : ''
                    }}
                  </div>

                  <div v-if="s.product" class="hero-sku">
                    {{ settings && settings.show_sku ? s.product.sku : '' }}
                  </div>

                  <div v-if="s.product" class="hero-title">
                    {{
                      s.product.name ||
                      s.product.product_name ||
                      s.product.description ||
                      ''
                    }}
                  </div>

                  <div
                    v-if="s.product && settings && settings.show_description"
                    class="hero-desc"
                  >
                    {{ s.product.description }}
                  </div>

                  <div
                    v-if="s.product && settings && settings.show_price"
                    class="hero-meta"
                  >
                    Precio: {{ s.product.price }}
                  </div>
                  <div
                    v-if="s.product && settings && settings.show_min_max"
                    class="hero-meta"
                  >
                    Min: {{ s.product.min_qty }} · Max: {{ s.product.max_qty }}
                  </div>

                  <div v-if="!s.product" class="hero-empty">
                    Configura HERO en Propiedades
                  </div>
                </div>
              </div>

              <div v-if="hero4DisplayUrls(s).length" class="hero4-images">
                <img
                  v-for="(u, ti) in hero4DisplayUrls(s)"
                  :key="ti"
                  class="hero4-img"
                  :src="u"
                  alt=""
                  @click.stop="
                    $emit('thumb-clicked', { slotIndex: idx, url: u })
                  "
                />
              </div>
            </template>
          </div>

          <div v-if="safeItems.length > heroSlotsCount" class="hero-note">
            Hay {{ safeItems.length - heroSlotsCount }} producto(s) extra en
            esta página
          </div>
        </div>
        <div v-else>
          <v-row dense>
            <v-col
              v-for="p in visibleItems"
              :key="p.product_id || p.sku"
              cols="12"
              v-bind="gridCols"
            >
              <v-card
                :outlined="effectiveTheme.card_style !== 'flat'"
                class="pa-1 cat-card"
                :class="cardClass"
                :style="cardInlineStyle"
              >
                <div class="d-flex">
                  <div>
                    <v-img
                      v-if="effectiveSettings.show_images"
                      ref="img-item"
                      :src="p.selected_image_url"
                      :lazy-src="p.selected_image_url"
                      width="72"
                      height="72"
                      class="d-flex mr-3 img-item-wrap"
                      contain
                    >
                      <v-chip
                        v-if="
                          effectiveSettings.show_images &&
                          p.images &&
                          p.images.length > 1
                        "
                        x-small
                        color="rgba(0, 0, 0, 0.50)"
                        text-color="white"
                        class="thumb-more"
                      >
                        +{{ p.images.length - 1 }}
                      </v-chip>
                    </v-img>
                  </div>

                  <div class="flex-grow-1">
                    <div
                      v-if="effectiveSettings.show_brand"
                      class="text-caption text--secondary item-brand"
                    >
                      {{ p.brand_name }}
                    </div>

                    <div
                      v-if="effectiveSettings.show_sku"
                      class="text-subtitle-2 font-weight-medium item-sku"
                    >
                      {{ p.sku }}
                    </div>

                    <div
                      v-if="effectiveSettings.show_description"
                      class="text-body-2 text--secondary item-desc"
                    >
                      {{ p.description }}
                    </div>

                    <div class="text-caption text--secondary item-price">
                      <span v-if="effectiveSettings.show_price">
                        {{ formatPrice(p.price) }}
                      </span>
                    </div>
                    <div class="text-caption text--secondary item-minmax">
                      <span v-if="effectiveSettings.show_min_max">
                        Min: {{ p.min_qty }} · Max: {{ p.max_qty }}
                      </span>
                    </div>
                  </div>
                </div>
              </v-card>
            </v-col>
          </v-row>
        </div>
        <v-alert v-if="hiddenCount > 0" dense text type="info" class="mt-4">
          Hay {{ hiddenCount }} productos más en esta página
        </v-alert>
      </template>
    </v-sheet>
  </div>
</template>

<script>
import { computeCatalogLayout } from '@/utils/catalogLayout'

export default {
  name: 'CatalogPageRender',

  props: {
    page: { type: Object, required: true },
    orientation: { type: String, default: 'portrait' },
    settings: { type: Object, default: () => ({}) },
    theme: { type: Object, default: () => ({}) },
    isPrint: { type: Boolean, default: false },
  },

  computed: {
    effectiveSettings() {
      const defaults = {
        show_price: true,
        show_brand: true,
        show_min_max: true,
        show_sku: true,
        show_description: true,
        show_images: true,
      }

      return { ...defaults, ...(this.settings || {}) }
    },

    isCover() {
      return this.page && this.page.layout === 'cover'
    },

    isLandscape() {
      return this.orientation === 'landscape'
    },

    paperStyle() {
      return {
        width: `${this.pageMetrics.effectivePageWidth}px`,
        height: `${this.pageMetrics.pageHeight}px`,
        margin: '0 auto',
        background: 'white',
      }
    },

    coverData() {
      if (!this.isCover) return {}
      return this.page.cover || {}
    },

    coverTitle() {
      return this.coverData.title || ''
    },

    coverSubtitle() {
      return this.coverData.subtitle || ''
    },

    coverLogoUrl() {
      return this.coverData.logo_url || ''
    },

    coverHeroUrl() {
      return this.coverData.hero_url || ''
    },

    layoutKey() {
      return (this.page && this.page.layout) || 'grid_2'
    },

    capacity() {
      return this.pageMetrics.capacity || 8
    },

    layout() {
      return (this.page && this.page.layout) || 'grid_2'
    },

    layoutColumns() {
      if (this.layoutKey === 'grid_3') return 3
      if (this.layoutKey === 'grid_2') return 2
      return 1
    },

    visibleInfoLines() {
      let lines = 0

      if (this.effectiveSettings.show_brand) lines += 1
      if (this.effectiveSettings.show_sku) lines += 1
      if (this.effectiveSettings.show_description) lines += 2
      if (this.effectiveSettings.show_price) lines += 1
      if (this.effectiveSettings.show_min_max) lines += 1

      return lines
    },

    pageMetrics() {
      return computeCatalogLayout({
        layout: this.layoutKey,
        orientation: this.orientation,
        settings: this.effectiveSettings,
        surface: 'canvas',
      })
    },

    items() {
      const items =
        this.page && Array.isArray(this.page.items) ? this.page.items : []
      return items
    },

    heroItems() {
      const cap = this.layout === 'hero_2' ? 2 : 1
      return this.items.slice(0, cap)
    },

    isHero() {
      return (
        this.page &&
        (this.layout === 'hero_1' ||
          this.layout === 'hero_2' ||
          this.layout === 'hero_3' ||
          this.layout === 'hero_4')
      )
    },

    heroSlotsCount() {
      if (!this.page) return 1
      return this.page.layout === 'hero_2' ? 2 : 1
    },

    safeItems() {
      const items =
        this.page && Array.isArray(this.page.items) ? this.page.items : []
      return items
    },

    heroSlots() {
      if (!this.isHero) return []

      const hero = this.page && this.page.hero ? this.page.hero : null
      const slots = hero && Array.isArray(hero.slots) ? hero.slots : []

      const out = []

      for (let i = 0; i < this.heroSlotsCount; i += 1) {
        const slot = slots[i] || {}
        const p = this.resolveProductByKey(slot.product_key)

        const mainUrl = this.resolveMainUrl(p, slot)
        const galleryUrls = this.resolveGalleryUrls(p, slot)

        out.push({
          product: p,
          product_key: slot.product_key || '',
          main_url: mainUrl,
          gallery_urls: galleryUrls,
        })
      }

      return out
    },

    visibleItems() {
      return this.items.slice(0, this.capacity)
    },

    hiddenCount() {
      const n = this.items.length - this.visibleItems.length
      return n > 0 ? n : 0
    },

    gridCols() {
      if (this.layoutKey === 'list_compact') return { md: 12 }
      if (this.layoutKey === 'hero_1') return { md: 12 }
      if (this.layoutKey === 'hero_2') return { md: 12 }
      if (this.layoutKey === 'grid_3') return { md: 4 }
      if (this.layoutKey === 'grid_2') return { md: 6 }
      return { md: 6 }
    },

    effectiveTheme() {
      const defaults = {
        primary: '#1976d2',
        cover_overlay: 'light',
        card_style: 'outlined',
      }

      return { ...defaults, ...(this.theme || {}) }
    },

    pageVars() {
      return {
        '--cat-primary': this.effectiveTheme.primary,
      }
    },

    cardClass() {
      const style = this.effectiveTheme.card_style
      if (style === 'flat') return 'cat-card-flat'
      return 'cat-card-outlined'
    },

    cardInlineStyle() {
      if (this.layoutKey !== 'grid_2' && this.layoutKey !== 'grid_3') return {}

      return {
        height: `${this.pageMetrics.cardHeight}px`,
        overflow: 'hidden',
      }
    },

    coverOverlayClass() {
      const overlay = this.effectiveTheme.cover_overlay
      if (overlay === 'dark') return 'cover-overlay-dark'
      if (overlay === 'light') return 'cover-overlay-light'
      return ''
    },
  },

  methods: {
    productKey(p) {
      if (!p) return ''
      if (p.product_id) return `id:${p.product_id}`
      if (p.sku) return `sku:${p.sku}`
      return ''
    },

    resolveProductByKey(key) {
      const k = String(key || '')
      if (!k) return null
      return this.safeItems.find((p) => this.productKey(p) === k) || null
    },

    resolveMainUrl(p, slot) {
      if (slot && slot.main_url) return slot.main_url
      if (p && p.selected_image_url) return p.selected_image_url

      const imgs = p && Array.isArray(p.images) ? p.images : []
      return imgs[0] && imgs[0].url ? imgs[0].url : ''
    },

    resolveGalleryUrls(p, slot) {
      const urls =
        slot && Array.isArray(slot.gallery_urls) ? slot.gallery_urls : []

      const selected = urls.filter(Boolean).slice(0, 4)

      // En todos los layouts HERO respetamos estrictamente la selección.
      if (this.isHero) {
        return selected
      }

      if (selected.length) return selected

      const imgs = p && Array.isArray(p.images) ? p.images : []
      return imgs
        .map((x) => x && x.url)
        .filter(Boolean)
        .slice(0, 4)
    },

    hero4DisplayUrls(slot) {
      const main = slot && slot.main_url ? slot.main_url : ''
      const gallery =
        slot && Array.isArray(slot.gallery_urls) ? slot.gallery_urls : []

      return Array.from(new Set([main, ...gallery].filter(Boolean))).slice(0, 2)
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

<style scoped>
.item-brand,
.item-sku,
.item-price,
.item-minmax {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-desc {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.cat-card {
  border-color: rgba(0, 0, 0, 0.12);
  height: 100%;
}

.img-item-wrap {
  position: relative;
  overflow: hidden;
  flex: 0 0 72px;
}

.cover {
  width: 100%;
  height: 100%;
  position: relative;
  display: grid;
  place-items: center;
  border-radius: 6px;
  overflow: hidden;
  background: #f2f2f2;
}

.cover-hero {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  filter: saturate(1.05);
}

.cover-title {
  color: var(--cat-primary);
  font-size: 30pt;
  font-weight: 700;
}

.cover-subtitle {
  color: var(--cat-primary);
  margin-top: 6mm;
  font-size: 14pt;
  opacity: 0.95;
}

.cat-card-outlined:hover {
  border-color: var(--cat-primary);
}

.cat-card-flat {
  border: none !important;
  box-shadow: none !important;
}

.cover-overlay {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  /* background: linear-gradient(
    rgba(255, 255, 255, 0.92),
    rgba(255, 255, 255, 0.78)
  ); */
}

.cover-overlay-light {
  background: linear-gradient(
    rgba(255, 255, 255, 0.92),
    rgba(255, 255, 255, 0.78)
  );
}

.cover-overlay-dark {
  background: linear-gradient(rgba(0, 0, 0, 0.52), rgba(0, 0, 0, 0.65));
}

.cover-overlay-dark .text-body-2 {
  color: rgba(255, 255, 255, 0.9) !important;
}

.cover-overlay-dark .cover-title,
.cover-overlay-dark .cover-subtitle {
  color: white;
}

.title-overlay {
  background: linear-gradient(
    rgba(255, 255, 255, 0.92),
    rgba(255, 255, 255, 0.78)
  );
}

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

.hero-item-top.hero-2 {
  grid-template-columns: 1fr 1fr;
}

.hero-item-top.hero-1 {
  grid-template-columns: 1fr 1fr;
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
  cursor: pointer;
}

.hero-thumb:hover {
  opacity: 0.9;
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

.hero-note {
  font-size: 12px;
  opacity: 0.8;
}

.thumb-more {
  position: absolute;
  left: 50%;
  bottom: 4px;
  transform: translateX(-50%);
  z-index: 2;
  pointer-events: none;
}

.cover-content {
  position: relative;
  z-index: 2;
  text-align: center;
  padding: 10mm;
  max-width: 160mm;
}

.cover-logo {
  margin-top: 10mm;
  max-height: 22mm;
  max-width: 80mm;
  object-fit: contain;
}

/* HERO 3 - Portrait Layout */
.hero3-header {
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.hero3-logo {
  max-height: 24px;
  max-width: 100%;
  object-fit: contain;
}

.hero3-middle {
  display: grid;
  grid-template-columns: 1fr 140px;
  gap: 12px;
  margin-bottom: 12px;
}

.hero3-media {
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero3-main-img {
  width: 100%;
  height: 280px;
  object-fit: contain;
  background: #fafafa;
  border-radius: 6px;
  border: 1px solid rgba(0, 0, 0, 0.08);
}

.hero3-thumbs {
  display: grid;
  grid-template-columns: 1fr;
  gap: 6px;
}

.hero3-thumb {
  width: 100%;
  height: 132px;
  object-fit: cover;
  border-radius: 6px;
  border: 1px solid rgba(0, 0, 0, 0.12);
  cursor: pointer;
}

.hero3-thumb:hover {
  opacity: 0.9;
}

.hero3-footer {
  display: grid;
  align-content: start;
  gap: 6px;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
  padding-top: 8px;
}

/* HERO 4 - Landscape Layout */
.hero4-header {
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: 16px;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  align-items: start;
}

.hero4-logo-section {
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
}

.hero4-logo {
  max-height: 28px;
  max-width: 120px;
  object-fit: contain;
}

.hero4-info-section {
  display: grid;
  align-content: start;
  gap: 6px;
}

.hero4-images {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-top: 12px;
}

.hero4-img {
  width: 100%;
  height: 200px;
  object-fit: contain;
  background: #fafafa;
  border-radius: 6px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  cursor: pointer;
}

.hero4-img:hover {
  opacity: 0.9;
}
</style>
