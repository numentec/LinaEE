<template>
  <v-container>
    <v-card outlined class="pa-3 mb-3">
      <div class="d-flex align-center">
        <div>
          <div class="text-subtitle-1 font-weight-medium">
            {{ catalogName }}
          </div>
          <div class="text-caption text--secondary">Catálogo público</div>
        </div>

        <v-spacer />

        <v-chip v-if="catalog" small outlined>
          {{ pages.length }} páginas
        </v-chip>
      </div>
    </v-card>

    <v-sheet v-if="!catalog" class="pa-10 text-center" outlined>
      <div class="text-h6 mb-2">Link inválido o expirado</div>
      <div class="text-body-2 text--secondary">
        Solicita al vendedor que te reenvíe el catálogo.
      </div>
    </v-sheet>

    <div v-else>
      <div v-for="(p, idx) in pages" :key="idx" class="mb-8">
        <CatalogPageRender :page="p" :orientation="catalog.orientation" />
      </div>
    </div>
  </v-container>
</template>

<script>
import CatalogPageRender from '~/components/catalogos/CatalogPageRender.vue'

export default {
  name: 'PublicCatalogPage',
  components: { CatalogPageRender },

  computed: {
    token() {
      return this.$route.params.token
    },

    catalog() {
      return this.$store.getters['catalogo/catalogos/byToken'](this.token)
    },

    catalogName() {
      return (this.catalog && this.catalog.name) || 'Catálogo'
    },

    pages() {
      const pages =
        this.catalog && Array.isArray(this.catalog.pages)
          ? this.catalog.pages
          : []

      return pages
    },
  },

  mounted() {
    this.$store.dispatch('catalogo/catalogos/init')
  },
}
</script>
