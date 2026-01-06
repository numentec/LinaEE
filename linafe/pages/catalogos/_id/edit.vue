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
          Agregar productos
        </v-btn>
        <v-btn color="primary" @click="goPreview"> Vista previa </v-btn>
      </div>
    </v-card>

    <v-row>
      <!-- Panel páginas -->
      <v-col cols="12" md="3">
        <v-sheet outlined class="pa-3">
          <div class="d-flex align-center mb-2">
            <div class="text-subtitle-2 font-weight-medium">Páginas</div>
            <v-spacer />
            <v-btn small text disabled>
              <v-icon left small>mdi-plus</v-icon> Página
            </v-btn>
          </div>

          <v-list dense>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>Página 1</v-list-item-title>
                <v-list-item-subtitle>Layout: grid_2x4</v-list-item-subtitle>
              </v-list-item-content>
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
          <div class="text-subtitle-2 font-weight-medium mb-3">
            Lienzo (MVP)
          </div>
          <v-sheet class="pa-8" outlined :style="paperStyle">
            <div class="text-h6 mb-2">{{ catalogName }}</div>
            <div class="text-caption text--secondary">
              Aquí renderizaremos la página actual y los productos.
            </div>
          </v-sheet>
        </v-sheet>
      </v-col>

      <!-- Propiedades -->
      <v-col cols="12" md="3">
        <v-sheet outlined class="pa-3">
          <div class="text-subtitle-2 font-weight-medium mb-2">Propiedades</div>
          <v-switch label="Mostrar precios" :value="true" disabled />
          <v-switch label="Mostrar marca" :value="true" disabled />
          <v-switch label="Mostrar min/max compra" :value="true" disabled />
          <div class="text-caption text--secondary">
            (MVP) Luego conectamos esto a settings del catálogo.
          </div>
        </v-sheet>
      </v-col>
    </v-row>
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
      this.showPicker = true
    },

    async onAddProducts(products) {
      const catalogId = this.$route.params.id
      const pageId = 'page_1'

      await this.$store.dispatch('catalogo/catalogos/addProductsToPage', {
        catalogId,
        pageId,
        products,
      })
    },
  },
}
</script>
