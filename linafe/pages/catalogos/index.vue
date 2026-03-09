<template>
  <div>
    <CatalogToolbar
      :search="search"
      @update:search="search = $event"
      @new="goNew"
    />

    <CatalogFilters
      :status="status"
      :template="template"
      :sort="sort"
      @update:status="status = $event"
      @update:template="template = $event"
      @update:sort="sort = $event"
    />

    <v-alert
      v-if="duplicateError"
      border="top"
      colored-border
      type="error"
      elevation="2"
      dismissible
    >
      {{ duplicateError }}
    </v-alert>

    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      rounded="pill"
      timeout="5000"
      absolute
      top
      left
    >
      {{ snackbar.message }}
      <template v-slot:action="{ attrs }">
        <v-btn icon dark v-bind="attrs" @click="snackbar.show = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </template>
    </v-snackbar>

    <CatalogGrid
      :items="filtered"
      @new="goNew"
      @open="openEdit"
      @duplicate="duplicate"
      @share="share"
      @exportPdf="exportPdf"
      @archive="archive"
    />

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
            :value="sharePublicLink"
            label="Link público"
            outlined
            dense
            hide-details
            readonly
          />

          <div class="d-flex mt-4">
            <v-btn outlined @click="copyShareLink">
              <v-icon left>mdi-content-copy</v-icon>
              Copiar
            </v-btn>

            <v-spacer />

            <v-btn text :loading="shareLoading" @click="regenerateShare">
              Regenerar token
            </v-btn>
          </div>

          <v-alert dense text type="info" class="mt-4">
            Si regeneras el token, el link anterior dejará de funcionar.
          </v-alert>
        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <v-btn color="primary" @click="closeShareDialog"> Listo </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import CatalogToolbar from '~/components/catalogos/CatalogToolbar.vue'
import CatalogFilters from '~/components/catalogos/CatalogFilters.vue'
import CatalogGrid from '~/components/catalogos/CatalogGrid.vue'

export default {
  name: 'CatalogosIndexPage',
  components: { CatalogToolbar, CatalogFilters, CatalogGrid },

  async asyncData({ app, error, store }) {
    try {
      await store.dispatch('catalogo/catalogos/fetchCatalogs')
      return {}
    } catch (e) {
      error({ statusCode: 500, message: 'Error al cargar los catálogos' })
    }
  },

  data() {
    return {
      search: '',
      status: 'all',
      template: 'all',
      sort: 'updated_desc',
      isDuplicating: false,
      duplicateError: '',
      showShareDialog: false,
      shareCatalogId: null,
      shareToken: '',
      shareLoading: false,
      snackbar: {
        show: false,
        message: '',
        color: 'success',
      },
    }
  },

  computed: {
    items() {
      return this.$store.getters['catalogo/catalogos/all']
    },

    filtered() {
      let out = [...this.items]

      // status
      if (this.status !== 'all') {
        out = out.filter((c) => c.status === this.status)
      }

      // template
      if (this.template !== 'all') {
        out = out.filter((c) => c.template === this.template)
      }

      // search
      const q = (this.search || '').trim().toLowerCase()
      if (q) {
        out = out.filter((c) => (c.name || '').toLowerCase().includes(q))
      }

      // sort
      if (this.sort === 'updated_desc') {
        out.sort((a, b) =>
          (b.updated_at || '').localeCompare(a.updated_at || '')
        )
      } else if (this.sort === 'name_asc') {
        out.sort((a, b) => (a.name || '').localeCompare(b.name || ''))
      } else if (this.sort === 'status_asc') {
        out.sort((a, b) => (a.status || '').localeCompare(b.status || ''))
      }

      return out
    },

    sharePublicLink() {
      if (!this.shareToken) return ''
      const origin = process.client ? window.location.origin : ''
      return `${origin}/portal/shared-catalog/${this.shareToken}`
    },
  },

  methods: {
    getErrorMessage(e, fallback = 'No se pudo duplicar el catálogo') {
      return (
        e?.response?.data?.message ||
        e?.response?.data?.error ||
        e?.message ||
        fallback
      )
    },

    goNew() {
      this.$router.push('/catalogos/new')
    },

    openEdit(id) {
      this.$store.dispatch('catalogo/catalogos/setCurrent', id)
      this.$router.push(`/catalogos/${id}/edit`)
    },

    async duplicate(id) {
      if (this.isDuplicating) return null

      this.isDuplicating = true
      this.duplicateError = ''

      try {
        const newCat = await this.$store.dispatch(
          'catalogo/catalogos/duplicateCatalog',
          { id }
        )

        if (!newCat?.id) throw new Error('Respuesta inválida al duplicar')

        this.$toast?.success?.('Catálogo duplicado')
        await this.$router.push(`/catalogos/${newCat.id}/edit`)
        return newCat
      } catch (e) {
        const message = this.getErrorMessage(e)
        this.duplicateError = message
        this.$toast?.error?.(message)
        return null
      } finally {
        this.isDuplicating = false
      }
    },

    async share(id) {
      this.shareCatalogId = id
      this.shareLoading = true

      try {
        const token = await this.$store.dispatch(
          'catalogo/catalogos/ensureShareToken',
          { id }
        )

        this.shareToken = token
        this.showShareDialog = true
      } catch (e) {
        this.$toast?.error?.('No se pudo obtener el link público')
      } finally {
        this.shareLoading = false
      }
    },

    async regenerateShare() {
      if (!this.shareCatalogId) return

      this.shareLoading = true

      try {
        const token = await this.$store.dispatch(
          'catalogo/catalogos/regenerateShareToken',
          { id: this.shareCatalogId }
        )

        this.shareToken = token
        this.$toast?.success?.('Link regenerado')
      } catch (e) {
        this.$toast?.error?.('No se pudo regenerar el link')
      } finally {
        this.shareLoading = false
      }
    },

    async copyShareLink() {
      if (!this.sharePublicLink) return

      try {
        await navigator.clipboard.writeText(this.sharePublicLink)
        this.$toast?.success?.('Link copiado')
      } catch (e) {
        this.$toast?.error?.('No se pudo copiar el link')
      }
    },

    closeShareDialog() {
      this.showShareDialog = false
      this.shareCatalogId = null
      this.shareToken = ''
    },

    exportPdf(id) {
      this.$toast?.info?.('Exportar PDF: pendiente (MVP botón listo)')
    },

    async archive(id) {
      if (this.items.find((c) => c.id === id)?.status === 'archived') {
        this.snackbar = {
          show: true,
          message: 'Este catálogo ya está archivado',
          color: 'info',
        }
        return
      }

      const ok = window.confirm('¿Archivar este catálogo?')
      if (!ok) return

      try {
        await this.$store.dispatch('catalogo/catalogos/archiveCatalog', {
          id,
        })

        this.snackbar = {
          show: true,
          message: 'Catálogo archivado con éxito',
          color: 'success',
        }

        // this.$toast?.success?.('Catálogo archivado')
      } catch (e) {
        this.snackbar = {
          show: true,
          message: 'No se pudo archivar el catálogo',
          color: 'error',
        }
        // this.$toast?.error?.('No se pudo archivar el catálogo')
      }
    },
  },
}
</script>
