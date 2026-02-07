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
        <v-btn
          color="primary"
          class="mr-2"
          :disabled="isCoverPage"
          @click="openPicker"
        >
          <v-icon left>mdi-package-variant-closed-plus</v-icon>
          Agregar productos
        </v-btn>
        <v-btn
          v-if="lastSaveError"
          small
          outlined
          :disabled="saving"
          @click="saveCatalog()"
        >
          Reintentar
        </v-btn>

        <v-btn class="mx-2" color="primary" @click="goPreview">
          <v-icon left>mdi-file-eye-outline</v-icon>
          Vista previa
        </v-btn>
        <v-btn class="mr-2" outlined @click="openShare">
          <v-icon left>mdi-share-variant</v-icon>
          Compartir
        </v-btn>
        <v-btn class="mr-2" outlined @click="exportPdf">
          <v-icon left>mdi-file-pdf-box</v-icon>
          Exportar PDF
        </v-btn>
        <v-btn
          class="mr-2"
          color="primary"
          :loading="saving"
          :disabled="!hasPendingChanges || saving"
          @click="saveCatalog"
        >
          <v-icon left>mdi-content-save</v-icon>
          Guardar
        </v-btn>
      </div>
      <div class="d-flex">
        <v-spacer />
        <v-chip
          v-if="toast.show"
          :color="toast.type"
          small
          outlined
          class="mr-2"
        >
          {{ toast.text }}
        </v-chip>
        <v-chip v-if="saveStateLabel" small outlined class="mr-2">
          {{ saveStateLabel }}
        </v-chip>
        <div v-for="j in pdfJobs" :key="j.jobId" class="mt-2">
          <div class="d-flex justify-space-between">
            <small>Generando PDF (estimado)</small>
            <small>{{ j.progress }}%</small>
          </div>
          <v-progress-linear :value="j.progress" height="8" />
        </div>
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
                    color="rgba(0, 0, 0, 0.50)"
                    text-color="white"
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
                      :disabled="p.id === 'cover'"
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
                      :disabled="idx === 0 || p.id === 'cover'"
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
                      :disabled="idx === pages.length - 1 || p.id === 'cover'"
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

                    <v-list-item
                      :disabled="p.id === 'cover'"
                      @click="duplicatePage(idx)"
                    >
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
          <div class="canvas-header">
            <div class="text-subtitle-2 font-weight-medium">Lienzo</div>

            <div class="text-caption text--secondary mr-3">
              {{ pageHeaderLabel }}
            </div>

            <div>
              <v-btn
                small
                outlined
                :disabled="!canAutoDistribute"
                @click="openDistributeDialog"
              >
                {{ autoDistributeLabel }}
              </v-btn>
              <div class="text-caption text--secondary mt-1">
                {{ showingLabel }}
              </div>
            </div>
          </div>
          <div v-if="needsReflow" class="text-caption text--secondary mt-1">
            El diseño cambió. Usa <strong>Reacomodar</strong> para ajustar las
            páginas.
          </div>
          <v-alert v-if="needsReflow" type="info" dense text class="mt-2">
            Cambiaste la plantilla u orientación. Reacomoda para aprovechar el
            espacio del nuevo diseño.
          </v-alert>

          <div v-if="!page" class="text-body-2 text--secondary">
            Página no disponible
          </div>

          <v-sheet
            v-else-if="!isCoverPage && pageItems.length === 0"
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

          <CatalogPageRender
            v-else
            :page="page"
            :orientation="catalog && catalog.orientation"
            :settings="catalog && catalog.settings"
            :theme="catalog && catalog.theme"
          />
        </v-sheet>
      </v-col>

      <!-- Propiedades -->
      <v-col cols="12" md="3">
        <v-sheet outlined class="pa-3">
          <div class="text-subtitle-2 font-weight-medium mb-2">Propiedades</div>

          <!-- Catálogo -->
          <div class="text-subtitle-2 font-weight-medium mt-2 mb-2">
            Catálogo
          </div>

          <v-text-field
            :value="catalogName"
            label="Nombre"
            outlined
            dense
            hide-details
            class="mb-3"
            @input="onCatalogMetaChange({ name: $event })"
          />

          <div class="d-flex align-center mb-3">
            <div class="text-body-2 font-weight-medium">
              Plantilla: {{ catalogTemplate }}
            </div>
            <v-spacer />
            <v-btn small outlined @click="openTemplateDialog">Cambiar</v-btn>
          </div>

          <v-select
            :value="catalog && catalog.orientation"
            :items="orientationItems"
            label="Orientación"
            outlined
            dense
            hide-details
            class="mb-3"
            @change="onCatalogMetaChange({ orientation: $event })"
          />

          <div class="text-subtitle-2 font-weight-medium mt-4 mb-2">Tema</div>

          <v-text-field
            :value="catalogTheme.primary"
            label="Color primario (hex)"
            outlined
            dense
            hide-details
            class="mb-3"
            @input="onThemeChange({ primary: $event })"
          />

          <v-select
            :value="catalogTheme.cover_overlay"
            :items="coverOverlayItems"
            label="Overlay portada"
            outlined
            dense
            hide-details
            class="mb-3"
            @change="onThemeChange({ cover_overlay: $event })"
          />

          <v-select
            :value="catalogTheme.card_style"
            :items="cardStyleItems"
            label="Estilo de tarjeta"
            outlined
            dense
            hide-details
            class="mb-2"
            @change="onThemeChange({ card_style: $event })"
          />

          <div class="text-subtitle-2 font-weight-medium mt-4 mb-2">
            Contenido
          </div>

          <v-switch
            label="Mostrar imágenes"
            :input-value="catalogSettings.show_images"
            @change="onSettingsChange({ show_images: $event })"
          />

          <v-switch
            label="Mostrar marca"
            :input-value="catalogSettings.show_brand"
            @change="onSettingsChange({ show_brand: $event })"
          />

          <v-switch
            label="Mostrar SKU"
            :input-value="catalogSettings.show_sku"
            @change="onSettingsChange({ show_sku: $event })"
          />

          <v-switch
            label="Mostrar descripción"
            :input-value="catalogSettings.show_description"
            @change="onSettingsChange({ show_description: $event })"
          />

          <v-switch
            label="Mostrar precios"
            :input-value="catalogSettings.show_price"
            @change="onSettingsChange({ show_price: $event })"
          />

          <v-switch
            label="Mostrar min/max compra"
            :input-value="catalogSettings.show_min_max"
            @change="onSettingsChange({ show_min_max: $event })"
          />

          <!-- Página -->
          <div class="text-subtitle-2 font-weight-medium mt-6 mb-2">Página</div>

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

            <div class="text-caption text--secondary mt-2">
              Edita el contenido de la portada
            </div>
          </div>

          <div v-else>
            <v-select
              :value="layoutKey"
              :items="layoutItems"
              label="Layout de página"
              outlined
              dense
              hide-details
              class="mb-2"
              @change="onLayoutChange"
            />

            <div class="text-caption text--secondary">
              El layout afecta cuántos productos entran por página.
            </div>
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

    <v-dialog v-model="showShareDialog" max-width="640">
      <v-card>
        <v-card-title class="text-subtitle-1 font-weight-medium">
          Compartir catálogo
        </v-card-title>

        <v-card-text>
          <div class="text-body-2 text--secondary mb-4">
            Comparte este link con tus clientes. Verán el catálogo sin iniciar
            sesión.
          </div>

          <v-text-field
            :value="publicLink"
            label="Link público"
            outlined
            dense
            hide-details
            readonly
          />

          <div class="d-flex mt-4">
            <v-btn outlined @click="copyLink">
              <v-icon left>mdi-content-copy</v-icon>
              Copiar
            </v-btn>

            <v-spacer />

            <v-btn text @click="regenerateToken"> Regenerar token </v-btn>
          </div>

          <v-alert dense text type="info" class="mt-4">
            Si regeneras el token, el link anterior dejará de funcionar.
          </v-alert>
        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <v-btn color="primary" @click="showShareDialog = false">
            Listo
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showTemplateDialog" max-width="560">
      <v-card>
        <v-card-title class="text-subtitle-1 font-weight-medium">
          Aplicar plantilla
        </v-card-title>

        <v-card-text>
          <v-select
            v-model="templateKey"
            :items="templateItems"
            label="Plantilla"
            outlined
            dense
            hide-details
            class="mb-4"
          />

          <v-switch
            v-model="applyTemplateToPages"
            label="Aplicar layout a todas las páginas"
          />

          <v-alert dense text type="info" class="mt-4">
            La plantilla ajusta settings del catálogo y defaults de portada. Si
            aplicas a todas las páginas, también cambia el layout.
          </v-alert>
        </v-card-text>

        <v-card-actions>
          <v-btn text @click="showTemplateDialog = false">Cancelar</v-btn>
          <v-spacer />
          <v-btn color="primary" @click="applyTemplate"> Aplicar </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <ProductPickerDialog v-model="showPicker" @add="onAddProducts" />
  </v-container>
</template>

<script>
import { mapState } from 'vuex'
import ProductPickerDialog from '~/components/catalogos/ProductPickerDialog.vue'
import CatalogPageRender from '~/components/catalogos/CatalogPageRender.vue'

export default {
  name: 'CatalogosEditPage',

  components: {
    ProductPickerDialog,
    CatalogPageRender,
  },

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
      capacityItems: [4, 5, 6, 7, 8, 9, 10, 12, 15, 16],

      layoutItems: [
        { text: 'Grid 2 x 3 (6)', value: 'grid_2x3' },
        { text: 'Grid 2 x 4 (8)', value: 'grid_2x4' },
        { text: 'Grid 2 x 5 (10)', value: 'grid_2x5' },
        { text: 'Grid 2 x 6 (12)', value: 'grid_2x6' },
        { text: 'Grid 3 x 3 (9)', value: 'grid_3x3' },
        { text: 'Grid 3 x 4 (12)', value: 'grid_3x4' },
        { text: 'Grid 3 x 5 (15)', value: 'grid_3x5' },

        { text: 'Lista compacta (6)', value: 'list_compact' },
      ],

      showShareDialog: false,
      shareToken: '',

      // Configuración de template del catálogo
      templateKey: 'minimal',
      applyTemplateToPages: true,
      showTemplateDialog: false,
      templateItems: [
        { text: 'Minimal', value: 'minimal' },
        { text: 'Fashion', value: 'fashion' },
        { text: 'Promo', value: 'promo' },
      ],

      coverOverlayItems: [
        { text: 'Claro', value: 'light' },
        { text: 'Oscuro', value: 'dark' },
        { text: 'Ninguno', value: '' },
      ],

      cardStyleItems: [
        { text: 'Outlined', value: 'outlined' },
        { text: 'Flat', value: 'flat' },
      ],

      saving: false,
      lastSavedHash: '',

      autosaveTimer: null,
      autosaveDelayMs: 1800,
      autosaveEnabled: true,
      lastSaveError: '',
    }
  },

  computed: {
    ...mapState('catalogo/catalogos', ['toast']),

    catalogId() {
      return Number(this.$route.params.id)
    },

    catalog() {
      return this.$store.getters['catalogo/catalogos/byId'](this.catalogId)
    },

    catalogName() {
      return (this.catalog && this.catalog.name) || 'Catálogo'
    },

    catalogTemplate() {
      const t = (this.catalog && this.catalog.template) || 'minimal'
      const map = { minimal: 'Minimal', fashion: 'Fashion', promo: 'Promo' }
      return map[t] || t
    },

    catalogOrientation() {
      // const o = this.catalog && this.catalog.orientation
      // return o === 'portrait' ? 'Vertical' : 'Horizontal'
      return this.catalog?.orientation === 'portrait'
        ? 'Vertical'
        : 'Horizontal'
    },

    pageHeaderLabel() {
      const n = this.activePageIndex + 1
      const total = this.pages.length

      const name = this.page && this.page.name ? this.page.name : `Página ${n}`

      return `${name} (${n}/${total})`
    },

    pages() {
      return (this.catalog && this.catalog.pages) || []
    },

    activePageIndex() {
      return this.$store.getters['catalogo/catalogos/activePageIndex'](
        this.catalogId
      )
    },
    activePage() {
      return this.pages[this.activePageIndex] || null
    },

    page() {
      return this.pages[this.activePageIndex] || null
    },

    layoutKey() {
      return (this.page && this.page.layout) || 'grid_2x4'
    },

    layoutCapacity() {
      const map = {
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

    pageItems() {
      const items =
        this.page && Array.isArray(this.page.items) ? this.page.items : []
      return items
    },

    showingLabel() {
      const total = this.pageItems.length
      const shown = Math.min(total, this.layoutCapacity)
      return `Mostrando ${shown} de ${total}`
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

    publicLink() {
      if (!this.shareToken) return ''
      const origin = process.client ? window.location.origin : ''
      return `${origin}/portal/shared-catalog/${this.shareToken}`
      // return `${origin}/catalogos/${this.shareToken}`
    },
    catalogSettings() {
      return (
        (this.catalog && this.catalog.settings) || {
          show_price: true,
          show_brand: true,
          show_min_max: true,
          show_sku: true,
          show_description: true,
          show_images: true,
        }
      )
    },

    catalogTheme() {
      return (
        (this.catalog && this.catalog.theme) || {
          primary: '#1976d2',
          cover_overlay: 'light',
          card_style: 'outlined',
        }
      )
    },

    catalogSnapshot() {
      if (!this.catalog) return null

      return {
        name: this.catalog.name,
        template: this.catalog.template,
        orientation: this.catalog.orientation,
        settings: this.catalog.settings,
        theme: this.catalog.theme,
        pages: this.catalog.pages,
      }
    },

    snapshotHash() {
      try {
        return JSON.stringify(this.catalogSnapshot || {})
      } catch (e) {
        return ''
      }
    },

    hasPendingChanges() {
      if (!this.catalog) return false
      if (!this.lastSavedHash) return true
      return this.snapshotHash !== this.lastSavedHash
    },

    saveStateLabel() {
      if (!this.catalog) return ''
      if (this.lastSaveError) return 'Error'
      if (this.saving) return 'Guardando...'
      if (!this.lastSavedHash) return 'No guardado'
      if (this.hasPendingChanges) return 'Cambios pendientes'
      return 'Guardado'
    },

    pdfJobs() {
      return this.$store.getters['catalogo/catalogos/pdfJobsActiveByCatalog'](
        this.catalogId
      )
    },

    needsReflow() {
      return this.$store.getters['catalogo/catalogos/needsReflow'](
        this.catalogId
      )
    },

    canAutoDistribute() {
      if (this.isCoverPage) return false
      if (!this.page) return false

      return this.needsReflow || this.pageItems.length > this.layoutCapacity
    },

    autoDistributeLabel() {
      if (this.needsReflow && this.pageItems.length <= this.layoutCapacity) {
        return 'Reacomodar'
      }
      return 'Auto-distribuir'
    },

    orientationItems() {
      return [
        { text: 'Vertical (Carta)', value: 'portrait' },
        { text: 'Horizontal (Carta)', value: 'landscape' },
      ]
    },
  },

  watch: {
    catalog: {
      immediate: true,
      handler(val) {
        if (!val) return
        if (!this.lastSavedHash) this.lastSavedHash = this.snapshotHash
      },
    },

    snapshotHash(val, oldVal) {
      if (!this.autosaveEnabled) return
      if (!this.catalog) return
      if (!this.lastSavedHash) return

      if (val === oldVal) return
      if (val === this.lastSavedHash) return

      this.queueAutosave()
    },
  },

  mounted() {
    // this.$store.dispatch('catalogo/catalogos/init')
    this.$store.dispatch('catalogo/catalogos/setCurrent', this.catalogId)

    this.$store.dispatch('catalogo/catalogos/ensureCoverPage', {
      catalogId: this.catalogId,
    })

    // opcional: mostrar portada al abrir
    this.$store.dispatch('catalogo/catalogos/setActivePage', {
      catalogId: this.catalogId,
      pageIndex: 0,
    })

    window.addEventListener('beforeunload', this.onBeforeUnload)
  },

  beforeRouteLeave(to, from, next) {
    if (this.shouldBlockNavigation()) {
      const ok = window.confirm(
        'Tienes cambios pendientes. ¿Salir sin guardar?'
      )
      if (!ok) return next(false)
    }

    next()
  },

  beforeDestroy() {
    if (this.autosaveTimer) clearTimeout(this.autosaveTimer)

    window.removeEventListener('beforeunload', this.onBeforeUnload)
  },

  methods: {
    goPreview() {
      this.$router.push(`/catalogos/${this.catalogId}/preview`)
    },

    openPicker() {
      // this.showPicker = true
      if (this.isCoverPage) return
      this.openPickerForIndex(this.activePageIndex)
    },

    async onAddProducts(products) {
      const catalogId = this.catalogId

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

    setActivePage(pageIndex) {
      const catalogId = this.catalogId

      this.$store.dispatch('catalogo/catalogos/setActivePage', {
        catalogId,
        pageIndex,
      })
    },

    onLayoutChange(layout) {
      const catalogId = this.catalogId
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
        grid_2x3: 6,
        grid_2x4: 8,
        grid_2x5: 10,
        grid_2x6: 12,
        grid_3x3: 9,
        grid_3x4: 12,
        grid_3x5: 15,
        list_compact: 6,
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
      const catalogId = this.catalogId

      await this.$store.dispatch('catalogo/catalogos/autoDistribute', {
        catalogId,
        layout: this.distributeLayout,
        capacity: this.distributeCapacity,
      })

      this.setActivePage(0)
      this.showDistributeDialog = false
    },

    openNewPageDialog() {
      const map = {
        Minimal: 'grid_2x4',
        Fashion: 'grid_3x3',
        Promo: 'list_compact',
      }

      const t = (this.catalog && this.catalog.template) || 'Minimal'
      this.newPageLayout = map[t] || this.layoutKey

      this.newPageAddProducts = true
      this.showNewPageDialog = true
    },

    async createNewPage() {
      const catalogId = this.catalogId

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
      const catalogId = this.catalogId

      await this.$store.dispatch('catalogo/catalogos/duplicatePage', {
        catalogId,
        pageIndex: idx,
      })
    },

    async deletePage(idx) {
      const ok = window.confirm('¿Eliminar esta página?')
      if (!ok) return

      const catalogId = this.catalogId

      await this.$store.dispatch('catalogo/catalogos/deletePage', {
        catalogId,
        pageIndex: idx,
      })
    },

    async movePageUp(idx) {
      if (idx <= 0) return
      const catalogId = this.catalogId

      await this.$store.dispatch('catalogo/catalogos/movePage', {
        catalogId,
        fromIndex: idx,
        toIndex: idx - 1,
      })
    },

    async movePageDown(idx) {
      if (idx >= this.pages.length - 1) return
      const catalogId = this.catalogId

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

      const catalogId = this.catalogId

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
      const catalogId = this.catalogId

      await this.$store.dispatch('catalogo/catalogos/ensureCoverPage', {
        catalogId,
      })

      this.setActivePage(0)
    },

    onCoverChange(patch) {
      const catalogId = this.catalogId

      this.$store.dispatch('catalogo/catalogos/updateCover', {
        catalogId,
        patch,
      })
    },

    async openShare() {
      const catalogId = this.catalogId

      const token = await this.$store.dispatch(
        'catalogo/catalogos/ensureShareToken',
        { catalogId }
      )

      this.shareToken = token
      this.showShareDialog = true
    },

    async regenerateToken() {
      const catalogId = this.catalogId

      const token = await this.$store.dispatch(
        'catalogo/catalogos/regenerateShareToken',
        { catalogId }
      )

      this.shareToken = token
    },

    async copyLink() {
      if (!this.publicLink) return

      try {
        await navigator.clipboard.writeText(this.publicLink)
        this.$toast?.success?.('Link copiado')
      } catch (e) {
        this.$toast?.info?.('Copia manualmente el link')
      }
    },

    onSettingsChange(patch) {
      const catalogId = this.catalogId

      this.$store.dispatch('catalogo/catalogos/updateSettings', {
        catalogId,
        patch,
      })
    },

    openTemplateDialog() {
      const t = (this.catalog && this.catalog.template) || 'Minimal'

      const map = {
        Minimal: 'minimal',
        Fashion: 'fashion',
        Promo: 'promo',
      }

      this.templateKey = map[t] || 'minimal'
      this.applyTemplateToPages = true
      this.showTemplateDialog = true
    },

    onCatalogMetaChange(patch) {
      const catalogId = this.catalogId

      this.$store.dispatch('catalogo/catalogos/updateCatalogMeta', {
        catalogId,
        patch,
      })
    },

    applyTemplate() {
      const catalogId = this.catalogId

      // 1) asegura que el catálogo refleje el template elegido y marque reflow
      //    Actualiza metadata del catálogo.
      this.onCatalogMetaChange({
        template: this.templateKey,
      })

      // 2) aplica defaults (settings/cover) y opcionalmente layout a páginas
      this.$store.dispatch('catalogo/catalogos/applyTemplate', {
        catalogId,
        key: this.templateKey,
        applyToPages: this.applyTemplateToPages,
      })

      this.showTemplateDialog = false
    },

    onThemeChange(patch) {
      const catalogId = this.catalogId

      const next = { ...patch }

      if (Object.prototype.hasOwnProperty.call(next, 'primary')) {
        const v = String(next.primary || '').trim()
        const ok = /^#([0-9a-fA-F]{6})$/.test(v)
        if (!ok) return
        next.primary = v
      }

      this.$store.dispatch('catalogo/catalogos/updateTheme', {
        catalogId,
        patch: next,
      })
    },

    // async exportPdf() {
    //   const catalogId = this.catalogId
    //   const res = await this.$axios.request({
    //     url: `/catalog/api/catalogs/${catalogId}/export-pdf/`,
    //     method: 'POST',
    //     responseType: 'blob',
    //   })

    //   const blob = new Blob([res.data], { type: 'application/pdf' })
    //   const url = window.URL.createObjectURL(blob)

    //   const a = document.createElement('a')
    //   a.href = url
    //   a.download = `catalogo-${catalogId}.pdf`
    //   a.click()

    //   window.URL.revokeObjectURL(url)
    // },

    queueAutosave() {
      if (this.autosaveTimer) clearTimeout(this.autosaveTimer)

      this.autosaveTimer = setTimeout(() => {
        this.saveCatalog({ silent: true })
      }, this.autosaveDelayMs)
    },

    async saveCatalog({ silent } = { silent: false }) {
      if (!this.catalog) return

      this.saving = true
      this.lastSaveError = ''

      try {
        const id = this.catalogId

        await this.$axios.$patch(`/catalog/api/catalogs/${id}/`, {
          name: this.catalog.name,
          template: this.catalog.template,
          orientation: this.catalog.orientation,
          settings: this.catalog.settings,
          theme: this.catalog.theme,
          pages: this.catalog.pages,
        })

        this.lastSavedHash = this.snapshotHash
        if (!silent) this.$toast?.success?.('Guardado')
      } catch (e) {
        this.lastSaveError = 'No se pudo guardar'
        if (!silent) this.$toast?.error?.('No se pudo guardar')
      } finally {
        this.saving = false
      }
    },

    shouldBlockNavigation() {
      if (!this.catalog) return false
      if (this.saving) return false

      // Si hay autosave activo, normalmente los cambios se guardan solos,
      // pero si hay error o aún hay cambios pendientes, bloqueamos.
      if (this.lastSaveError) return true
      return this.hasPendingChanges
    },

    onBeforeUnload(e) {
      if (!this.shouldBlockNavigation()) return

      e.preventDefault()
      e.returnValue = ''
    },

    async exportPdf() {
      // totalPages lo puedes tomar de tu estado actual del catálogo:
      const totalPages = (this.catalog?.pages || []).length
      await this.$store.dispatch('catalogo/catalogos/exportPdfStart', {
        catalogId: this.catalogId,
        totalPages,
      })
    },

    // applyTemplateDefaults() {
    //   const catalogId = this.catalogId

    //   this.$store.dispatch('catalogo/catalogos/applyTemplateDefaults', {
    //     catalogId,
    //     template: this.templateKey,
    //   })
    // },
  },
}
</script>

<style scoped>
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
  /* background: white; */
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

.canvas-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}
</style>
