<template>
  <CatalogPrintDocument :doc="doc" :pdf-mode="pdfMode" />
</template>

<script>
import CatalogPrintDocument from '@/components/catalogos/CatalogPrintDocument.vue'

export default {
  layout: 'print',
  components: { CatalogPrintDocument },

  async asyncData({ app, params, query }) {
    // const { token } = params

    // Si tienes proxy en nuxt.config.js, esto puede ser relativo.
    // Si no, usa URL absoluta:
    // const url = `/catalog/api/public/catalogos/${token}/`

    const doc = await app.$api.getPublicCatalog(params.token)
    const pdfMode = query && (query.pdf === '1' || query.pdf === 'true')

    return { doc, pdfMode }
  },

  data() {
    return { doc: null, pdfMode: false }
  },

  mounted() {
    const done = () => {
      window.__PDF_READY__ = true
    }

    this.$nextTick(() => {
      const imgs = Array.from(document.images || [])
      if (!imgs.length) return done()

      let pending = imgs.filter((img) => !img.complete).length
      if (!pending) return done()

      imgs.forEach((img) => {
        if (img.complete) return
        img.addEventListener(
          'load',
          () => {
            if (--pending === 0) done()
          },
          { once: true }
        )
        img.addEventListener(
          'error',
          () => {
            if (--pending === 0) done()
          },
          { once: true }
        )
      })
    })
  },

  beforeDestroy() {
    document.body.classList.remove('pdf-mode')
  },

  head() {
    const isLandscape = this.doc && this.doc.orientation === 'landscape'
    const pageSize = isLandscape ? 'Letter landscape' : 'Letter'

    return {
      style: [
        {
          hid: 'print-page-size',
          type: 'text/css',
          cssText: `
            @media print {
              @page { size: ${pageSize}; margin: 0; }
            }
          `,
        },
      ],
    }
  },
}
</script>
