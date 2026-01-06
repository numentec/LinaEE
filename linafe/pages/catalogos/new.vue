<template>
  <v-container>
    <v-card outlined class="pa-4">
      <div class="text-h6 mb-2">Nuevo catálogo</div>
      <div class="text-body-2 text--secondary mb-6">
        Por ahora crearemos con plantilla <strong>Minimal</strong>.
      </div>

      <v-row>
        <v-col cols="12" md="6">
          <v-text-field v-model="name" label="Nombre del catálogo" outlined />
        </v-col>

        <v-col cols="12" md="3">
          <v-select
            v-model="orientation"
            :items="orientationItems"
            label="Orientación"
            outlined
          />
        </v-col>

        <v-col cols="12" md="3">
          <v-text-field v-model="companyId" label="Company ID" outlined />
        </v-col>
      </v-row>

      <div class="d-flex">
        <v-btn text @click="$router.push('/catalogos')">Cancelar</v-btn>
        <v-spacer />
        <v-btn color="primary" @click="create"> Crear y editar </v-btn>
      </div>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: 'CatalogosNewPage',
  data() {
    return {
      name: '',
      orientation: 'portrait',
      companyId: 'cia_01',
      orientationItems: [
        { text: 'Vertical (Carta)', value: 'portrait' },
        { text: 'Horizontal (Carta)', value: 'landscape' },
      ],
    }
  },
  methods: {
    async create() {
      const item = await this.$store.dispatch('catalogos/createCatalog', {
        name: this.name,
        template: 'minimal',
        orientation: this.orientation,
        company_id: this.companyId,
      })
      this.$router.push(`/catalogos/${item.id}/edit`)
    },
  },
}
</script>
