<template>
  <v-sheet class="pa-6" outlined :style="paperStyle">
    <template v-if="isCover">
      <div class="cover">
        <div
          v-if="coverHeroUrl"
          class="cover-hero"
          :style="{ backgroundImage: `url('${coverHeroUrl}')` }"
        />
        <div class="cover-overlay">
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
            <div class="title-overlay pa-3 rounded">
              <div class="text-h5 font-weight-bold">
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
      <v-row dense>
        <v-col
          v-for="p in visibleItems"
          :key="p.product_id || p.sku"
          cols="12"
          v-bind="gridCols"
        >
          <v-card outlined class="pa-2">
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

                  <span
                    v-if="
                      effectiveSettings.show_price &&
                      effectiveSettings.show_min_max
                    "
                  >
                    ·
                  </span>

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
                <v-chip x-small outlined> +{{ p.images.length - 1 }} </v-chip>
              </div>
            </div>
          </v-card>
        </v-col>
      </v-row>

      <v-alert v-if="hiddenCount > 0" dense text type="info" class="mt-4">
        Hay {{ hiddenCount }} productos más en esta página
      </v-alert>
    </template>
  </v-sheet>
</template>

<script>
export default {
  name: 'CatalogPageRender',

  props: {
    page: { type: Object, required: true },
    orientation: { type: String, default: 'portrait' },
    settings: { type: Object, default: () => ({}) },
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
      const width = 700
      const portraitRatio = 11 / 8.5
      const landscapeRatio = 8.5 / 11

      const isLand = this.orientation === 'landscape'
      const ratio = isLand ? landscapeRatio : portraitRatio
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
        grid_2x4: 8,
        grid_3x3: 9,
        grid_2x3: 6,
        list_compact: 16,
      }
      return map[this.layoutKey] || 8
    },

    items() {
      const items =
        this.page && Array.isArray(this.page.items) ? this.page.items : []
      return items
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
      if (this.layoutKey === 'grid_3x3') return { md: 4 }
      if (this.layoutKey === 'grid_2x3') return { md: 6 }
      return { md: 6 }
    },
  },
}
</script>

<style scoped>
.item-desc {
  display: -webkit-box;
  -webkit-line-clamp: 2;
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

.cover-overlay {
  position: absolute;
  inset: 0;
  padding: 24px;
  /* background: linear-gradient(
    rgba(255, 255, 255, 0.92),
    rgba(255, 255, 255, 0.78)
  ); */
}

.title-overlay {
  background: linear-gradient(
    rgba(255, 255, 255, 0.92),
    rgba(255, 255, 255, 0.78)
  );
}
</style>
