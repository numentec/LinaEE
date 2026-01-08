<template>
  <v-container fluid>
    <v-card outlined class="pa-3 mb-3">
      <div class="d-flex align-center">
        <v-btn icon @click="$router.push('/catalogos')">
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
        <div class="ml-2">
          <div class="text-subtitle-1 font-weight-medium">
            {{ catalogName }}
          </div>
          <div class="text-caption text--secondary">
            {{ catalogTemplate }} · {{ catalogOrientation }}
          </div>
        </div>
        <v-spacer />
        <v-btn class="mr-2" color="primary" @click="openPicker">
          <v-icon left>mdi-package-variant-closed-plus</v-icon>
          Agregar productos
        </v-btn>
        <v-btn color="primary" @click="goPreview">
          <v-icon left>mdi-file-eye-outline</v-icon>
          Vista previa
        </v-btn>
      </div>
    </v-card>

    <v-row>
      <!-- Panel páginas -->
      <v-col cols="12" md="3">
        <v-sheet outlined class="pa-3">
          <div class="d-flex align-center mb-2">
            <div class="text-subtitle-2 font-weight-medium">Páginas</div>
            <v-spacer />
            <v-btn small text @click="openNewPageDialog">
              <v-icon left small>mdi-note-plus-outline</v-icon> Página
            </v-btn>
          </div>
          <div class="text-caption text--secondary">
            Total páginas: {{ pages.length }}
          </div>
          <v-list dense nav>
            <v-list-item
              v-for="(p, idx) in pages"
              :key="p.id"
              :input-value="idx === activePageIndex"
              @click="setActivePage(idx)"
            >
              <v-list-item-content>
                <v-list-item-title>
                  {{ p.name || `Página ${idx + 1}` }}
                </v-list-item-title>
                <v-list-item-subtitle>
                  {{ p.layout }} · {{ (p.items && p.items.length) || 0 }} items
                </v-list-item-subtitle>
              </v-list-item-content>

              <v-list-item-action class="d-flex align-center">
                <v-tooltip bottom>
                  <template #activator="{ on, attrs }">
                    <v-btn
                      icon
                      small
                      v-bind="attrs"
                      v-on="on"
                      @click.stop="onAddHere(idx)"
                    >
                      <v-icon small>mdi-package-variant-closed-plus</v-icon>
                    </v-btn>
                  </template>
                  <span>Agregar productos aquí</span>
                </v-tooltip>

                <v-tooltip bottom>
                  <template #activator="{ on, attrs }">
                    <v-btn
                      icon
                      small
                      v-bind="attrs"
                      :disabled="idx === 0"
                      v-on="on"
                      @click.stop="movePageUp(idx)"
                    >
                      <v-icon small>mdi-arrow-up</v-icon>
                    </v-btn>
                  </template>
                  <span>Mover arriba</span>
                </v-tooltip>

                <v-tooltip bottom>
                  <template #activator="{ on, attrs }">
                    <v-btn
                      icon
                      small
                      v-bind="attrs"
                      :disabled="idx === pages.length - 1"
                      v-on="on"
                      @click.stop="movePageDown(idx)"
                    >
                      <v-icon small>mdi-arrow-down</v-icon>
                    </v-btn>
                  </template>
                  <span>Mover abajo</span>
                </v-tooltip>

                <v-menu left bottom>
                  <template #activator="{ on, attrs }">
                    <v-btn icon small v-bind="attrs" v-on="on" @click.stop>
                      <v-icon small>mdi-dots-vertical</v-icon>
                    </v-btn>
                  </template>

                  <v-list dense>
                    <v-list-item @click="duplicatePage(idx)">
                      <v-list-item-title>Duplicar página</v-list-item-title>
                    </v-list-item>

                    <v-list-item @click="deletePage(idx)">
                      <v-list-item-title class="red--text">
                        Eliminar página
                      </v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-menu>
              </v-list-item-action>
            </v-list-item>
          </v-list>

          <div class="text-caption text--secondary mt-2">
            (MVP) Luego agregaremos miniaturas y reordenamiento.
          </div>
        </v-sheet>
      </v-col>

      <!-- Canvas -->
      <v-col cols="12" md="6">
        <v-sheet outlined class="pa-4">
          <div class="d-flex align-center mb-3">
            <div class="text-subtitle-2 font-weight-medium">Lienzo</div>

            <v-spacer />

            <div class="text-caption text--secondary mr-3">
              Página {{ activePageIndex + 1 }} de {{ pages.length }}
            </div>

            <div class="text-caption text--secondary mr-3">
              {{ showingLabel }}
            </div>

            <v-btn
              small
              outlined
              :disabled="pageItems.length <= layoutCapacity"
              @click="openDistributeDialog"
            >
              Auto-distribuir
            </v-btn>
          </div>

          <v-sheet class="pa-6" outlined :style="paperStyle">
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
                      :src="p.selected_image_url"
                      :lazy-src="p.selected_image_url"
                      width="72"
                      height="72"
                      class="mr-3"
                      contain
                    />

                    <div class="flex-grow-1">
                      <div class="text-caption text--secondary">
                        {{ p.brand_name }}
                      </div>

                      <div class="text-subtitle-2 font-weight-medium">
                        {{ p.sku }}
                      </div>

                      <div class="text-body-2 text--secondary item-desc">
                        {{ p.description }}
                      </div>

                      <div class="text-caption text--secondary mt-1">
                        Precio: {{ p.price }} · Min: {{ p.min_qty }} · Max:
                        {{ p.max_qty }}
                      </div>
                    </div>

                    <div v-if="p.images && p.images.length > 1" class="ml-2">
                      <v-chip x-small outlined>
                        +{{ p.images.length - 1 }}
                      </v-chip>
                    </div>
                  </div>
                </v-card>
              </v-col>
            </v-row>

            <v-alert v-if="hiddenCount > 0" dense text type="info" class="mt-4">
              Hay {{ hiddenCount }} productos más. Usa
              <strong>Auto-distribuir</strong> para crear páginas.
            </v-alert>

            <v-sheet
              v-if="pageItems.length === 0"
              class="pa-8 text-center"
              outlined
            >
              <div class="text-subtitle-1 font-weight-medium mb-1">
                Catálogo vacío
              </div>
              <div class="text-body-2 text--secondary">
                Agrega productos para comenzar.
              </div>
            </v-sheet>
          </v-sheet>
        </v-sheet>
      </v-col>

      <!-- Propiedades -->
      <v-col cols="12" md="3">
        <v-sheet outlined class="pa-3">
          <div class="text-subtitle-2 font-weight-medium mb-2">Propiedades</div>

          <v-select
            :value="layoutKey"
            :items="layoutItems"
            label="Layout de página"
            outlined
            dense
            hide-details
            class="mb-4"
            @change="onLayoutChange"
          />

          <v-switch label="Mostrar precios" :value="true" disabled />
          <v-switch label="Mostrar marca" :value="true" disabled />
          <v-switch label="Mostrar min/max compra" :value="true" disabled />

          <div class="text-caption text--secondary">
            (MVP) El layout afecta cuántos productos entran por página.
          </div>
        </v-sheet>
      </v-col>
    </v-row>
    <!-- Diálogos -->
    <v-dialog v-model="showDistributeDialog" max-width="520">
      <v-card>
        <v-card-title class="text-subtitle-1 font-weight-medium">
          Auto-distribuir productos
        </v-card-title>

        <v-card-text>
          <div class="text-body-2 text--secondary mb-4">
            Esto repartirá todos los productos del catálogo en páginas nuevas.
          </div>

          <v-select
            :value="distributeLayout"
            :items="layoutItems"
            label="Layout"
            outlined
            dense
            hide-details
            class="mb-4"
            @change="onDistributeLayoutChange"
          />

          <v-select
            v-model="distributeCapacity"
            :items="capacityItems"
            label="Productos por página"
            outlined
            dense
            hide-details
          />

          <v-alert dense text type="info" class="mt-4">
            Tip: Para catálogos grandes, <strong>Grid 2 x 4</strong> suele ser
            el mejor balance entre lectura y número de páginas.
          </v-alert>
        </v-card-text>

        <v-card-actions>
          <v-btn text @click="showDistributeDialog = false">Cancelar</v-btn>
          <v-spacer />
          <v-btn color="primary" @click="confirmDistribute"> Distribuir </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="showNewPageDialog" max-width="520">
      <v-card>
        <v-card-title class="text-subtitle-1 font-weight-medium">
          Nueva página
        </v-card-title>

        <v-card-text>
          <v-select
            v-model="newPageLayout"
            :items="layoutItems"
            label="Layout"
            outlined
            dense
            hide-details
            class="mb-4"
          />

          <v-switch
            v-model="newPageAddProducts"
            label="Abrir selector de productos al crear"
          />

          <v-alert dense text type="info" class="mt-4">
            Crear una página vacía te permite armar secciones por temas o por
            categorías sin redistribuir todo el catálogo.
          </v-alert>
        </v-card-text>

        <v-card-actions>
          <v-btn text @click="showNewPageDialog = false">Cancelar</v-btn>
          <v-spacer />
          <v-btn color="primary" @click="createNewPage"> Crear </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <ProductPickerDialog v-model="showPicker" @add="onAddProducts" />
  </v-container>
</template>

<script>
import ProductPickerDialog from '~/components/catalogos/ProductPickerDialog.vue'

export default {
  name: 'CatalogosEditPage',

  components: { ProductPickerDialog },

  data() {
    return {
      showPicker: false,
      showDistributeDialog: false,

      showNewPageDialog: false,
      newPageLayout: 'grid_2x4',
      newPageAddProducts: true,

      pickerTargetIndex: null,

      distributeLayout: 'grid_2x4',
      distributeCapacity: 8,
      capacityItems: [6, 8, 9, 12, 16],

      layoutItems: [
        { text: 'Grid 2 x 4 (8)', value: 'grid_2x4' },
        { text: 'Grid 3 x 3 (9)', value: 'grid_3x3' },
        { text: 'Grid 2 x 3 (6)', value: 'grid_2x3' },
        { text: 'Lista compacta (16)', value: 'list_compact' },
      ],
    }
  },

  computed: {
    catalog() {
      return this.$store.getters['catalogo/catalogos/byId'](
        this.$route.params.id
      )
    },

    catalogName() {
      return (this.catalog && this.catalog.name) || 'Catálogo'
    },

    catalogTemplate() {
      return (this.catalog && this.catalog.template) || 'Template'
    },

    catalogOrientation() {
      return this.catalog?.orientation === 'portrait'
        ? 'Vertical'
        : 'Horizontal'
    },

    paperStyle() {
      // Carta a un ancho fijo; alto según orientación (ratio aproximado)
      const width = 700 // px
      const portraitRatio = 11 / 8.5 // alto/ancho
      const landscapeRatio = 8.5 / 11
      const isLand = this.catalog && this.catalog.orientation === 'landscape'
      const ratio = isLand ? landscapeRatio : portraitRatio
      const height = Math.round(width * ratio)

      return {
        width: `${width}px`,
        height: `${height}px`,
        margin: '0 auto',
        background: 'white',
      }
    },

    pages() {
      if (!this.catalog) return []
      return Array.isArray(this.catalog.pages) ? this.catalog.pages : []
    },

    activePageIndex() {
      return this.$store.getters['catalogo/catalogos/activePageIndex'](
        this.$route.params.id
      )
    },

    page() {
      // if (!this.catalog) return null
      // const pages = Array.isArray(this.catalog.pages) ? this.catalog.pages : []
      // return pages[0] || null
      return this.pages[this.activePageIndex] || null
    },

    layoutKey() {
      return (this.page && this.page.layout) || 'grid_2x4'
    },

    layoutCapacity() {
      const map = {
        grid_2x4: 8,
        grid_3x3: 9,
        grid_2x3: 6,
        list_compact: 16,
      }
      return map[this.layoutKey] || 8
    },

    pageItems() {
      const items =
        this.page && Array.isArray(this.page.items) ? this.page.items : []
      return items
    },

    visibleItems() {
      return this.pageItems.slice(0, this.layoutCapacity)
    },

    hiddenCount() {
      const n = this.pageItems.length - this.visibleItems.length
      return n > 0 ? n : 0
    },

    showingLabel() {
      const total = this.pageItems.length
      const shown = this.visibleItems.length
      return `Mostrando ${shown} de ${total}`
    },

    gridCols() {
      if (this.layoutKey === 'list_compact') return { md: 12 }
      if (this.layoutKey === 'grid_3x3') return { md: 4 }
      if (this.layoutKey === 'grid_2x3') return { md: 6 }
      return { md: 6 }
    },
  },
  mounted() {
    this.$store.dispatch('catalogo/catalogos/init')
    this.$store.dispatch('catalogo/catalogos/setCurrent', this.$route.params.id)
  },
  methods: {
    goPreview() {
      this.$router.push(`/catalogos/${this.$route.params.id}/preview`)
    },

    openPicker() {
      // this.showPicker = true
      this.openPickerForIndex(this.activePageIndex)
    },

    async onAddProducts(products) {
      const catalogId = this.$route.params.id

      const idx =
        typeof this.pickerTargetIndex === 'number'
          ? this.pickerTargetIndex
          : this.activePageIndex

      const p = this.pages[idx]
      const pageId = p ? p.id : 'page_1'

      await this.$store.dispatch('catalogo/catalogos/addProductsToPage', {
        catalogId,
        pageId,
        products,
      })

      this.pickerTargetIndex = null
    },

    autoDistribute() {
      const catalogId = this.$route.params.id

      this.$store.dispatch('catalogo/catalogos/autoDistribute', {
        catalogId,
        layout: this.layoutKey,
        capacity: this.layoutCapacity,
      })

      this.setActivePage(0)
    },

    setActivePage(pageIndex) {
      const catalogId = this.$route.params.id

      this.$store.dispatch('catalogo/catalogos/setActivePage', {
        catalogId,
        pageIndex,
      })
    },

    onLayoutChange(layout) {
      const catalogId = this.$route.params.id
      const pageId = this.page ? this.page.id : null

      if (!pageId) return

      this.$store.dispatch('catalogo/catalogos/setPageLayout', {
        catalogId,
        pageId,
        layout,
      })
    },

    capacityForLayout(layout) {
      const map = {
        grid_2x4: 8,
        grid_3x3: 9,
        grid_2x3: 6,
        list_compact: 16,
      }
      return map[layout] || 8
    },

    openDistributeDialog() {
      this.distributeLayout = this.layoutKey
      this.distributeCapacity = this.capacityForLayout(this.layoutKey)
      this.showDistributeDialog = true
    },

    onDistributeLayoutChange(layout) {
      this.distributeLayout = layout
      this.distributeCapacity = this.capacityForLayout(layout)
    },

    async confirmDistribute() {
      const catalogId = this.$route.params.id

      await this.$store.dispatch('catalogo/catalogos/autoDistribute', {
        catalogId,
        layout: this.distributeLayout,
        capacity: this.distributeCapacity,
      })

      this.setActivePage(0)
      this.showDistributeDialog = false
    },

    openNewPageDialog() {
      this.newPageLayout = this.layoutKey
      this.newPageAddProducts = true
      this.showNewPageDialog = true
    },

    async createNewPage() {
      const catalogId = this.$route.params.id

      const idx = await this.$store.dispatch(
        'catalogo/catalogos/addEmptyPage',
        {
          catalogId,
          layout: this.newPageLayout,
        }
      )

      await this.setActivePage(idx)

      this.showNewPageDialog = false

      if (this.newPageAddProducts) {
        this.openPickerForIndex(idx)
      }
    },

    openPickerForIndex(idx) {
      this.pickerTargetIndex = idx
      this.showPicker = true
    },

    onAddHere(idx) {
      this.setActivePage(idx)
      this.openPickerForIndex(idx)
    },

    async duplicatePage(idx) {
      const catalogId = this.$route.params.id

      await this.$store.dispatch('catalogo/catalogos/duplicatePage', {
        catalogId,
        pageIndex: idx,
      })
    },

    async deletePage(idx) {
      const ok = window.confirm('¿Eliminar esta página?')
      if (!ok) return

      const catalogId = this.$route.params.id

      await this.$store.dispatch('catalogo/catalogos/deletePage', {
        catalogId,
        pageIndex: idx,
      })
    },

    async movePageUp(idx) {
      if (idx <= 0) return
      const catalogId = this.$route.params.id

      await this.$store.dispatch('catalogo/catalogos/movePage', {
        catalogId,
        fromIndex: idx,
        toIndex: idx - 1,
      })
    },

    async movePageDown(idx) {
      if (idx >= this.pages.length - 1) return
      const catalogId = this.$route.params.id

      await this.$store.dispatch('catalogo/catalogos/movePage', {
        catalogId,
        fromIndex: idx,
        toIndex: idx + 1,
      })
    },
  },
}
</script>

<style scoped>
.item-desc {
  display: -webkit-box;
  -webkit-line-clamp: 2; /* For older browsers */
  line-clamp: 2; /* Standard property */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
