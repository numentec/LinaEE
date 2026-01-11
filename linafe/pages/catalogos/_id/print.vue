<template>
  <div class="print-root">
    <div v-if="!catalog" class="print-empty">Catálogo no encontrado</div>

    <div v-else>
      <div v-for="p in pages" :key="p.id" class="print-page">
        <CatalogPageRender
          :page="p"
          :orientation="catalog.orientation"
          :settings="catalog.settings"
          :theme="catalog.theme"
          :is-print="true"
        />
      </div>
    </div>
  </div>
</template>

<script>
import CatalogPageRender from '~/components/catalogos/CatalogPageRender.vue'

export default {
  name: 'CatalogosPrintPage',
  layout: 'publicapps',
  components: { CatalogPageRender },

  computed: {
    catalog() {
      return this.$store.getters['catalogo/catalogos/byId'](
        this.$route.params.id
      )
    },

    pages() {
      const pages =
        this.catalog && Array.isArray(this.catalog.pages)
          ? this.catalog.pages
          : []

      return pages
    },
  },

  async mounted() {
    await this.$store.dispatch('catalogo/catalogos/init')

    this.$nextTick(() => {
      // pequeño delay para que carguen imágenes
      setTimeout(() => {
        window.print()
      }, 1200)
    })
  },
}
</script>

<style scoped>
.print-root {
  padding: 16px;
}

.print-empty {
  padding: 32px;
  text-align: center;
}
</style>

<style>
/* Estilos de impresión globales para esta página */
@media print {
  /* quita márgenes de la app */
  html,
  body {
    margin: 0 !important;
    padding: 0 !important;
    background: white !important;
  }

  /* evita que Vuetify meta fondos raros */
  .application,
  .v-application {
    background: white !important;
  }

  /* cada página del catálogo en una hoja */
  .print-page {
    page-break-after: always;
    break-after: page;
  }

  .print-page:last-child {
    page-break-after: auto;
    break-after: auto;
  }

  /* no imprimir sombras */
  .v-sheet,
  .v-card {
    box-shadow: none !important;
  }
}

/*
  Importante: @page con tamaño "letter".
  Nota: la orientación real la decide el diálogo de impresión (usuario),
  pero esto ayuda a guiar el tamaño.
*/
@page {
  size: letter;
  margin: 10mm;
}
</style>
