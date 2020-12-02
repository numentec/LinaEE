<template>
  <div>
    <MaterialCard class="mt-10">
      <template v-slot:heading>
        <v-toolbar dense color="secondary" dark flat>
          <v-menu :close-on-content-click="false" offset-y>
            <template v-slot:activator="{ on, attrs }">
              <v-btn dark icon v-bind="attrs" v-on="on">
                <v-icon>mdi-dots-vertical</v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item link>
                <v-list-item-title>Nuevo</v-list-item-title>
              </v-list-item>
              <v-list-group prepend-icon="mdi-export" no-action>
                <template v-slot:activator>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title>Exportar</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </template>
                <v-list-item link>
                  <v-list-item-content>
                    <v-list-item-title>Excel</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item link>
                  <v-list-item-content>
                    <v-list-item-title>CSV</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item link>
                  <v-list-item-content>
                    <v-list-item-title>PDF</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list-group>
              <v-list-item link>
                <v-list-item-title>Imprimir</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
          <v-spacer />
          <v-toolbar-title>Proveedores</v-toolbar-title>
          <v-spacer />
          <v-menu
            v-model="menu"
            :close-on-content-click="false"
            :nudge-width="200"
            offset-y
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn dark icon v-bind="attrs" v-on="on">
                <v-icon>mdi-table-column-plus-after</v-icon>
              </v-btn>
            </template>
            <SelCols :cols-headers="headers" @hide-cols="hideCols" />
          </v-menu>
        </v-toolbar>
      </template>
      <v-card-title>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Buscar"
          single-line
          hide-details
        ></v-text-field>
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>
        <v-btn fab small color="grey lighten-4" @click="refreshData">
          <v-icon color="grey lighten-1">mdi-sync-circle</v-icon>
        </v-btn>
      </v-card-title>
      <v-card-text>
        <v-data-table
          :headers="showCols"
          :items="stakeholders"
          :items-per-page="10"
          multi-sort
          show-select
          :search="search"
          item-key="id"
        >
          <template v-slot:item.is_active="{ item }">
            <v-simple-checkbox
              v-model="item.is_active"
              disabled
            ></v-simple-checkbox>
          </template>
          <template v-slot:item.actions="{ item }">
            <v-icon @click="showItem(item)">mdi-file-eye-outline</v-icon>
          </template>
        </v-data-table>
      </v-card-text>
    </MaterialCard>
  </div>
</template>

<script>
export default {
  components: {
    MaterialCard: () => import('~/components/core/MaterialCard'),
    SelCols: () => import('~/components/utilities/SelCols'),
  },

  async asyncData({ $axios, error }) {
    try {
      const { data } = await $axios.get('stakeholders/', {
        params: { shtype: 'Proveedor' },
      })
      return {
        stakeholders: data,
      }
    } catch (err) {
      error({
        statusCode: 503,
        message: 'Unable to fetch customers list at this time. Try later',
      })
    }
  },

  data() {
    return {
      page_name: 'page',
      menu: false,
      search: '',
      headers: [
        { text: 'ID', value: 'id' },
        { text: 'Código', value: 'codigo' },
        { text: 'Nombre', value: 'nombre' },
        { text: 'RUC', value: 'ruc' },
        { text: 'Email', value: 'email' },
        { text: 'Tel', value: 'tel1' },
        { text: 'Ver', value: 'actions', sortable: false },
      ],
      selected_cols: [],
    }
  },

  computed: {
    showCols() {
      return this.headers.filter((s) => this.selected_cols.includes(s))
    },
  },

  created() {
    this.selected_cols = this.headers
  },

  methods: {
    async refreshData() {
      try {
        const { data } = await this.$axios.get('stakeholders/', {
          params: { shtype: 'Proveedor' },
        })
        this.stakeholders = data
        // return stakeholders
      } catch (err) {
        this.$error({
          statusCode: 503,
          message: 'Unable to fetch customers list at this time. Try later',
        })
      }
    },
    hideCols(xcols) {
      this.selected_cols = xcols.colssel
      this.menu = xcols.menu
    },
    showItem(item) {
      alert(item.nombre)
    },
  },

  head() {
    return {
      title: 'Proveedores',
    }
  },
}
</script>
