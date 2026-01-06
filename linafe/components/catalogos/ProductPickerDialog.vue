<template>
  <v-dialog v-model="openLocal" fullscreen scrollable>
    <v-card>
      <v-toolbar flat>
        <v-btn icon @click="close">
          <v-icon>mdi-close</v-icon>
        </v-btn>

        <v-toolbar-title>Agregar productos</v-toolbar-title>
        <v-spacer />

        <v-chip class="mr-2" outlined>
          Seleccionados: {{ selectedMapSize }}
        </v-chip>

        <v-btn
          color="primary"
          :disabled="selectedMapSize === 0"
          @click="addSelected"
        >
          Agregar seleccionados
        </v-btn>
      </v-toolbar>

      <v-card-text>
        <v-row class="mb-2">
          <v-col cols="12" md="6">
            <v-text-field
              v-model="search"
              outlined
              dense
              hide-details
              label="Buscar por SKU / descripción / marca"
              prepend-inner-icon="mdi-magnify"
            />
          </v-col>

          <v-col cols="12" md="3">
            <v-select
              v-model="brand"
              :items="brandItems"
              outlined
              dense
              hide-details
              label="Marca"
            />
          </v-col>

          <v-col cols="12" md="3">
            <v-select
              v-model="sort"
              :items="sortItems"
              outlined
              dense
              hide-details
              label="Ordenar"
            />
          </v-col>
        </v-row>

        <v-virtual-scroll
          :items="filtered"
          :item-height="92"
          class="picker-scroll"
        >
          <template #default="{ item }">
            <div class="d-flex align-center py-2 px-2">
              <v-checkbox
                class="mt-0 pt-0"
                hide-details
                :input-value="isSelected(item)"
                @change="toggle(item)"
              />

              <v-img
                :src="item.selected_image_url"
                :lazy-src="item.selected_image_url"
                width="64"
                height="64"
                class="mr-3"
                contain
              />

              <div class="flex-grow-1">
                <div class="text-subtitle-2 font-weight-medium">
                  {{ item.sku }} · {{ item.brand_name }}
                </div>
                <div class="text-body-2 text--secondary">
                  {{ item.description }}
                </div>
                <div class="text-caption text--secondary">
                  Precio: {{ item.price }} · Min: {{ item.min_qty }} · Max:
                  {{ item.max_qty }}
                </div>
              </div>

              <v-btn icon @click="quickSelectOnly(item)">
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </div>

            <v-divider />
          </template>
        </v-virtual-scroll>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import { mockProductos } from '~/mock/productos'

export default {
  name: 'ProductPickerDialog',
  props: {
    value: { type: Boolean, default: false },
  },

  data() {
    return {
      openLocal: this.value,
      search: '',
      brand: 'all',
      sort: 'sku_asc',
      selected: {},
      productos: mockProductos,
      brandItems: [
        { text: 'Todas', value: 'all' },
        { text: 'Nike', value: 'Nike' },
        { text: 'Adidas', value: 'Adidas' },
        { text: 'Puma', value: 'Puma' },
        { text: 'Lina', value: 'Lina' },
      ],
      sortItems: [
        { text: 'SKU (A-Z)', value: 'sku_asc' },
        { text: 'Marca (A-Z)', value: 'brand_asc' },
        { text: 'Precio (asc)', value: 'price_asc' },
        { text: 'Precio (desc)', value: 'price_desc' },
      ],
    }
  },

  computed: {
    selectedMapSize() {
      return Object.keys(this.selected).length
    },

    filtered() {
      let out = [...this.productos]

      if (this.brand !== 'all') {
        out = out.filter((p) => p.brand_name === this.brand)
      }

      const q = (this.search || '').trim().toLowerCase()
      if (q) {
        out = out.filter((p) => {
          const sku = (p.sku || '').toLowerCase()
          const d = (p.description || '').toLowerCase()
          const b = (p.brand_name || '').toLowerCase()
          return sku.includes(q) || d.includes(q) || b.includes(q)
        })
      }

      if (this.sort === 'sku_asc') {
        out.sort((a, b) => (a.sku || '').localeCompare(b.sku || ''))
      } else if (this.sort === 'brand_asc') {
        out.sort((a, b) =>
          (a.brand_name || '').localeCompare(b.brand_name || '')
        )
      } else if (this.sort === 'price_asc') {
        out.sort((a, b) => (a.price || 0) - (b.price || 0))
      } else if (this.sort === 'price_desc') {
        out.sort((a, b) => (b.price || 0) - (a.price || 0))
      }

      return out
    },
  },

  watch: {
    value(val) {
      this.openLocal = val
      if (val) this.selected = {}
    },
    openLocal(val) {
      this.$emit('input', val)
    },
  },

  //   watch: {
  //     value(val) {
  //       this.openLocal = val
  //       if (val) {
  //         this.selected = {}
  //         // Forzar re-render del virtual scroll después de abrir
  //         this.$nextTick(() => {
  //           window.dispatchEvent(new Event('resize'))
  //         })
  //       }
  //     },
  //     openLocal(val) {
  //       this.$emit('input', val)
  //       if (val) {
  //         // Segundo intento para asegurar el render
  //         setTimeout(() => {
  //           window.dispatchEvent(new Event('resize'))
  //         }, 100)
  //       }
  //     },
  //   },

  activated() {
    if (this.openLocal) {
      // Forzar render del virtual scroll después de abrir
      this.$nextTick(() => {
        window.dispatchEvent(new Event('resize'))
      })
    }
  },

  methods: {
    close() {
      this.openLocal = false
    },

    isSelected(item) {
      return Boolean(this.selected[item.product_id])
    },

    toggle(item) {
      const id = item.product_id
      const next = { ...this.selected }

      if (next[id]) {
        delete next[id]
      } else {
        next[id] = item
      }

      this.selected = next
    },

    quickSelectOnly(item) {
      this.selected = { [item.product_id]: item }
    },

    addSelected() {
      const products = Object.values(this.selected)

      this.$emit('add', products)
      this.close()
    },
  },
}
</script>

<style scoped>
.picker-scroll {
  height: calc(100vh - 160px);
}
</style>
