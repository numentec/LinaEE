<template>
  <v-container>
    <v-card outlined class="pa-4">
      <div class="text-h6 mb-2">Nuevo catálogo</div>
      <v-row>
        <v-col cols="12" md="6">
          <v-text-field v-model="name" label="Nombre del catálogo" outlined />
        </v-col>

        <v-col cols="12" md="2">
          <v-select
            v-model="templateKey"
            :items="templateItems"
            label="Plantilla"
            outlined
          />
        </v-col>

        <v-col cols="12" md="2">
          <v-select
            v-model="orientation"
            :items="orientationItems"
            label="Orientación"
            outlined
          />
        </v-col>

        <v-col cols="12" md="2">
          <v-text-field v-model="companyId" label="Company ID" outlined />
        </v-col>
      </v-row>

      <div class="d-flex">
        <v-btn text @click="$router.push('/catalogos')">Cancelar</v-btn>
        <v-spacer />
        <v-btn
          color="primary"
          :loading="loading"
          :disabled="!canCreate || loading"
          @click="create"
        >
          Crear y editar
        </v-btn>
      </div>
    </v-card>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'CatalogosNewPage',

  data() {
    return {
      name: '',
      templateKey: 'minimal',
      orientation: 'portrait',
      companyId: 'cia_01',
      templateItems: [
        { text: 'Minimal', value: 'minimal' },
        { text: 'Fashion', value: 'fashion' },
        { text: 'Promo', value: 'promo' },
      ],
      orientationItems: [
        { text: 'Vertical (Carta)', value: 'portrait' },
        { text: 'Horizontal (Carta)', value: 'landscape' },
      ],
      loading: false,
    }
  },

  computed: {
    ...mapGetters('sistema', ['getCurCia']),

    canCreate() {
      return (this.name || '').trim().length >= 3
    },
  },

  mounted() {
    this.companyId = this.getCurCia.id
  },

  methods: {
    async create() {
      if (!this.canCreate) return

      this.loading = true

      try {
        const item = await this.$store.dispatch(
          'catalogo/catalogos/createCatalog',
          {
            name: this.name,
            template: this.templateKey,
            orientation: this.orientation,
            companyId: this.companyId,
          }
        )

        this.$router.push(`/catalogos/${item.id}/edit`)
      } catch (e) {
        console.error(e)
        this.$toast?.error?.('No se pudo crear el catálogo')
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
