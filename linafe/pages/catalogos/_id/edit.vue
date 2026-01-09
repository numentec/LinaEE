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
            <v-btn small text @click="addCover">
              <v-icon left small>mdi-image-frame</v-icon> Portada
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
              <v-list-item-avatar tile class="mr-2 page-thumb">
                <div class="thumb-wrapper">
                  <v-sheet outlined class="thumb-sheet">
                    <v-row dense class="ma-0">
                      <v-col
                        v-for="(it, i) in thumbItemsByPage[p.id]"
                        :key="(it.product_id || it.sku) + '_' + i"
                        cols="6"
                        class="pa-0"
                      >
                        <v-img
                          :src="it.selected_image_url"
                          :lazy-src="it.selected_image_url"
                          height="34"
                          width="34"
                          contain
                        />
                      </v-col>
                    </v-row>
                    <!-- <div
                      v-if="(p.items && p.items.length) === 0"
                      class="thumb-empty text-caption text--secondary"
                    >
                      Vacía
                    </div> -->
                  </v-sheet>

                  <v-chip
                    v-if="hiddenCountByPage[p.id] > 0"
                    x-small
                    outlined
                    class="thumb-more"
                  >
                    +{{ hiddenCountByPage[p.id] }}
                  </v-chip>
                </div>
              </v-list-item-avatar>

              <v-list-item-content>
                <v-list-item-title>
                  {{ p.name || `Página ${idx + 1}` }}
                  <v-chip v-if="p.id === 'cover'" x-small class="ml-2" outlined>
                    PORTADA
                  </v-chip>
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
                    <v-list-item @click="openRename(idx)">
                      <v-list-item-title>Renombrar</v-list-item-title>
                    </v-list-item>

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
            <v-row dense justify="space-between" class="align-center">
              <div class="text-subtitle-2 font-weight-medium">Lienzo</div>

              <div class="text-caption text--secondary mr-3">
                {{ pageHeaderLabel }}
              </div>

              <div>
                <v-btn
                  small
                  outlined
                  :disabled="pageItems.length <= layoutCapacity"
                  @click="openDistributeDialog"
                >
                  Auto-distribuir
                </v-btn>
                <div class="text-caption text--secondary mt-1">
                  {{ showingLabel }}
                </div>
              </div>
            </v-row>
          </div>
          <v-sheet class="pa-6" outlined :style="paperStyle">
            <template v-if="isCoverPage">
              <div class="cover-hero" :style="coverHeroStyle">
                <div class="cover-overlay">
                  <v-img
                    v-if="coverLogoUrl"
                    :src="coverLogoUrl"
                    max-width="140"
                    contain
                    class="mb-4"
                  />
                  <div class="text-h4 font-weight-bold white--text">
                    {{ coverTitle }}
                  </div>
                  <div class="text-subtitle-1 white--text mt-2">
                    {{ coverSubtitle }}
                  </div>
                </div>
              </div>
            </template>

            <template v-else>
              <!-- tu render actual de productos -->
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
              <v-alert
                v-if="hiddenCount > 0"
                dense
                text
                type="info"
                class="mt-4"
              >
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
            </template>
          </v-sheet>
        </v-sheet>
      </v-col>

      <!-- Propiedades -->
      <v-col cols="12" md="3">
        <v-sheet outlined class="pa-3">
          <div class="text-subtitle-2 font-weight-medium mb-2">Propiedades</div>

          <div v-if="isCoverPage">
            <v-text-field
              :value="coverTitle"
              label="Título"
              outlined
              dense
              hide-details
              class="mb-3"
              @input="onCoverChange({ title: $event })"
            />

            <v-text-field
              :value="coverSubtitle"
              label="Subtítulo"
              outlined
              dense
              hide-details
              class="mb-3"
              @input="onCoverChange({ subtitle: $event })"
            />

            <v-text-field
              :value="coverLogoUrl"
              label="Logo URL"
              outlined
              dense
              hide-details
              class="mb-3"
              @input="onCoverChange({ logo_url: $event })"
            />

            <v-text-field
              :value="coverHeroUrl"
              label="Imagen de portada URL"
              outlined
              dense
              hide-details
              @input="onCoverChange({ hero_url: $event })"
            />
          </div>
          <div v-else>
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
          </div>

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

    <v-dialog v-model="showRenameDialog" max-width="520">
      <v-card>
        <v-card-title class="text-subtitle-1 font-weight-medium">
          Renombrar página
        </v-card-title>

        <v-card-text>
          <v-text-field
            ref="renameInput"
            v-model="renameValue"
            label="Nombre"
            outlined
            dense
            hide-details
            @keyup.enter="confirmRename"
          />
        </v-card-text>

        <v-card-actions>
          <v-btn text @click="closeRename">Cancelar</v-btn>
          <v-spacer />
          <v-btn color="primary" @click="confirmRename"> Guardar </v-btn>
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

      showRenameDialog: false,
      renameIndex: null,
      renameValue: '',

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

    pageHeaderLabel() {
      const n = this.activePageIndex + 1
      const total = this.pages.length

      const name = this.page && this.page.name ? this.page.name : `Página ${n}`

      return `${name} (${n}/${total})`
    },

    currentCatalog() {
      return this.$store.getters['catalogo/catalogos/current']
    },
    pages() {
      return (this.currentCatalog && this.currentCatalog.pages) || []
    },

    activePageIndex() {
      return this.$store.getters['catalogo/catalogos/activePageIndex'](
        this.$route.params.id
      )
    },
    activePage() {
      return this.pages[this.activePageIndex] || null
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

    thumbItemsByPage() {
      const out = {}
      this.pages.forEach((p) => {
        const items = Array.isArray(p.items) ? p.items : []
        out[p.id] = items.slice(0, 4)
      })
      return out
    },

    hiddenCountByPage() {
      const out = {}
      this.pages.forEach((p) => {
        const items = Array.isArray(p.items) ? p.items : []
        const n = items.length - 4
        out[p.id] = n > 0 ? n : 0
      })
      return out
    },

    isCoverPage() {
      return this.activePage && this.activePage.layout === 'cover'
    },

    coverData() {
      if (!this.page) return null
      return this.page.id === 'cover' ? this.page.cover || {} : null
    },

    cover() {
      if (!this.isCoverPage) return null
      return this.activePage.cover || {}
    },
    coverTitle() {
      return (this.cover && this.cover.title) || this.catalogName || 'Catálogo'
    },
    coverSubtitle() {
      return (this.cover && this.cover.subtitle) || ''
    },
    coverLogoUrl() {
      return (this.cover && this.cover.logo_url) || ''
    },
    coverHeroUrl() {
      return (this.cover && this.cover.hero_url) || ''
    },
    coverHeroStyle() {
      const url = this.coverHeroUrl
      return {
        backgroundImage: url ? `url('${url}')` : 'none',
        backgroundSize: 'cover',
        backgroundPosition: 'top center',
      }
    },
  },

  mounted() {
    this.$store.dispatch('catalogo/catalogos/init')
    this.$store.dispatch('catalogo/catalogos/setCurrent', this.$route.params.id)

    this.$store.dispatch('catalogo/catalogos/ensureCoverPage', {
      catalogId: this.$route.params.id,
    })

    // opcional: mostrar portada al abrir
    // this.$store.dispatch('catalogo/catalogos/setActivePage', {
    //   catalogId: this.$route.params.id,
    //   pageIndex: 0,
    // })
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

    openRename(idx) {
      const p = this.pages[idx]
      if (!p) return

      this.renameIndex = idx
      this.renameValue = p.name || `Página ${idx + 1}`
      this.showRenameDialog = true

      this.$nextTick(() => {
        const el = this.$refs.renameInput
        if (el && typeof el.focus === 'function') el.focus()
      })
    },

    closeRename() {
      this.showRenameDialog = false
      this.renameIndex = null
      this.renameValue = ''
    },

    async confirmRename() {
      const idx = this.renameIndex
      const p = typeof idx === 'number' ? this.pages[idx] : null
      if (!p) return

      const name = (this.renameValue || '').trim()
      if (!name) return

      const catalogId = this.$route.params.id

      await this.$store.dispatch('catalogo/catalogos/renamePage', {
        catalogId,
        pageId: p.id,
        name,
      })

      this.closeRename()
    },

    openPickerForIndex(idx) {
      this.pickerTargetIndex = idx
      this.showPicker = true
    },

    onAddHere(idx) {
      this.setActivePage(idx)
      this.openPickerForIndex(idx)
    },

    async addCover() {
      const catalogId = this.$route.params.id

      await this.$store.dispatch('catalogo/catalogos/ensureCoverPage', {
        catalogId,
      })

      this.setActivePage(0)
    },

    onCoverChange(patch) {
      const catalogId = this.$route.params.id

      this.$store.dispatch('catalogo/catalogos/updateCover', {
        catalogId,
        patch,
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

.page-thumb {
  position: relative;
  width: 76px;
  height: 76px;
}

.thumb-sheet {
  width: 72px;
  height: 72px;
  position: relative;
  overflow: hidden;
}

.thumb-more {
  position: absolute;
  right: 2px;
  bottom: 2px;
  background: white;
}

.thumb-empty {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* CSS Portada */
.cover {
  width: 100%;
  height: 100%;
  position: relative;
  border-radius: 6px;
  overflow: hidden;
}

.cover-hero {
  width: 100%;
  height: 520px;
  border-radius: 6px;
  position: relative;
  background-color: #f2f2f2;
}

.cover-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 24px;
  background: linear-gradient(180deg, rgba(0, 0, 0, 0.05), rgba(0, 0, 0, 0.55));
}
</style>
