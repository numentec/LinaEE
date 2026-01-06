<template>
  <div class="d-flex flex-wrap align-center px-4 pb-2">
    <v-chip-group
      v-model="statusLocal"
      mandatory
      active-class="primary--text"
      @change="$emit('update:status', statusLocal)"
    >
      <v-chip value="all">Todos</v-chip>
      <v-chip value="draft">Borradores</v-chip>
      <v-chip value="ready">Listos</v-chip>
      <v-chip value="sent">Enviados</v-chip>
      <v-chip value="archived">Archivados</v-chip>
    </v-chip-group>

    <v-spacer />

    <v-select
      v-model="templateLocal"
      :items="templateItems"
      dense
      outlined
      hide-details
      label="Plantilla"
      style="max-width: 180px"
      class="mr-2"
      @change="$emit('update:template', templateLocal)"
    />

    <v-select
      v-model="sortLocal"
      :items="sortItems"
      dense
      outlined
      hide-details
      label="Ordenar"
      style="max-width: 220px"
      @change="$emit('update:sort', sortLocal)"
    />
  </div>
</template>

<script>
export default {
  name: 'CatalogFilters',
  props: {
    status: { type: String, default: 'all' },
    template: { type: String, default: 'all' },
    sort: { type: String, default: 'updated_desc' },
  },
  data() {
    return {
      statusLocal: this.status,
      templateLocal: this.template,
      sortLocal: this.sort,
      templateItems: [
        { text: 'Todas', value: 'all' },
        { text: 'Minimal', value: 'minimal' },
        { text: 'Fashion (próx.)', value: 'fashion', disabled: true },
        { text: 'Promo (próx.)', value: 'promo', disabled: true },
      ],
      sortItems: [
        { text: 'Última edición (desc)', value: 'updated_desc' },
        { text: 'Nombre (A-Z)', value: 'name_asc' },
        { text: 'Estado', value: 'status_asc' },
      ],
    }
  },
}
</script>
