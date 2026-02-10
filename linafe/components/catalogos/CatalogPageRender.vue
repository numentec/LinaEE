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
            <div class="d-flex align-center mb-4">
              <v-img
                v-if="coverLogoUrl"
                :src="coverLogoUrl"
                :lazy-src="coverLogoUrl"
                width="56"
                height="56"
                contain
                class="mr-3"
              />
              <!-- <div class="title-overlay pa-3 rounded"> -->
              <div class="pa-3 rounded">
                <div class="text-h5 font-weight-bold cover-title">
                  {{ coverTitle }}
                </div>
                <div class="text-body-2 text--secondary">
                  {{ coverSubtitle }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>

      <template v-else>
        <div v-if="isHero" class="hero-wrap">
          <div
            v-for="p in heroItems"
            :key="p.product_id || p.sku"
            class="hero-item"
            :class="layout === 'hero_2' ? 'hero-2' : 'hero-1'"
          >
            <div class="hero-media">
              <img class="hero-img" :src="p.selected_image_url" alt="" />

              <div v-if="p.images && p.images.length > 1" class="hero-thumbs">
                <img
                  v-for="(img, idx) in p.images.slice(0, 4)"
                  :key="idx"
                  class="hero-thumb"
                  :src="img.url || img"
                  alt=""
                />
              </div>
            </div>

            <div class="hero-body">
              <div v-if="settings && settings.show_brand" class="hero-brand">
                {{ p.brand_name }}
              </div>

              <div v-if="settings && settings.show_sku" class="hero-sku">
                {{ p.sku }}
              </div>

              <div class="hero-title">
                {{ p.name || p.description || p.product_name || '' }}
              </div>

              <div
                v-if="settings && settings.show_description"
                class="hero-desc"
              >
                {{ p.description }}
              </div>

              <div class="hero-meta">
                <span v-if="settings && settings.show_price">
                  Precio: {{ p.price }}
                </span>

                <span v-if="settings && settings.show_min_max">
                  · Min: {{ p.min_qty }} · Max: {{ p.max_qty }}
                </span>
              </div>
            </div>
          </div>

          <div v-if="items.length > heroItems.length" class="hero-note">
            Hay {{ items.length - heroItems.length }} producto(s) extra en esta
            página. Usa Reacomodar para distribuirlos.
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
                class="pa-2 cat-card"
                :class="cardClass"
              >
                <div class="d-flex">
                  <v-img
                    v-if="effectiveSettings.show_images"
                    :src="p.selected_image_url"
                    :lazy-src="p.selected_image_url"
                    width="72"
                    height="72"
                    class="mr-3"
                    contain
                  />

                  <div class="flex-grow-1">
                    <div
                      v-if="effectiveSettings.show_brand"
                      class="text-caption text--secondary"
                    >
                      {{ p.brand_name }}
                    </div>

                    <div
                      v-if="effectiveSettings.show_sku"
                      class="text-subtitle-2 font-weight-medium"
                    >
                      {{ p.sku }}
                    </div>

                    <div
                      v-if="effectiveSettings.show_description"
                      class="text-body-2 text--secondary item-desc"
                    >
                      {{ p.description }}
                    </div>

                    <div class="text-caption text--secondary mt-1">
                      <span v-if="effectiveSettings.show_price">
                        Precio: {{ p.price }}
                      </span>
                    </div>
                    <div class="text-caption text--secondary mt-1">
                      <span v-if="effectiveSettings.show_min_max">
                        Min: {{ p.min_qty }} · Max: {{ p.max_qty }}
                      </span>
                    </div>
                  </div>

                  <div
                    v-if="
                      effectiveSettings.show_images &&
                      p.images &&
                      p.images.length > 1
                    "
                    class="ml-2"
                  >
                    <v-chip x-small outlined>
                      +{{ p.images.length - 1 }}
                    </v-chip>
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

    paperStyle() {
      const portraitRatio = 11 / 8.5
      const landscapeRatio = 8.5 / 11

      const isLand = this.orientation === 'landscape'
      const ratio = isLand ? landscapeRatio : portraitRatio

      if (this.isPrint) {
        return {
          width: '100%',
          height: 'auto',
          aspectRatio: `${isLand ? '11 / 8.5' : '8.5 / 11'}`,
          margin: '0 auto',
          background: 'white',
        }
      }

      const width = 700
      const height = Math.round(width * ratio)

      return {
        width: `${width}px`,
        height: `${height}px`,
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
      return (this.page && this.page.layout) || 'grid_2x4'
    },

    capacity() {
      const map = {
        hero_1: 1,
        hero_2: 2,
        grid_2x3: 6,
        grid_2x4: 8,
        grid_2x5: 10,
        grid_2x6: 12,
        grid_3x3: 9,
        grid_3x4: 12,
        grid_3x5: 15,
        list_compact: 6,
      }
      return map[this.layoutKey] || 8
    },

    layout() {
      return (this.page && this.page.layout) || 'grid_2x4'
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
      return this.layout === 'hero_1' || this.layout === 'hero_2'
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
      if (this.layoutKey === 'grid_3x3') return { md: 4 }
      if (this.layoutKey === 'grid_2x3') return { md: 6 }
      if (this.layoutKey === 'grid_2x4') return { md: 6 }
      if (this.layoutKey === 'grid_2x5') return { md: 6 }
      if (this.layoutKey === 'grid_2x6') return { md: 6 }
      if (this.layoutKey === 'grid_3x4') return { md: 4 }
      if (this.layoutKey === 'grid_3x5') return { md: 4 }
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

    coverOverlayClass() {
      const overlay = this.effectiveTheme.cover_overlay
      if (overlay === 'dark') return 'cover-overlay-dark'
      if (overlay === 'light') return 'cover-overlay-light'
      return ''
    },
  },
}
</script>

<style scoped>
.item-desc {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.cover {
  width: 100%;
  height: 100%;
  position: relative;
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
}

.cat-card {
  border-color: rgba(0, 0, 0, 0.12);
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
  padding: 24px;
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

.cover-overlay-dark .cover-title {
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
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  border: 1px solid rgba(0, 0, 0, 0.12);
  border-radius: 6px;
  padding: 12px;
}

.hero-item.hero-2 {
  grid-template-columns: 1fr 1fr;
}

.hero-item.hero-1 {
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

.hero-thumbs {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 6px;
}

.hero-thumb {
  width: 100%;
  height: 56px;
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

.hero-note {
  font-size: 12px;
  opacity: 0.8;
}
</style>
