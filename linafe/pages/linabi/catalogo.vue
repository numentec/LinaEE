<template>
  <div>
    <MaterialCard class="mt-10">
      <template v-slot:heading>
        <v-toolbar dense color="secondary" class="mx-1" dark flat>
          <v-menu
            v-model="menuFilter"
            :close-on-content-click="false"
            :nudge-width="150"
            offset-y
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn dark icon v-bind="attrs" v-on="on">
                <v-icon>mdi-dots-vertical</v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item link>
                <v-list-item-icon>
                  <v-icon>mdi-cloud-download</v-icon>
                </v-list-item-icon>
                <v-list-item-title @click.stop="showBaseFilters = true">
                  Descargar Datos
                </v-list-item-title>
              </v-list-item>
              <v-list-item link>
                <v-list-item-icon>
                  <v-icon>mdi-table-cancel</v-icon>
                </v-list-item-icon>
                <v-list-item-title @click.stop="clearData">
                  Limpiar Datos
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
                <v-list-item-icon>
                  <v-icon>mdi-book-open-page-variant</v-icon>
                </v-list-item-icon>
                <v-list-item-title>Generar Catálogos</v-list-item-title>
              </v-list-item>
              <v-list-group prepend-icon="mdi-table-cog" no-action>
                <template v-slot:activator>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title>Consulta</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </template>
                <v-list-item link>
                  <v-list-item-content>
                    <v-list-item-title>Guardar</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item link>
                  <v-list-item-content>
                    <v-list-item-title>Abrir</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item link>
                  <v-list-item-content>
                    <v-list-item-title>Eliminar</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list-group>
              <v-list-group prepend-icon="mdi-cog" no-action>
                <template v-slot:activator>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title>Configuración</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </template>
                <v-list-item-group
                  v-model="showPanels"
                  multiple
                  active-class=""
                >
                  <v-list-item>
                    <template v-slot:default="{ active }">
                      <v-list-item-action>
                        <v-checkbox :input-value="active"></v-checkbox>
                      </v-list-item-action>

                      <v-list-item-content>
                        <v-list-item-title>Panel Agrupar</v-list-item-title>
                        <v-list-item-subtitle>
                          Agrupar y búsqueda global
                        </v-list-item-subtitle>
                      </v-list-item-content>
                    </template>
                  </v-list-item>

                  <v-list-item>
                    <template v-slot:default="{ active }">
                      <v-list-item-action>
                        <v-checkbox :input-value="active"></v-checkbox>
                      </v-list-item-action>

                      <v-list-item-content>
                        <v-list-item-title>Filtro avanzado</v-list-item-title>
                        <v-list-item-subtitle>
                          Fila de filtros avanzados
                        </v-list-item-subtitle>
                      </v-list-item-content>
                    </template>
                  </v-list-item>
                </v-list-item-group>
                <v-list-item link>
                  <v-list-item-content>
                    <v-list-item-title>Ajustes</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list-group>
            </v-list>
          </v-menu>
          <v-spacer />
          <v-toolbar-title>Catálogo de Productos</v-toolbar-title>
          <v-spacer />
          <v-btn dark icon @click="showColumnChooser">
            <v-icon>mdi-table-column-plus-after</v-icon>
          </v-btn>
        </v-toolbar>
      </template>
      <div ref="resizableDiv" v-resize="onResize">
        <DxDataGrid
          :ref="curGridRefKey"
          class="ma-4"
          :focused-row-enabled="true"
          :data-source="dataSource"
          :remote-operations="false"
          :allow-column-reordering="true"
          :row-alternation-enabled="true"
          :show-borders="true"
          :height="tableHeight"
          @content-ready="onContentReady"
        >
          <DxColumn
            width="200"
            :allow-grouping="false"
            data-field="REFERENCIA"
            name="FOTO"
            caption="Foto"
            cell-template="imgCellTemplate"
          />
          <DxColumn
            v-for="xcol in colsConfig"
            :key="xcol.id"
            :allow-grouping="xcol.configval7 == '1'"
            :data-field="xcol.configkey"
            :visible="xcol.configval2 == '1'"
            :caption="xcol.configval3"
            :data-type="xcol.configval4"
            :format="xcol.configval5"
            :alignment="xcol.configval6"
          />
          <DxSelection
            select-all-mode="allPages"
            show-check-boxes-mode="always"
            mode="multiple"
          />
          <DxLoadPanel :enable="true" />
          <DxGroupPanel :visible="showPanels.includes(0)" />
          <DxSearchPanel
            :visible="showPanels.includes(0)"
            :highlight-case-sensitive="true"
          />
          <DxColumnChooser mode="select" :allow-search="true" />
          <DxGrouping :auto-expand-all="false" />
          <DxFilterRow :visible="showPanels.includes(1)" />
          <DxHeaderFilter :visible="true" />
          <DxScrolling mode="virtual" />
          <DxPaging :page-size="100" />
          <template #imgCellTemplate="{ data: cellData }">
            <ImgForGrid :img-file="cellData" />
          </template>
        </DxDataGrid>
      </div>
    </MaterialCard>
    <BaseFilters
      :dialog.sync="showBaseFilters"
      :config="config.filter((e) => e.tipo == 'filter')"
      @closeDialog="closeDialog"
    />
  </div>
</template>
<script>
import { mapActions } from 'vuex'
import {
  DxDataGrid,
  DxColumn,
  DxGrouping,
  DxGroupPanel,
  DxSearchPanel,
  DxColumnChooser,
  DxFilterRow,
  DxHeaderFilter,
  DxScrolling,
  DxPaging,
  DxSelection,
} from 'devextreme-vue/data-grid'
import DxLoadPanel from 'devextreme-vue/load-panel'
import MaterialCard from '~/components/core/MaterialCard'
import BaseFilters from '~/components/linabi/BaseFilters'
import ImgForGrid from '~/components/utilities/ImgForGrid'
import 'devextreme/data/odata/store'

const curGridRefKey = 'cur-grid'

let collapsed = false

export default {
  components: {
    DxDataGrid,
    DxColumn,
    DxGrouping,
    DxGroupPanel,
    DxSearchPanel,
    DxColumnChooser,
    DxFilterRow,
    DxHeaderFilter,
    DxScrolling,
    DxPaging,
    DxSelection,
    DxLoadPanel,
    MaterialCard,
    BaseFilters,
    ImgForGrid,
  },
  async asyncData({ $axios, error }) {
    try {
      const { data } = await $axios.get('vistas/14/')
      return {
        config: data.configs_x_vista,
      }
    } catch (err) {
      if (err.response) {
        error({
          statusCode: err.response.status,
          message: err.response.data.detail,
        })
      } else {
        error({
          statusCode: 503,
          message: 'No se pudo cargar la configuración. Intente luego',
        })
      }
    }
  },
  data() {
    return {
      curGridRefKey,
      dataSource: null,
      showPanels: [],
      colsConfig: [],
      testVisible: false,
      menuFilter: false,
      radioGroup: '1',
      showBaseFilters: false,
      tableHeight: 0,
      onContentReady(e) {
        if (!collapsed) {
          e.component.expandRow(1)
          collapsed = true
        }
      },
    }
  },
  computed: {
    curGrid() {
      return this.$refs[curGridRefKey].instance
    },
  },
  mounted() {
    this.colsConfig = this.config.filter((e) => e.tipo === 'col')
    // const options = { p02: 'gorr%' }
    // const load = (loadOptions) => {
    //   return this.$axios
    //     .get('linabi/catalog/', {
    //       params: loadOptions,
    //     })
    //     .then((response) => response.data)
    // }
    // store = new CustomStore(load(options))
    // setTimeout(() => (this.dataSource = store))
    // this.dataSource = store
  },
  methods: {
    ...mapActions('linabi', [
      'setFilters',
      'setTotalCount',
      'fetchCatalogData',
    ]),
    clearData() {
      this.dataSource = null
      this.menuFilter = false
    },
    showColumnChooser() {
      this.curGrid.showColumnChooser()
    },
    closeDialog(refresh) {
      this.showBaseFilters = false
      if (refresh) {
        this.fetchCatalogData().then((store) => {
          this.dataSource = store
          this.setTotalCount(store.length)
        })
      }
    },
    onResize() {
      this.tableHeight =
        window.innerHeight -
        this.$refs.resizableDiv.getBoundingClientRect().y -
        82
    },
  },
  head() {
    return {
      title: 'Catálogo',
    }
  },
}
</script>
