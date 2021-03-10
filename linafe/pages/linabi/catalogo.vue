<template>
  <div>
    <MaterialCard class="mt-10">
      <template v-slot:heading>
        <v-toolbar dense color="secondary" dark flat>
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
            name="FOTO"
            data-field="REFERENCIA"
            caption="Foto"
            cell-template="imgCellTemplate"
          />
          <DxColumn data-field="ID" data-type="number" />
          <DxColumn data-field="REFERENCIA" data-type="string" caption="SKU" />
          <DxColumn
            :allow-grouping="false"
            data-field="DESCRIP"
            caption="DESCRIPCION"
          />
          <DxColumn
            data-field="PRECIO"
            caption="PRECIO"
            data-type="number"
            format="currency"
            alignment="right"
          />
          <DxColumn
            data-field="PRECIOPUBLICO"
            caption="PVP"
            data-type="number"
            format="currency"
            alignment="right"
          />
          <DxColumn data-field="DISPONIBLE_REAL" caption="DISPOIBLE" />
          <DxColumn data-field="DISTRIBUCION" data-type="string" />
          <DxColumn data-field="PAISORIGEN" data-type="string" />
          <DxSelection
            select-all-mode="allPages"
            show-check-boxes-mode="always"
            mode="multiple"
          />
          <DxLoadPanel :enable="true" />
          <DxGroupPanel :visible="true" />
          <DxSearchPanel :visible="true" :highlight-case-sensitive="true" />
          <DxColumnChooser mode="select" />
          <DxGrouping :auto-expand-all="false" />
          <DxFilterRow :visible="true" />
          <DxHeaderFilter :visible="true" />
          <DxScrolling mode="virtual" />
          <DxPaging :page-size="100" />
          <template #imgCellTemplate="{ data: cellData }">
            <ImgForGrid :img-file="cellData" />
          </template>
        </DxDataGrid>
      </div>
    </MaterialCard>
    <BaseFilters :dialog.sync="showBaseFilters" @closeDialog="closeDialog" />
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
  data() {
    return {
      curGridRefKey,
      dataSource: null,
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
    ...mapActions('linabi', ['setFilters', 'fetchCatalogData']),
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
