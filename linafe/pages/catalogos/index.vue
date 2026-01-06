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

    <CatalogGrid
      :items="filtered"
      @new="goNew"
      @open="openEdit"
      @duplicate="duplicate"
      @share="share"
      @exportPdf="exportPdf"
      @archive="archive"
    />
  </div>
</template>

<script>
import CatalogToolbar from '~/components/catalogos/CatalogToolbar.vue'
import CatalogFilters from '~/components/catalogos/CatalogFilters.vue'
import CatalogGrid from '~/components/catalogos/CatalogGrid.vue'

export default {
  name: 'CatalogosIndexPage',
  components: { CatalogToolbar, CatalogFilters, CatalogGrid },

  data() {
    return {
      search: '',
      status: 'all',
      template: 'all',
      sort: 'updated_desc',
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
  },

  //   activated() {
  //     console.log('CatalogosIndexPage activated')
  //   },

  mounted() {
    this.$store.dispatch('catalogo/catalogos/init')
  },

  methods: {
    goNew() {
      this.$router.push('/catalogos/new')
    },
    openEdit(id) {
      this.$store.dispatch('catalogo/catalogos/setCurrent', id)
      this.$router.push(`/catalogos/${id}/edit`)
    },
    duplicate(id) {
      // MVP: duplicación rápida en frontend (más adelante: backend)
      const src = this.$store.getters['catalogo/catalogos/byId'](id)
      if (!src) return
      this.$store
        .dispatch('catalogo/catalogos/createCatalog', {
          name: `${src.name} (copia)`,
          template: src.template,
          orientation: src.orientation,
          company_id: src.company_id,
        })
        .then((newCat) => this.$router.push(`/catalogos/${newCat.id}/edit`))
    },
    share(id) {
      // MVP: placeholder (luego /share)
      this.$router.push(`/catalogos/${id}/preview`)
    },
    exportPdf(id) {
      // MVP: placeholder
      this.$toast?.info?.('Exportar PDF: pendiente (MVP botón listo)')
      console.log('Export PDF', id)
    },
    archive(id) {
      this.$store.commit('catalogo/catalogos/UPDATE_ITEM', {
        id,
        patch: { status: 'archived', updated_at: new Date().toISOString() },
      })
    },
  },
}
</script>
