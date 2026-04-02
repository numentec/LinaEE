<template>
  <v-dialog v-model="openLocal" fullscreen scrollable>
    <v-card class="picker-card">
      <v-toolbar flat color="grey lighten-4">
        <v-btn icon @click="close">
          <v-icon>mdi-close</v-icon>
        </v-btn>

        <v-toolbar-title>Selector de productos</v-toolbar-title>
        <v-spacer />

        <v-chip class="mr-2" outlined>
          Seleccionados: {{ selectedMapSize }}
        </v-chip>

        <v-chip class="mr-2" outlined> Total: {{ totalCount }} </v-chip>

        <template v-if="isCompactActions">
          <v-btn
            icon
            class="mr-1"
            :loading="loadingProductos"
            title="Buscar"
            @click="fetchProducts({ resetOffset: true })"
          >
            <v-icon>mdi-cloud-search-outline</v-icon>
          </v-btn>

          <v-btn
            icon
            class="mr-1"
            title="Limpiar filtros"
            @click="clearFilters"
          >
            <v-icon>mdi-filter-remove-outline</v-icon>
          </v-btn>

          <v-btn
            icon
            color="primary"
            :disabled="selectedMapSize === 0"
            title="Agregar seleccionados"
            @click="addSelected"
          >
            <v-icon>mdi-checkbox-marked-circle-plus-outline</v-icon>
          </v-btn>
        </template>

        <v-btn
          v-else
          color="primary"
          :disabled="selectedMapSize === 0"
          @click="addSelected"
        >
          <v-icon left>mdi-checkbox-marked-circle-plus-outline</v-icon>
          AGREGAR SELECCIONADOS
        </v-btn>
      </v-toolbar>

      <v-card-text class="picker-body">
        <v-row class="mb-2" dense>
          <v-col cols="12" md="5">
            <v-text-field
              v-model="search"
              outlined
              dense
              clearable
              hide-details="auto"
              label="Buscar por SKU / descripción / marca"
              prepend-inner-icon="mdi-magnify"
              @keyup.enter="onSearchSubmit"
            />
          </v-col>

          <v-col cols="12" md="5">
            <v-select
              v-model="brand"
              :items="brandItems"
              item-text="text"
              item-value="value"
              outlined
              dense
              clearable
              hide-details="auto"
              label="Marca"
            />
          </v-col>
          <v-col
            v-if="!isCompactActions"
            cols="12"
            md="2"
            class="d-flex align-center"
          >
            <v-btn
              color="primary"
              class="mr-2"
              :loading="loadingProductos"
              @click="fetchProducts({ resetOffset: true })"
            >
              <v-icon left>mdi-cloud-search-outline</v-icon>
              Buscar
            </v-btn>

            <v-btn text @click="clearFilters">
              <v-icon left>mdi-filter-remove-outline</v-icon>
              Limpiar
            </v-btn>
          </v-col>
        </v-row>

        <v-row class="mb-2" dense>
          <v-col cols="12" md="4">
            <v-select
              v-model="departamento"
              :items="departamentoItems"
              item-text="text"
              item-value="value"
              outlined
              dense
              clearable
              hide-details="auto"
              label="Departamento"
            />
          </v-col>

          <v-col cols="12" md="3">
            <v-select
              v-model="categoria"
              :items="categoriaItems"
              item-text="text"
              item-value="value"
              outlined
              dense
              clearable
              hide-details="auto"
              label="Categoría"
            />
          </v-col>

          <v-col cols="12" md="3">
            <v-select
              v-model="subcategoria"
              :items="subcategoriaItems"
              item-text="text"
              item-value="value"
              outlined
              dense
              clearable
              hide-details="auto"
              label="Subcategoría"
            />
          </v-col>

          <v-col cols="12" md="2" class="d-flex align-center justify-end">
            <v-chip small outlined>Bloques de 24</v-chip>
          </v-col>
        </v-row>

        <v-alert v-if="errorMessage" type="warning" dense text class="mb-3">
          {{ errorMessage }}
        </v-alert>

        <div
          ref="productsScroll"
          class="picker-scroll"
          @scroll.passive="onProductsScroll"
        >
          <v-skeleton-loader
            v-if="loadingProductos && !productos.length"
            type="list-item-avatar-three-line@8"
          />

          <template v-else>
            <v-list two-line>
              <v-list-item
                v-for="item in productos"
                :key="item.product_id || item.sku"
                class="px-1"
              >
                <v-list-item-action>
                  <v-checkbox
                    hide-details
                    :input-value="isSelected(item)"
                    @change="toggle(item)"
                  />
                </v-list-item-action>

                <v-list-item-avatar tile size="64">
                  <v-img
                    :src="item.selected_image_url"
                    :lazy-src="item.selected_image_url"
                    contain
                  />
                </v-list-item-avatar>

                <v-list-item-content>
                  <v-list-item-title class="font-weight-medium">
                    {{ item.sku }} · {{ item.brand_name }}
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    {{ item.description }}
                  </v-list-item-subtitle>
                  <v-list-item-subtitle class="text-caption">
                    Precio: {{ item.price }} · Min: {{ item.min_qty }} · Max:
                    {{ item.max_qty }} ·
                    {{ item.departamento || 'Sin departamento' }}
                  </v-list-item-subtitle>
                </v-list-item-content>

                <v-list-item-action>
                  <v-btn icon @click="quickSelectOnly(item)">
                    <v-icon>mdi-plus</v-icon>
                  </v-btn>
                </v-list-item-action>
              </v-list-item>
            </v-list>

            <div
              v-if="!loadingProductos && !productos.length"
              class="text-center py-8 text--secondary"
            >
              No se encontraron productos para los filtros seleccionados.
            </div>

            <div v-if="loadingProductos && productos.length" class="py-3 px-2">
              <v-progress-linear indeterminate color="primary" rounded />
            </div>
          </template>
        </div>

        <div class="d-flex align-center justify-space-between pt-4">
          <div class="text-caption text--secondary">
            Mostrando {{ productos.length }} de {{ totalCount }} registros
          </div>

          <div class="d-flex align-center">
            <v-btn
              small
              text
              class="mr-2"
              :disabled="!productos.length || allLoadedSelected"
              @click="selectAllLoaded"
            >
              Seleccionar todo
            </v-btn>

            <div class="text-caption text--secondary">
              {{
                hasNext
                  ? 'Desplaza hacia abajo para cargar más'
                  : 'Fin de resultados'
              }}
            </div>
          </div>
        </div>

        <v-sheet
          v-if="selectedProducts.length"
          class="selected-tray mt-4 pa-3"
          outlined
          rounded
        >
          <div class="d-flex align-center mb-2">
            <div class="font-weight-medium">
              Seleccionados ({{ selectedProducts.length }})
            </div>
            <v-spacer />
            <v-btn small text color="error" @click="clearSelection">
              Limpiar selección
            </v-btn>
          </div>

          <div class="selected-chips-wrap">
            <v-chip
              v-for="item in selectedProducts"
              :key="item.product_id || item.sku"
              small
              close
              class="mr-2 mb-2"
              @click:close="removeSelected(item)"
            >
              {{ item.sku }}
            </v-chip>
          </div>
        </v-sheet>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'ProductPickerDialog',
  props: {
    value: { type: Boolean, default: false },
    companyId: { type: [String, Number], default: null },
  },

  data() {
    return {
      openLocal: this.value,
      search: '',
      brand: null,
      departamento: null,
      categoria: null,
      subcategoria: null,
      pageSize: 24,
      offset: 0,
      totalCount: 0,
      nextUrl: null,
      previousUrl: null,
      selected: {},
      productos: [],
      loadingProductos: false,
      loadingFilters: false,
      errorMessage: '',
      brandItems: [],
      departamentoItems: [],
      categoriaItems: [],
      subcategoriaItems: [],
    }
  },

  computed: {
    ...mapGetters('sistema', ['getCurCia']),

    resolvedCompanyId() {
      if (this.companyId !== null && this.companyId !== undefined) {
        return String(this.companyId)
      }

      const c = this.getCurCia || {}
      return String(c.extrel || c.codigo || c.id || '01')
    },

    selectedMapSize() {
      return Object.keys(this.selected).length
    },

    selectedProducts() {
      return Object.values(this.selected)
    },

    hasNext() {
      return Boolean(this.nextUrl)
    },

    isCompactActions() {
      return Boolean(
        this.$vuetify &&
          this.$vuetify.breakpoint &&
          this.$vuetify.breakpoint.mdAndDown
      )
    },

    loadedSelectedCount() {
      return this.productos.reduce((acc, item) => {
        const id = item && item.product_id
        return id && this.selected[id] ? acc + 1 : acc
      }, 0)
    },

    allLoadedSelected() {
      return (
        this.productos.length > 0 &&
        this.loadedSelectedCount === this.productos.length
      )
    },
  },

  watch: {
    value(val) {
      this.openLocal = val
      if (val) {
        this.bootstrapDialog()
      }
    },
    openLocal(val) {
      this.$emit('input', val)
      if (val) {
        this.bootstrapDialog()
      }
    },
  },

  methods: {
    normalizeListItems(data) {
      const rows = Array.isArray(data) ? data : []
      const out = []
      const seen = new Set()

      rows.forEach((row) => {
        if (!row || typeof row !== 'object') return

        const rawValue = row.id
        const text = row.name

        if (rawValue === null || rawValue === undefined) return
        if (!text || !String(text).trim()) return

        const item = {
          text: String(text).trim(),
          value: String(rawValue).trim(),
        }

        const key = `${item.text}|${item.value}`
        if (seen.has(key)) return

        seen.add(key)
        out.push(item)
      })

      return out.sort((a, b) => a.text.localeCompare(b.text))
    },

    async fetchFilterList(listType) {
      const data = await this.$axios.$get(
        `/catalog/api/list/${this.resolvedCompanyId}/${listType}/`
      )
      return this.normalizeListItems(data)
    },

    async loadFilterOptions() {
      if (this.loadingFilters) return
      this.loadingFilters = true

      try {
        const [brands, deps, cats, scats] = await Promise.all([
          this.fetchFilterList('mar'),
          this.fetchFilterList('dep'),
          this.fetchFilterList('cat'),
          this.fetchFilterList('scat'),
        ])

        this.brandItems = brands
        this.departamentoItems = deps
        this.categoriaItems = cats
        this.subcategoriaItems = scats
      } catch (error) {
        this.errorMessage =
          'No fue posible cargar las listas de filtros. Puedes seguir buscando por texto.'
      } finally {
        this.loadingFilters = false
      }
    },

    getOffsetFromUrl(url, fallback = 0) {
      if (!url) return fallback

      try {
        const base = window.location.origin
        const parsed = new URL(url, base)
        const off = Number(parsed.searchParams.get('offset'))
        return Number.isFinite(off) && off >= 0 ? off : fallback
      } catch (_) {
        return fallback
      }
    },

    async fetchProducts({
      resetOffset = false,
      append = false,
      forcedOffset = null,
    } = {}) {
      if (this.loadingProductos) return
      this.errorMessage = ''

      if (resetOffset) this.offset = 0
      const requestOffset = Number.isFinite(forcedOffset)
        ? forcedOffset
        : this.offset

      this.loadingProductos = true
      try {
        const data = await this.$axios.$get('/catalog/api/productos/', {
          params: {
            limit: this.pageSize,
            offset: requestOffset,
            cia: this.resolvedCompanyId,
            search: this.search || undefined,
            brand: this.brand || undefined,
            departamento: this.departamento || undefined,
            categoria: this.categoria || undefined,
            subcategoria: this.subcategoria || undefined,
          },
        })

        const rows = Array.isArray(data) ? data : data.results || []
        if (append) {
          const merged = [...this.productos, ...rows]
          const seen = new Set()
          this.productos = merged.filter((item) => {
            const key = item.product_id || item.sku
            if (!key || seen.has(key)) return false
            seen.add(key)
            return true
          })
        } else {
          this.productos = rows
        }

        this.offset = requestOffset
        this.totalCount = Number(data.count || rows.length || 0)
        this.nextUrl = data.next || null
        this.previousUrl = data.previous || null
      } catch (error) {
        if (!append) {
          this.productos = []
          this.totalCount = 0
          this.nextUrl = null
          this.previousUrl = null
        }
        this.errorMessage =
          'No fue posible cargar productos para los filtros seleccionados.'
      } finally {
        this.loadingProductos = false
      }
    },

    async bootstrapDialog() {
      this.selected = {}
      await this.loadFilterOptions()
      await this.fetchProducts({ resetOffset: true })
    },

    onSearchSubmit() {
      this.fetchProducts({ resetOffset: true })
    },

    clearFilters() {
      this.search = ''
      this.brand = null
      this.departamento = null
      this.categoria = null
      this.subcategoria = null
      this.fetchProducts({ resetOffset: true })
    },

    onProductsScroll(event) {
      if (!this.hasNext || this.loadingProductos) return

      const target = event && event.target
      if (!target) return

      const threshold = 140
      const reachedBottom =
        target.scrollTop + target.clientHeight >=
        target.scrollHeight - threshold

      if (!reachedBottom) return

      const nextOffset = this.getOffsetFromUrl(
        this.nextUrl,
        this.offset + this.pageSize
      )
      this.fetchProducts({ append: true, forcedOffset: nextOffset })
    },

    selectAllLoaded() {
      const next = { ...this.selected }
      this.productos.forEach((item) => {
        const id = item && item.product_id
        if (!id) return
        next[id] = item
      })
      this.selected = next
    },

    removeSelected(item) {
      const id = item && item.product_id
      if (!id) return
      const next = { ...this.selected }
      delete next[id]
      this.selected = next
    },

    clearSelection() {
      this.selected = {}
    },

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
.picker-card {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.picker-body {
  flex: 1 1 auto;
  min-height: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.picker-scroll {
  flex: 1 1 auto;
  min-height: 0;
  overflow-y: auto;
}

.selected-tray {
  position: sticky;
  bottom: 0;
  background: #fff;
  z-index: 2;
}

.selected-chips-wrap {
  max-height: 86px;
  overflow-y: auto;
}
</style>
