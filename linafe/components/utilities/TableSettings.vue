<template>
  <div>
    <v-card>
      <v-list nav dense>
        <v-list-item>
          <v-list-item-action>
            <v-btn icon @click="showColumnChooser">
              <v-icon color="primary darken-2">
                mdi-table-column-plus-after
              </v-icon>
            </v-btn>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title> Seleccionar columnas </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <v-divider></v-divider>

      <v-list nav dense>
        <v-list-item v-show="ver.filtros">
          <v-list-item-action>
            <v-switch
              :value="setFiltros"
              @change="$emit('set-conf-filtros')"
            ></v-switch>
          </v-list-item-action>
          <v-list-item-title>Filtros Avanzados</v-list-item-title>
        </v-list-item>

        <v-list-item v-show="ver.agrupar">
          <v-list-item-action>
            <v-switch
              :value="setAgrupar"
              @change="$emit('set-conf-agrupar')"
            ></v-switch>
          </v-list-item-action>
          <v-list-item-title>Panel agrupar</v-list-item-title>
        </v-list-item>

        <!-- <v-list-item>
          <v-list-item-action>
            <v-switch @change="$emit('set-conf-totglobal')"></v-switch>
          </v-list-item-action>
          <v-list-item-title>Total global</v-list-item-title>
        </v-list-item> -->
        <v-list-item link>
          <v-list-item-icon>
            <v-icon>mdi-filter-variant-remove</v-icon>
          </v-list-item-icon>
          <v-list-item-title @click="$emit('clear-all-filters')">
            Limpiar filtros
          </v-list-item-title>
        </v-list-item>

        <v-list-item link>
          <v-list-item-icon>
            <v-icon>mdi-table-cog</v-icon>
          </v-list-item-icon>
          <v-list-item-title @click="$emit('snkb')">Ajustes</v-list-item-title>
        </v-list-item>
      </v-list>

      <v-divider></v-divider>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" text @click="$emit('menu-conf-close')">
          Cerrar
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
export default {
  name: 'TableSettings',
  props: {
    showColumnChooser: {
      type: Function,
      default: () => ({}),
    },
    setAgrupar: {
      type: Boolean,
      default: false,
    },
    setFiltros: {
      type: Boolean,
      default: false,
    },
    ver: {
      type: Object,
      default: () => ({ agrupar: true, filtros: true }),
    },
  },
}
</script>

<style lang="scss" scoped></style>
