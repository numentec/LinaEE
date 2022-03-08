/* eslint-disable no-console */
<template>
  <div>
    <MaterialCard class="mt-10">
      <template v-slot:heading>
        <v-toolbar dense color="secondary" class="mx-1" dark flat>
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn icon v-bind="attrs" v-on="on" @click="$router.back()">
                <v-icon>mdi-chevron-left</v-icon>
              </v-btn>
            </template>
            <span>Volver a vista anterior</span>
          </v-tooltip>
          <v-toolbar-title>Usuarios</v-toolbar-title>
          <v-spacer />
          <!-- <v-btn dark icon @click="testMethod">
            <v-icon>mdi-test-tube</v-icon>
          </v-btn> -->
          <v-menu
            v-model="menuConf"
            :nudge-width="200"
            :close-on-content-click="false"
            left
            offset-y
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn dark icon v-bind="attrs" v-on="on">
                <v-icon>mdi-cog-outline</v-icon>
              </v-btn>
            </template>
            <TableSettings
              :show-column-chooser="showColumnChooser"
              :set-filtros="setConf.filtros"
              :set-agrupar="setConf.agrupar"
              :ver="{ filtros: true, agrupar: false }"
              @set-conf-filtros="setConf.filtros = !setConf.filtros"
              @set-conf-agrupar="setConf.agrupar = !setConf.agrupar"
              @menu-conf-close="menuConf = false"
              @snkb="snackbar = true"
            />
          </v-menu>
          <v-menu
            v-model="menuMain"
            :close-on-content-click="false"
            :nudge-width="150"
            offset-y
            offset-x
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn dark icon v-bind="attrs" v-on="on">
                <v-icon>mdi-dots-vertical</v-icon>
              </v-btn>
            </template>
            <v-list nav>
              <v-list-item link>
                <v-list-item-icon>
                  <v-icon>mdi-account-plus</v-icon>
                </v-list-item-icon>
                <v-list-item-title
                  @click.stop="
                    showRegister = true
                    menuMain = false
                  "
                >
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
                    <v-list-item-title @click.stop="exportGrid(1)">
                      Excel
                    </v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item link>
                  <v-list-item-content>
                    <v-list-item-title>CSV</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item link>
                  <v-list-item-content>
                    <v-list-item-title @click.stop="exportGrid(3)">
                      PDF
                    </v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list-group>
              <v-list-item link>
                <v-list-item-icon>
                  <v-icon>mdi-table-refresh</v-icon>
                </v-list-item-icon>
                <v-list-item-title @click="$fetch">
                  Actualizar
                </v-list-item-title>
              </v-list-item>
              <v-list-group prepend-icon="mdi-cog" no-action>
                <template v-slot:activator>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title>Configuración</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </template>
                <v-list-item>
                  <v-list-item-action>
                    <v-switch v-model="setConf.agrupar"></v-switch>
                  </v-list-item-action>
                  <v-list-item-content>
                    <v-list-item-title>Panel Agrupar</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item>
                  <v-list-item-action>
                    <v-switch v-model="setConf.filtros"></v-switch>
                  </v-list-item-action>
                  <v-list-item-content>
                    <v-list-item-title>Filtro avanzado</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item link>
                  <v-list-item-content>
                    <v-list-item-title @click.stop="snackbar = true"
                      >Ajustes</v-list-item-title
                    >
                  </v-list-item-content>
                </v-list-item>
              </v-list-group>
            </v-list>
          </v-menu>
        </v-toolbar>
      </template>
      <div ref="resizableDiv" v-resize="onResize">
        <DxDataGrid
          :ref="curGridRefKey"
          :focused-row-enabled="true"
          :data-source="dataSource"
          :remote-operations="false"
          :column-auto-width="true"
          :allow-column-reordering="true"
          :allow-column-resizing="true"
          column-resizing-mode="widget"
          :row-alternation-enabled="true"
          :show-column-lines="true"
          :show-row-lines="false"
          :show-borders="true"
          :height="tableHeight"
        >
          <DxColumn
            width="100"
            :allow-grouping="false"
            data-field="foto"
            caption="Foto"
            cell-template="imgCellTemplate"
            :allow-header-filtering="false"
            :allow-reordering="false"
            :allow-sorting="false"
          />
          <DxColumn
            v-for="(xcol, index) in colsConfig"
            :key="index"
            :data-field="xcol.df"
            :visible="xcol.v"
            :caption="xcol.caption"
            :allow-sorting="xcol.s"
          >
          </DxColumn>
          <DxColumn
            :width="100"
            data-field="online.is_online"
            caption="OnLine"
            cell-template="icoOnline"
            alignment="center"
            :allow-sorting="true"
          />
          <DxColumn
            :width="75"
            caption="Perfil"
            cell-template="btnPerfil"
            alignment="center"
            :allow-sorting="false"
          />
          <DxSearchPanel :visible="true" :highlight-case-sensitive="true" />
          <DxColumnChooser
            mode="select"
            :allow-search="true"
            :height="360"
            title="Columnas"
          />
          <DxFilterRow :visible="setConf.filtros" />
          <DxHeaderFilter :visible="true" />
          <DxPaging :page-size="10" />
          <DxSelection
            select-all-mode="allPages"
            show-check-boxes-mode="always"
            mode="multiple"
          />
          <template #icoOnline="{ data: cellData }">
            <v-menu open-on-hover top offset-y :nudge-width="100">
              <template v-slot:activator="{ on, attrs }">
                <v-btn icon>
                  <v-icon
                    v-if="cellData.data.online.is_online == 'ON'"
                    color="green lightn-2"
                    v-bind="attrs"
                    v-on="on"
                  >
                    mdi-account-network-outline
                  </v-icon>
                  <v-icon v-else color="grey"> mdi-connection </v-icon>
                </v-btn>
              </template>
              <v-card>
                <v-list>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title>
                        {{ cellData.data.fullname }}
                      </v-list-item-title>
                      <v-list-item-subtitle>
                        {{ cellData.data.username }}
                      </v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>
                      {{ `Inicio: ${cellData.data.online.last_login}` }}
                    </v-list-item-title>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-title>
                      {{ `Origen: ${cellData.data.online.fromip}` }}
                    </v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-card>
            </v-menu>
          </template>
          <template #btnPerfil="{ data: cellData }">
            <v-btn icon @click="showProfile(cellData)">
              <v-icon color="primary lightn-2">mdi-account-details</v-icon>
            </v-btn>
          </template>
          <template #imgCellTemplate="{ data }">
            <ImgForGrid :img-file="data.value" />
          </template>
        </DxDataGrid>
      </div>
    </MaterialCard>
    <UserRegister :dialog.sync="showRegister" @closeDialog="closeDialog" />
    <v-snackbar v-model="snackbar" timeout="2000">
      No implementado
      <template v-slot:action="{ attrs }">
        <v-btn color="secondary" text v-bind="attrs" @click="snackbar = false">
          Cerrar
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import {
  DxDataGrid,
  DxColumn,
  DxSearchPanel,
  DxColumnChooser,
  DxFilterRow,
  DxHeaderFilter,
  DxPaging,
  DxSelection,
} from 'devextreme-vue/data-grid'
import MaterialCard from '~/components/core/MaterialCard'
import UserRegister from '~/components/core/UserRegister'
import ImgForGrid from '~/components/utilities/ImgForGrid'
import TableSettings from '~/components/utilities/TableSettings'

const curGridRefKey = 'cur-grid'

export default {
  name: 'UserList',
  components: {
    DxDataGrid,
    DxColumn,
    DxSearchPanel,
    DxColumnChooser,
    DxFilterRow,
    DxHeaderFilter,
    DxPaging,
    DxSelection,
    MaterialCard,
    UserRegister,
    ImgForGrid,
    TableSettings,
  },

  async fetch() {
    // Lista de usuarios
    await this.fetchUsers().then((store) => {
      this.dataSource = store
    })
  },

  data() {
    return {
      curGridRefKey,
      dataSource: null,
      menuMain: false,
      menuConf: false,
      setConf: {
        filtros: true,
        agrupar: false,
      },
      colsConfig: [
        { caption: 'ID', df: 'id', v: true, s: true },
        { caption: 'Nombre', df: 'fullname', v: true, s: true },
        { caption: 'Usuario', df: 'username', v: true, s: true },
        { caption: 'Email', df: 'email', v: true, s: true },
        { caption: 'Tel', df: 'tel1', v: true, s: true },
        { caption: 'Activo', df: 'is_active', v: false, s: false },
      ],
      showRegister: false,
      snackbar: false,
      tableHeight: 0,
    }
  },

  computed: {
    curGrid() {
      return this.$refs[curGridRefKey].instance
    },
  },

  mounted() {
    this.setConf.filtros = true
  },

  methods: {
    ...mapActions('sistema', ['fetchUsers']),
    showProfile(data) {
      this.$router.push({ path: 'usuarios/' + data.key })
    },
    refreshItems() {
      this.$fetch()
    },
    showItem(item) {
      alert(item.email)
    },
    closeDialog(refresh) {
      this.showRegister = false
      if (refresh) {
        this.refreshItems()
      }
    },
    exportGrid(value) {
      return value
    },
    onResize() {
      this.tableHeight =
        window.innerHeight -
        this.$refs.resizableDiv.getBoundingClientRect().y -
        82
    },
    showColumnChooser() {
      this.curGrid.showColumnChooser()
      this.menuConf = false
    },
  },
  head() {
    return {
      title: 'Users List',
    }
  },
}
</script>
