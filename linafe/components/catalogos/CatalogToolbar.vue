<template>
  <v-toolbar flat>
    <v-toolbar-title>Mis catálogos</v-toolbar-title>
    <v-spacer />

    <v-text-field
      v-model="searchLocal"
      hide-details
      dense
      outlined
      prepend-inner-icon="mdi-magnify"
      label="Buscar"
      style="max-width: 360px"
      @input="$emit('update:search', searchLocal)"
    />

    <v-btn class="ml-3" color="primary" @click="$emit('new')">
      <v-icon left>mdi-plus</v-icon>
      Nuevo catálogo
    </v-btn>
  </v-toolbar>
</template>

<script>
export default {
  name: 'CatalogToolbar',
  props: {
    search: { type: String, default: '' },
  },
  data() {
    return { searchLocal: this.search }
  },
  watch: {
    search(val) {
      this.searchLocal = val
    },
  },
}
</script>
