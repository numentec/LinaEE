<template>
  <v-container>
    <v-card v-if="!isPdf" outlined class="pa-3 mb-3">
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
      <div v-for="p in pages" :key="p.id" :class="isPdf ? 'pdf-page' : 'mb-8'">
        <CatalogPageRender
          :page="p"
          :orientation="catalog.orientation"
          :settings="catalog.settings"
          :theme="catalog.theme"
          :is-print="isPdf"
        />
      </div>
    </div>
  </v-container>
</template>

<script>
import CatalogPageRender from '~/components/catalogos/CatalogPageRender.vue'

export default {
  name: 'PublicCatalogPage',
  layout: 'clean',
  components: { CatalogPageRender },

  async asyncData({ app, params, error }) {
    try {
      const catalog = await app.$api.getPublicCatalog(params.token)
      return { catalog }
    } catch (e) {
      error({ statusCode: 404, message: 'Catálogo no encontrado' })
    }
  },

  data() {
    return { catalog: null }
  },

  computed: {
    token() {
      return this.$route.params.token
    },

    // catalog() {
    //   return this.$store.getters['catalogo/catalogos/byToken'](this.token)
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
    },

    isPdf() {
      return this.$route.query.pdf === '1'
    },
  },

  watch: {
    catalog: {
      immediate: true,
      async handler(val) {
        if (!process.client) return
        if (!val) return

        const isPdf = this.$route.query.pdf === '1'
        if (!isPdf) return

        // Espera a que el DOM pinte
        await this.$nextTick()

        // Espera a que se hayan renderizado items (evita imprimir antes de tiempo)
        const start = Date.now()
        while (Date.now() - start < 15000) {
          const items = document.querySelectorAll('.catalog-item')
          if (items && items.length > 0) break
          await new Promise((resolve) => setTimeout(resolve, 100))
        }

        // Espera a que carguen imágenes (best effort)
        const imgs = Array.from(document.images || [])
        await Promise.all(
          imgs.map((img) => {
            if (img.complete) return Promise.resolve()
            return new Promise((resolve) => {
              img.addEventListener('load', resolve, { once: true })
              img.addEventListener('error', resolve, { once: true })
            })
          })
        )

        window.__PDF_READY__ = true
      },
    },
  },

  mounted() {
    // this.$store.dispatch('catalogo/catalogos/init')
    window.__PDF_READY__ = false
  },

  head() {
    return {
      title: 'Shared Catalog',
      meta: [
        {
          hid: 'description',
          name: 'description',
          content: 'Access and view the shared catalog.',
        },
      ],
    }
  },
}
</script>

<style scoped>
@media print {
  .pdf-page {
    page-break-after: always;
    break-after: page;
  }
  .pdf-page:last-child {
    page-break-after: auto;
    break-after: auto;
  }
}

.pdf-page {
  margin-bottom: 0;
}
</style>
