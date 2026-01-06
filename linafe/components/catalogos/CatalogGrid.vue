<template>
  <v-container fluid>
    <v-row>
      <v-col v-for="c in items" :key="c.id" cols="12" sm="6" md="4" lg="3">
        <CatalogCard
          :item="c"
          @open="$emit('open', $event)"
          @duplicate="$emit('duplicate', $event)"
          @share="$emit('share', $event)"
          @exportPdf="$emit('exportPdf', $event)"
          @archive="$emit('archive', $event)"
        />
      </v-col>
    </v-row>

    <v-sheet v-if="!items.length" class="pa-10 text-center" outlined rounded>
      <div class="text-h6 mb-2">Aún no tienes catálogos</div>
      <div class="text-body-2 mb-4 text--secondary">
        Crea tu primer catálogo y luego podrás exportarlo como PDF o compartirlo
        con un link.
      </div>
      <v-btn color="primary" @click="$emit('new')">
        <v-icon left>mdi-plus</v-icon> Crear primer catálogo
      </v-btn>
    </v-sheet>
  </v-container>
</template>

<script>
import CatalogCard from '~/components/catalogos/CatalogCard.vue'

export default {
  name: 'CatalogGrid',
  components: { CatalogCard },
  props: {
    items: { type: Array, default: () => [] },
  },
}
</script>
