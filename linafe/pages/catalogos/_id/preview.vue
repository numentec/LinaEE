<template>
  <v-container>
    <v-card outlined class="pa-3 mb-3">
      <div class="d-flex align-center">
        <v-btn icon @click="goBack">
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>

        <div class="ml-2">
          <div class="text-subtitle-1 font-weight-medium">Vista previa</div>
          <div class="text-caption text--secondary">
            {{ catalogName }}
          </div>
        </div>

        <v-spacer />

        <v-chip small outlined> {{ pages.length }} páginas </v-chip>
      </div>
    </v-card>

    <div v-if="!catalog" class="text-body-2 text--secondary">
      Catálogo no encontrado
    </div>

    <div v-else>
      <div v-for="(p, idx) in pages" :key="p.id" class="mb-8">
        <div class="d-flex align-center mb-2">
          <div class="text-caption text--secondary">
            {{ pageLabel(p, idx) }}
          </div>
        </div>

        <CatalogPageRender
          :page="p"
          :orientation="catalog.orientation"
          :settings="catalog.settings"
          :theme="catalog.theme"
        />
      </div>
    </div>
  </v-container>
</template>

<script>
import CatalogPageRender from '~/components/catalogos/CatalogPageRender.vue'

export default {
  name: 'CatalogosPreviewPage',
  components: { CatalogPageRender },

  async asyncData({ app, params, error }) {
    try {
      const catalog = await app.$api.getCatalog(params.id)
      return { catalog }
    } catch (e) {
      error({ statusCode: 404, message: 'Catálogo no encontrado' })
    }
  },

  data() {
    return { catalog: null }
  },

  computed: {
    // catalog() {
    //   return this.$store.getters['catalogo/catalogos/byId'](
    //     this.$route.params.id
    //   )
    // },

    catalogName() {
      return (this.catalog && this.catalog.name) || 'Catálogo'
    },

    pages() {
      const pages =
        this.catalog && Array.isArray(this.catalog.pages)
          ? this.catalog.pages
          : []

      return pages
      // return (this.catalog && this.catalog.pages) || []
    },
  },

  mounted() {
    this.$store.dispatch('catalogo/catalogos/init')
  },

  methods: {
    goBack() {
      this.$router.push(`/catalogos/${this.$route.params.id}/edit`)
    },

    pageLabel(p, idx) {
      if (p && p.layout === 'cover') return 'Portada'
      const n = idx + 1
      const name = p && p.name ? p.name : `Página ${n}`
      return `${name}`
    },
  },
}
</script>
