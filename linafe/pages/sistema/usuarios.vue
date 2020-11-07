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
                <v-list-item-title @click="showRegister = true">
                  Registrar Nuevo
                </v-list-item-title>
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
          <v-toolbar-title>Usuarios</v-toolbar-title>
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
            <SelCols />
          </v-menu>
          <div v-show="false">
            <v-select
              v-model="selected_cols"
              :items="headers"
              prepend-icon="mdi-table-column-plus-after"
              multiple
              return-object
            >
            </v-select>
          </div>
        </v-toolbar>
      </template>
      <v-card-title>
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Buscar"
          single-line
          hide-details
        ></v-text-field>
      </v-card-title>
      <v-card-text>
        <v-data-table
          :headers="showCols"
          :items="users"
          :items-per-page="10"
          multi-sort
          show-select
          :search="search"
          item-key="id"
        >
          <template #item.full_name="{ item }">
            {{ item.first_name }} {{ item.last_name }}
          </template>
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
    <UserRegister :dialog.sync="showRegister" @closeDialog="closeDialog" />
  </div>
</template>

<script>
export default {
  components: {
    MaterialCard: () => import('~/components/core/MaterialCard'),
    SelCols: () => import('~/components/utilities/SelCols'),
    UserRegister: () => import('~/components/core/UserRegister'),
  },

  async asyncData({ $axios, error }) {
    try {
      const { data } = await $axios.get('/users/')
      return {
        users: data,
      }
    } catch (err) {
      error({
        statusCode: 503,
        message: 'Unable to fetch users list at this time. Try later',
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
        { text: 'Nombre', value: 'full_name' },
        { text: 'Usuario', value: 'username' },
        { text: 'Email', value: 'email' },
        { text: 'Tel', value: 'tel1' },
        { text: 'Activo', sortable: false, value: 'is_active' },
        { text: 'Ver', value: 'actions', sortable: false },
      ],
      selected_cols: [],
      showRegister: false,
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
    showItem(item) {},
    closeDialog() {
      this.showRegister = false
    },
  },

  head() {
    return {
      title: 'Users List',
    }
  },
}
</script>
