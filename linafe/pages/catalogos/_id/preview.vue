<template>
  <v-container>
    <v-card outlined class="pa-3 mb-3">
      <div class="d-flex align-center">
        <v-btn
          icon
          @click="$router.push(`/catalogos/${$route.params.id}/edit`)"
        >
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
        <div class="ml-2">
          <div class="text-subtitle-1 font-weight-medium">Vista previa</div>
          <div class="text-caption text--secondary">
            {{ catalogName }}
          </div>
        </div>
      </div>
    </v-card>

    <v-sheet class="pa-8" outlined :style="paperStyle">
      <div class="text-h5 mb-2">{{ catalogName }}</div>
      <div class="text-body-2 text--secondary">
        (MVP) Esto será la vista web compartible y también base para PDF.
      </div>
    </v-sheet>
  </v-container>
</template>

<script>
export default {
  name: 'CatalogosPreviewPage',
  computed: {
    catalog() {
      return this.$store.getters['catalogo/catalogos/byId'](
        this.$route.params.id
      )
    },
    catalogName() {
      return (this.catalog && this.catalog.name) || 'Catalog Name'
    },
    paperStyle() {
      const width = 700
      const portraitRatio = 11 / 8.5
      const landscapeRatio = 8.5 / 11
      const ratio =
        this.catalog?.orientation === 'landscape'
          ? landscapeRatio
          : portraitRatio
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
  },
}
</script>
