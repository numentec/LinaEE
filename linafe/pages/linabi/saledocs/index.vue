/* eslint-disable no-console */
<template>
  <div>
    <div>
      <v-breadcrumbs class="mt-0" :items="breadCrumbsItems"></v-breadcrumbs>
    </div>
    <div>
      <MaterialCard class="mt-5">
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
                    <v-icon>mdi-ballot-recount-outline</v-icon>
                  </v-list-item-icon>
                  <v-list-item-title @click.stop="loadDetails"
                    >Descargar Detalle</v-list-item-title
                  >
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
                      <v-list-item-title @click.stop="exportGrid(1)">
                        Excel
                      </v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item v-show="expDetail" link>
                    <v-list-item-content>
                      <v-list-item-title @click.stop="exportGrid(2)">
                        Excel BC
                      </v-list-item-title>
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
                      <v-list-item-title @click.stop="snackbar = true"
                        >Guardar</v-list-item-title
                      >
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item link>
                    <v-list-item-content>
                      <v-list-item-title @click.stop="snackbar = true"
                        >Abrir</v-list-item-title
                      >
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item link>
                    <v-list-item-content>
                      <v-list-item-title @click.stop="snackbar = true"
                        >Eliminar</v-list-item-title
                      >
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
                  <v-list-item v-show="tab == 0">
                    <v-list-item-action>
                      <v-switch v-model="setConf0.agrupar"></v-switch>
                    </v-list-item-action>
                    <v-list-item-content>
                      <v-list-item-title>Panel Agrupar</v-list-item-title>
                      <v-list-item-subtitle>
                        Agrupar y búsqueda global
                      </v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item v-show="tab == 0">
                    <v-list-item-action>
                      <v-switch v-model="setConf0.filtros"></v-switch>
                    </v-list-item-action>
                    <v-list-item-content>
                      <v-list-item-title>Filtro avanzado</v-list-item-title>
                      <v-list-item-subtitle>
                        Fila de filtros avanzados
                      </v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item v-show="tab == 1">
                    <v-list-item-action>
                      <v-switch v-model="setConf1.agrupar"></v-switch>
                    </v-list-item-action>
                    <v-list-item-content>
                      <v-list-item-title>Panel Agrupar</v-list-item-title>
                      <v-list-item-subtitle>
                        Agrupar y búsqueda global
                      </v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item v-show="tab == 1">
                    <v-list-item-action>
                      <v-switch v-model="setConf1.filtros"></v-switch>
                    </v-list-item-action>
                    <v-list-item-content>
                      <v-list-item-title>Filtro avanzado</v-list-item-title>
                      <v-list-item-subtitle>
                        Fila de filtros avanzados
                      </v-list-item-subtitle>
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
            <v-spacer />
            <v-toolbar-title>Documentos de Ventas</v-toolbar-title>
            <v-spacer />
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
                v-show="tab == 0"
                ref="settings0"
                :show-column-chooser="showColumnChooser"
                :set-filtros="setConf0.filtros"
                :set-agrupar="setConf0.agrupar"
                @set-conf-filtros="setConf0.filtros = !setConf0.filtros"
                @set-conf-agrupar="setConf0.agrupar = !setConf0.agrupar"
                @menu-conf-close="menuConf = false"
                @snkb="snackbar = true"
              />
              <TableSettings
                v-show="tab == 1"
                ref="settings1"
                :show-column-chooser="showColumnChooser"
                :set-filtros="setConf1.filtros"
                :set-agrupar="setConf1.agrupar"
                @set-conf-filtros="setConf1.filtros = !setConf1.filtros"
                @set-conf-agrupar="setConf1.agrupar = !setConf1.agrupar"
                @menu-conf-close="menuConf = false"
                @snkb="snackbar = true"
              />
            </v-menu>
          </v-toolbar>
        </template>
        <div ref="resizableDiv" v-resize="onResize">
          <v-tabs v-model="tab" vertical icons-and-text>
            <v-tab key="tab0">
              Lista
              <v-icon left> mdi-format-list-checks </v-icon>
            </v-tab>
            <v-tab key="tab1">
              Detalle
              <v-icon left> mdi-ballot-outline </v-icon>
            </v-tab>
            <v-tabs-items v-model="tab">
              <v-tab-item key="tab0">
                <DxDataGrid
                  :ref="curGridRefKey0"
                  :focused-row-enabled="true"
                  :data-source="dataSource0"
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
                  :width="tableWidth"
                >
                  <DxColumn
                    v-for="xcol in colsConfig0"
                    :key="'tab0' + xcol.id"
                    :allow-grouping="xcol.configval7 == '1'"
                    :data-field="xcol.configkey"
                    :visible="xcol.configval2 == '1'"
                    :caption="xcol.configval3"
                    :data-type="xcol.configval4"
                    :format="setFormat(xcol.configval5)"
                    :alignment="xcol.configval6"
                  />
                  <DxGrouping :auto-expand-all="false" />
                  <DxGroupPanel
                    :visible="setConf0.agrupar"
                    empty-panel-text="Arrastre aquí el encabezado de una columna para agrupar"
                  />
                  <DxSearchPanel
                    :visible="setConf0.agrupar"
                    :highlight-case-sensitive="true"
                  />
                  <DxColumnChooser
                    mode="select"
                    :allow-search="true"
                    :height="360"
                    title="Ver Columna"
                  />
                  <DxFilterRow :visible="setConf0.filtros" />
                  <DxHeaderFilter :visible="true" />
                  <DxScrolling mode="virtual" />
                  <DxPaging :page-size="100" />
                  <DxSelection
                    select-all-mode="allPages"
                    show-check-boxes-mode="always"
                    mode="multiple"
                  />
                  <DxSummary>
                    <template v-for="gcol in colsWithSummary0">
                      <DxGroupItem
                        :key="'gi0' + gcol.id"
                        :column="gcol.configkey"
                        :align-by-column="true"
                        :summary-type="gcol.configval8"
                        :value-format="setFormat(gcol.configval5)"
                        :display-format="setDFormat('gi', gcol.configval8)"
                      />
                      <DxTotalItem
                        :key="'ti0' + gcol.id"
                        :column="gcol.configkey"
                        :summary-type="gcol.configval8"
                        :value-format="setFormat(gcol.configval5)"
                        :display-format="setDFormat('ti', gcol.configval8)"
                      />
                    </template>
                  </DxSummary>
                  <DxLoadPanel :enable="true" />
                </DxDataGrid>
              </v-tab-item>
              <v-tab-item key="tab1">
                <DxDataGrid
                  :ref="curGridRefKey1"
                  :focused-row-enabled="true"
                  :data-source="dataSource1"
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
                  :width="tableWidth"
                >
                  <DxColumn
                    width="200"
                    :allow-grouping="false"
                    data-field="REFERENCIA"
                    name="FOTO"
                    caption="Foto"
                    cell-template="imgCellTemplate"
                    :allow-header-filtering="false"
                  />
                  <DxColumn
                    v-for="xcol in colsConfig1"
                    :key="'tab1' + xcol.id"
                    :allow-grouping="xcol.configval7 == '1'"
                    :data-field="xcol.configkey"
                    :visible="xcol.configval2 == '1'"
                    :caption="xcol.configval3"
                    :data-type="xcol.configval4"
                    :format="setFormat(xcol.configval5)"
                    :alignment="xcol.configval6"
                  />
                  <DxGrouping :auto-expand-all="false" />
                  <DxGroupPanel
                    :visible="setConf1.agrupar"
                    empty-panel-text="Arrastre aquí el encabezado de una columna para agrupar"
                  />
                  <DxSearchPanel
                    :visible="setConf1.agrupar"
                    :highlight-case-sensitive="true"
                  />
                  <DxColumnChooser
                    ref="chooser1"
                    mode="select"
                    :allow-search="true"
                    :height="360"
                    title="Ver Columna"
                  />
                  <DxFilterRow :visible="setConf1.filtros" />
                  <DxHeaderFilter :visible="true" />
                  <DxScrolling mode="virtual" />
                  <DxPaging :page-size="100" />
                  <DxSelection
                    select-all-mode="allPages"
                    show-check-boxes-mode="always"
                    mode="multiple"
                  />
                  <DxSummary>
                    <template v-for="gcol in colsWithSummary1">
                      <DxGroupItem
                        :key="'gi1' + gcol.id"
                        :column="gcol.configkey"
                        :summary-type="gcol.configval8"
                        :value-format="setFormat(gcol.configval5)"
                        :display-format="setDFormat('gi', gcol.configval8)"
                      />
                      <DxTotalItem
                        :key="'ti1' + gcol.id"
                        :column="gcol.configkey"
                        :summary-type="gcol.configval8"
                        :value-format="setFormat(gcol.configval5)"
                        :display-format="setDFormat('ti', gcol.configval8)"
                      />
                    </template>
                  </DxSummary>
                  <DxLoadPanel :enable="true" />
                  <template #imgCellTemplate="{ data: cellData }">
                    <ImgForGrid :img-file="cellData" />
                  </template>
                </DxDataGrid>
              </v-tab-item>
            </v-tabs-items>
          </v-tabs>
        </div>
      </MaterialCard>
      <BaseFilters
        :dialog.sync="showBaseFilters"
        :config="config0.filter((el) => el.tipo == 'filter')"
        :numvista="16"
        curstore="linabi/saledocsm"
        @closeDialog="closeDialog"
      />
    </div>
    <LoadingView :busy-with="busyWith" :message="loadingMessage" />
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
import { mapState, mapActions } from 'vuex'
import { mapFields } from 'vuex-map-fields'
import { locale } from 'devextreme/localization'
import {
  DxDataGrid,
  DxColumn,
  DxSummary,
  DxGroupItem,
  DxTotalItem,
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
import saveAs from 'file-saver'
import { jsPDF as JsPDF } from 'jspdf'
import 'jspdf-autotable'
import ExcelJS from 'exceljs'
import { exportDataGrid as exportDataGridToPdf } from 'devextreme/pdf_exporter'
import { exportDataGrid as exportDataGridToExcel } from 'devextreme/excel_exporter'
import MaterialCard from '~/components/core/MaterialCard'
import BaseFilters from '~/components/linabi/BaseFilters'
import ImgForGrid from '~/components/utilities/ImgForGrid'
import TableSettings from '~/components/utilities/TableSettings'
import LoadingView from '~/components/utilities/LoadingView'

const curGridRefKey0 = 'cur-grid1'
const curGridRefKey1 = 'cur-grid2'
let collapsed = false

async function addImageExcel(url, workbook, worksheet, excelCell, ax, resolve) {
  // url = this.$config.publicURL + url
  // ax.onResponse((response) => {
  //   if (response.status === 404) {
  //       console.log('Oh no it returned a 404')
  //   }
  // })

  await ax
    .get(url, {
      responseType: 'arraybuffer',
    })
    .then((response) => {
      const base64Img = Buffer.from(response.data, 'binary').toString('base64')

      const image = workbook.addImage({
        base64: base64Img,
        extension: 'JPEG',
      })

      worksheet.getRow(excelCell.row).height = 100
      worksheet.addImage(image, {
        tl: { col: excelCell.col - 1, row: excelCell.row - 1 },
        br: { col: excelCell.col, row: excelCell.row },
      })

      resolve()
    })
    .catch(() => {
      // if (err.response.status === 404) {
      worksheet.getRow(excelCell.row).height = 100
      resolve()
      // }
    })
}

export default {
  name: 'SaleDocs',
  components: {
    DxDataGrid,
    DxColumn,
    DxSummary,
    DxGroupItem,
    DxTotalItem,
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
    TableSettings,
    LoadingView,
  },

  async asyncData({ $axios, error }) {
    try {
      const [conf0, conf1] = await Promise.all([
        $axios.get('vistas/16/'),
        $axios.get('vistas/17/'),
      ])
      return {
        config0: conf0.data.configs_x_vista,
        config1: conf1.data.configs_x_vista,
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
      tab: 0,
      curGridRefKey0,
      curGridRefKey1,
      dataSource0: null,
      dataSource1: null,
      menuConf: false,
      setConf0: {
        filtros: false,
        agrupar: false,
      },
      setConf1: {
        filtros: false,
        agrupar: false,
      },
      colsConfig0: [],
      colsConfig1: [],
      menuFilter: false,
      radioGroup: '1',
      showBaseFilters: false,
      tableHeight: 0,
      tableWidth: 0,
      snackbar: false,
      onContentReady(e) {
        if (!collapsed) {
          e.component.expandRow(1)
          collapsed = true
        }
      },
      busyWith: false,
      loadingMessage: 'Exportando...',
    }
  },
  computed: {
    ...mapState('linabi/favoritos', ['breadCrumbsItems']),
    ...mapFields('linabi/saledocsm', ['filters']),
    curGrid0() {
      return this.$refs[curGridRefKey0].instance
    },
    curGrid1() {
      return this.$refs[curGridRefKey1].instance
    },
    colsWithSummary0() {
      return this.colsConfig0.filter((obj) => obj.configval8 !== '')
    },
    colsWithSummary1() {
      return this.colsConfig1.filter((obj) => obj.configval8 !== '')
    },
    expDetail() {
      let result = false
      if (this.menuFilter) {
        if (this.$refs[curGridRefKey1]) {
          const grd = this.$refs[curGridRefKey1].instance
          result = grd.columnOption('TALLA', 'visible')
        }
      }
      return result
    },
  },
  created() {
    locale(navigator.language)
  },
  mounted() {
    this.colsConfig0 = this.config0.filter((e) => e.tipo === 'col')
    this.colsConfig1 = this.config1.filter((e) => e.tipo === 'col')
  },
  methods: {
    ...mapActions('linabi/saledocsm/', ['setTotalCount', 'fetchData']),
    ...mapActions({
      setFiltersDetails: 'linabi/saledocsd/setFilters',
      fetchDataDetails: 'linabi/saledocsd/fetchData',
    }),
    ...mapActions('linabi/common', ['fetchVariants']),
    clearData() {
      if (this.tab === 1) {
        this.dataSource1 = null
      } else {
        this.dataSource0 = null
        this.dataSource1 = null
      }

      this.menuFilter = false
    },
    showColumnChooser() {
      if (this.tab === 0) {
        this.curGrid0.showColumnChooser()
      } else {
        this.curGrid1.showColumnChooser()
      }
      this.menuConf = false
    },
    closeDialog(refresh) {
      this.showBaseFilters = false
      if (refresh) {
        this.fetchData().then((store) => {
          this.dataSource0 = store
          // this.setTotalCount(store.length)
        })
      }
    },
    loadDetails() {
      const selectedRows = this.curGrid0.getSelectedRowKeys()
      this.menuFilter = false
      if (selectedRows.length) {
        const numdocs = selectedRows.toString()
        const tipodoc = this.filters.p15

        this.setFiltersDetails({ p01: numdocs, p15: tipodoc })
        this.fetchDataDetails().then((store) => {
          this.dataSource1 = store
        })
        this.tab = 1
      }
    },
    onResize() {
      this.tableHeight =
        window.innerHeight -
        this.$refs.resizableDiv.getBoundingClientRect().y -
        82
      this.tableWidth =
        this.$refs.resizableDiv.getBoundingClientRect().width - 100
    },
    setFormat(opc) {
      if (opc === 'currency') {
        opc = '#,##0.00'
      }
      if (opc === 'decimal') {
        opc = '#,##0.0###'
      }
      if (opc === 'date') {
        opc = 'dd/MM/yyyy'
      }
      return opc
    },
    setDFormat(itype, stype) {
      const stypes = {
        sum: (itype) => (itype === 'gi' ? 'Sub Total: {0}' : 'Total: {0}'),
        count: (itype) => (itype === 'gi' ? '{0} Regs. ' : '{0} Registros'),
      }

      return stypes[stype]?.(itype) ?? ''
    },
    exportGrid(opc) {
      let curGrid

      const ax = this.$axios.create({
        baseURL: this.$config.fotosURL,
        headers: {
          common: {
            Accept: 'image/*, application/json, text/plain, */*',
          },
        },
      })

      if (this.tab === 0) {
        curGrid = {
          component: this.curGrid0,
          docname: 'ventas',
        }
      } else {
        curGrid = {
          component: this.curGrid1,
          docname: 'ventas_detalle',
        }
      }

      // Exportar a Excel
      if (opc === 1) {
        this.doExportExcel([], ax, curGrid)
      }

      // Exportar a Excel con detalle de códigos de barra
      if (opc === 2) {
        const selectedRows = curGrid.component.getSelectedRowKeys()
        this.fetchVariants({ sku: selectedRows }).then((vv) => {
          this.doExportExcel(vv, ax, curGrid)
        })
      }

      // Exportar a PDF
      if (opc === 3) {
        this.doExportPDF(curGrid)
      }
    },

    doExportPDF(curGrid) {
      this.busyWith = true
      const pdfDoc = new JsPDF({
        orientation: 'landscape',
        format: 'letter',
      })

      let mch = { minCellHeight: 5 }
      if (curGrid.docname === 'ventas_detalle') {
        if (curGrid.columnOption('FOTO', 'visible')) {
          mch = { minCellHeight: 20 }
        }
      }

      exportDataGridToPdf({
        component: curGrid.component,
        jsPDFDocument: pdfDoc,
        selectedRowsOnly: true,
        autoTableOptions: {
          bodyStyles: mch,
          didDrawCell: (data) => {
            if (curGrid.docname === 'ventas_detalle') {
              if (curGrid.columnOption('FOTO', 'visible')) {
                if (data.column.index === 0 && data.cell.section === 'body') {
                  const rowKey = data.cell.raw.content
                  const imgsrc =
                    this.$config.fotosURL + rowKey + this.$config.fotosExt
                  const tPos = data.cell.getTextPos()
                  pdfDoc.addImage(imgsrc, 'JPEG', tPos.x, tPos.y, 22.5, 15)
                }
              }
            }
          },
        },
      }).then(() => {
        pdfDoc.save(curGrid.docname + '.pdf')
        this.busyWith = false
      })
    },

    doExportExcel(vv, ax, curGrid) {
      const PromiseArray = []
      const workbook = new ExcelJS.Workbook()
      const worksheet = workbook.addWorksheet(curGrid.docname)

      const masterRows = []

      this.busyWith = true

      exportDataGridToExcel({
        component: curGrid.component,
        worksheet,
        autoFilterEnabled: true,
        selectedRowsOnly: true,
        customizeCell: ({ excelCell, gridCell }) => {
          if (curGrid.docname === 'ventas_detalle') {
            if (gridCell.rowType === 'data') {
              if (gridCell.column.name === 'FOTO') {
                excelCell.value = undefined
                const imgfile = gridCell.value + this.$config.fotosExt
                PromiseArray.push(
                  new Promise((resolve, reject) => {
                    addImageExcel(
                      imgfile,
                      workbook,
                      worksheet,
                      excelCell,
                      ax,
                      resolve
                    )
                  })
                )
              }

              if (gridCell.column.dataField === 'TALLA' && vv.length > 0) {
                masterRows.push({
                  rowIndex: excelCell.fullAddress.row + 1,
                  data: gridCell.data,
                })
              }
            }
          }
        },
      })
        .then((cellRange) => {
          if (vv.length > 0) {
            const borderStyle = {
              style: 'thin',
              color: { argb: 'FF7E7E7E' },
            }
            let offset = 0

            const insertRow = (index, offset, outlineLevel) => {
              const currentIndex = index + offset
              const row = worksheet.insertRow(currentIndex, [], 'n')

              for (let j = worksheet.rowCount + 1; j > currentIndex; j--) {
                worksheet.getRow(j).outlineLevel = worksheet.getRow(
                  j - 1
                ).outlineLevel
              }

              row.outlineLevel = outlineLevel

              return row
            }

            for (let i = 0; i < masterRows.length; i++) {
              const columnIndex =
                curGrid.component.columnOption('TALLA', 'visibleIndex') - 1
              const prodSKU = masterRows[i].data.SKU

              const columns = ['TALLA', 'BARCODE']

              const row = insertRow(masterRows[i].rowIndex + i, offset++, 2)
              columns.forEach((columnName, currentColumnIndex) => {
                Object.assign(row.getCell(columnIndex + currentColumnIndex), {
                  value: columnName,
                  fill: {
                    type: 'pattern',
                    pattern: 'solid',
                    fgColor: { argb: 'BEDFE6' },
                  },
                  font: { bold: true },
                  border: {
                    bottom: borderStyle,
                    left: borderStyle,
                    right: borderStyle,
                    top: borderStyle,
                  },
                })
              })

              vv.filter((v) => v.SKU === prodSKU).forEach((variant, index) => {
                const row = insertRow(masterRows[i].rowIndex + i, offset++, 2)

                columns.forEach((columnName, currentColumnIndex) => {
                  Object.assign(row.getCell(columnIndex + currentColumnIndex), {
                    value: variant[columnName],
                    fill: {
                      type: 'pattern',
                      pattern: 'solid',
                      fgColor: { argb: 'EAFFFF' },
                    },
                    border: {
                      bottom: borderStyle,
                      left: borderStyle,
                      right: borderStyle,
                      top: borderStyle,
                    },
                  })
                })
              })
              offset--
            }
          }
        })
        .then(() => {
          Promise.all(PromiseArray).then(() => {
            workbook.xlsx.writeBuffer().then((buffer) => {
              saveAs(
                new Blob([buffer], { type: 'application/octet-stream' }),
                curGrid.docname + '.xlsx'
              )
              this.busyWith = false
            })
          })
        })
    },
  },
  head() {
    return {
      title: 'Docs Ventas',
    }
  },
}
</script>
