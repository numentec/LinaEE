<template>
  <v-container>
    <!-- Cargando -->
    <v-sheet v-if="loading" class="pa-10 text-center" outlined>
      <v-progress-circular indeterminate color="primary" />
      <div class="text-body-2 text--secondary mt-4">Cargando la orden…</div>
    </v-sheet>

    <!-- Error: enlace inválido, vencido, orden cancelada, etc. -->
    <v-sheet v-else-if="errorInfo" class="pa-10 text-center" outlined>
      <v-icon x-large color="grey" class="mb-4">{{ errorInfo.icon }}</v-icon>
      <div class="text-h6 mb-2">{{ errorInfo.title }}</div>
      <div class="text-body-2 text--secondary">{{ errorInfo.text }}</div>
      <v-btn
        v-if="errorInfo.retry"
        text
        color="primary"
        class="mt-4"
        @click="load"
      >
        Reintentar
      </v-btn>
    </v-sheet>

    <!-- Orden -->
    <div v-else-if="order">
      <v-card outlined class="pa-3 mb-3">
        <div class="d-flex align-center flex-wrap">
          <div class="mr-4">
            <div class="text-subtitle-1 font-weight-medium">
              Orden # {{ order.id }}
              <v-chip x-small label class="ml-2" :color="statusColor" dark>
                {{ statusLabel }}
              </v-chip>
            </div>
            <div class="text-caption text--secondary">
              Enlace válido hasta
              {{ formatDateTime(order.public_token_expires_at) }}
            </div>
          </div>

          <v-spacer />

          <div class="d-flex flex-wrap">
            <v-btn
              text
              small
              color="primary"
              :loading="downloading === 'pdf'"
              :disabled="!!downloading"
              @click="download('pdf')"
            >
              <v-icon left>mdi-file-pdf-box</v-icon> PDF
            </v-btn>
            <v-btn
              text
              small
              color="primary"
              :loading="downloading === 'xlsx'"
              :disabled="!!downloading"
              @click="download('xlsx')"
            >
              <v-icon left>mdi-microsoft-excel</v-icon> Excel
            </v-btn>
            <v-btn
              text
              small
              color="primary"
              :loading="downloading === 'zip'"
              :disabled="!!downloading"
              @click="download('zip')"
            >
              <v-icon left>mdi-folder-zip-outline</v-icon> Imágenes (ZIP)
            </v-btn>
          </div>
        </div>
      </v-card>

      <v-row>
        <v-col cols="12" md="4" order-md="2">
          <OrderSummary
            :cur-order="order"
            hide-controls
            public-view
            outlined
            @copied="notify('Copiado al portapapeles', 'success')"
            @copy-error="notify('No se pudo copiar', 'error')"
          />
        </v-col>
        <v-col cols="12" md="8" order-md="1">
          <OrderCard v-for="item in order.items" :key="item.id" :item="item" />
          <div
            v-if="!order.items || !order.items.length"
            class="text-body-2 text--secondary pa-4"
          >
            Esta orden no tiene productos.
          </div>
        </v-col>
      </v-row>
    </div>

    <v-snackbar v-model="snackbar" timeout="4000" :color="snackbarColor" dark>
      {{ snackbarText }}
    </v-snackbar>
  </v-container>
</template>

<script>
import { mapActions } from 'vuex'
import OrderCard from '~/components/saleapp/OrderCard.vue'
import OrderSummary from '~/components/saleapp/OrderSummary.vue'
import { getOrderStatus } from '~/utils/orderStatus'

// Mensajes por tipo de error (status HTTP / code del backend)
const ERRORS = {
  not_found: {
    icon: 'mdi-link-off',
    title: 'Enlace inválido',
    text:
      'Este enlace no existe o fue desactivado. Solicita al vendedor un enlace nuevo.',
  },
  expired: {
    icon: 'mdi-timer-off-outline',
    title: 'Enlace vencido',
    text:
      'La vigencia de este enlace terminó. Solicita al vendedor que lo renueve.',
  },
  cancelled: {
    icon: 'mdi-cancel',
    title: 'Orden no disponible',
    text:
      'Esta orden fue cancelada. Contacta al vendedor para más información.',
  },
  throttled: {
    icon: 'mdi-timer-sand',
    title: 'Demasiadas solicitudes',
    text: 'Espera unos minutos e inténtalo de nuevo.',
    retry: true,
  },
  network: {
    icon: 'mdi-cloud-off-outline',
    title: 'No se pudo cargar la orden',
    text: 'Revisa tu conexión e inténtalo de nuevo.',
    retry: true,
  },
}

// Las descargas son blobs y no exponen el cuerpo del error: se decide por status
function errorKey(error) {
  const response = error && error.response
  if (!response) return 'network'
  if (response.status === 404) return 'not_found'
  if (response.status === 429) return 'throttled'
  if (response.status === 410) {
    const code = response.data && response.data.code
    return code === 'cancelled' ? 'cancelled' : 'expired'
  }
  return 'network'
}

export default {
  name: 'SharedOrderPage',
  layout: 'clean',
  components: { OrderCard, OrderSummary },

  data() {
    return {
      order: null,
      loading: true,
      errorInfo: null,
      downloading: '',
      snackbar: false,
      snackbarText: '',
      snackbarColor: 'info',
    }
  },

  computed: {
    token() {
      return this.$route.params.token
    },
    statusLabel() {
      return getOrderStatus(this.order?.status).text
    },
    statusColor() {
      return getOrderStatus(this.order?.status).color
    },
  },

  // La orden se carga solo en el navegador: así los bots de vista previa
  // no reciben datos y los visitantes no comparten la IP del servidor Nuxt
  mounted() {
    this.load()
  },

  methods: {
    ...mapActions('saleapp/orders', [
      'publicPdfDownload',
      'publicXlsxDownload',
      'imagesZipDownload',
    ]),

    async load() {
      this.loading = true
      this.errorInfo = null
      try {
        this.order = await this.$api.getPublicOrder(this.token)
      } catch (error) {
        this.order = null
        this.errorInfo = ERRORS[errorKey(error)]
      } finally {
        this.loading = false
      }
    },

    async download(kind) {
      const payload = { token: this.token, orderid: this.order.id }
      this.downloading = kind
      try {
        if (kind === 'pdf') await this.publicPdfDownload(payload)
        else if (kind === 'xlsx') await this.publicXlsxDownload(payload)
        else
          await this.imagesZipDownload({
            orderid: this.order.id,
            items: this.order.items,
          })
      } catch (error) {
        const key = error && error.response ? errorKey(error) : null
        if (key === 'expired' || key === 'cancelled' || key === 'not_found') {
          // El enlace dejó de ser válido mientras la página estaba abierta
          this.order = null
          this.errorInfo = ERRORS[key]
        } else {
          this.notify(
            key === 'throttled'
              ? ERRORS.throttled.text
              : kind === 'zip'
              ? 'No se encontraron imágenes para descargar.'
              : 'No se pudo descargar el archivo.',
            'error'
          )
        }
      } finally {
        this.downloading = ''
      }
    },

    notify(text, color = 'info') {
      this.snackbarText = text
      this.snackbarColor = color
      this.snackbar = true
    },

    formatDateTime(value) {
      if (!value) return '—'
      return new Date(value).toLocaleString([], {
        dateStyle: 'medium',
        timeStyle: 'short',
      })
    },
  },

  // Metadatos fijos (se incluyen en el HTML del servidor)
  head() {
    return {
      title: 'Orden compartida',
      meta: [
        { hid: 'robots', name: 'robots', content: 'noindex, nofollow' },
        { hid: 'referrer', name: 'referrer', content: 'no-referrer' },
      ],
    }
  },
}
</script>
