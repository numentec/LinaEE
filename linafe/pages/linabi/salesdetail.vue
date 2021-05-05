/* eslint-disable no-console */
<template>
  <div>
    <div>
      <v-breadcrumbs :items="breadCrumbsItems"></v-breadcrumbs>
    </div>
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
                      <v-list-item-title @click.stop="exportGrid(2)">
                        Excel
                      </v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item link>
                    <v-list-item-content>
                      <v-list-item-title @click.stop="exportGrid(1)">
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
                  <v-list-item>
                    <v-list-item-action>
                      <v-switch v-model="setConf.agrupar"></v-switch>
                    </v-list-item-action>
                    <v-list-item-content>
                      <v-list-item-title>Panel Agrupar</v-list-item-title>
                      <v-list-item-subtitle>
                        Agrupar y búsqueda global
                      </v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item>
                    <v-list-item-action>
                      <v-switch v-model="setConf.filtros"></v-switch>
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
            <v-toolbar-title>Detalle de Documentos de Ventas</v-toolbar-title>
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
                :show-column-chooser="showColumnChooser"
                :set-filtros="setConf.filtros"
                :set-agrupar="setConf.agrupar"
                @set-conf-filtros="setConf.filtros = !setConf.filtros"
                @set-conf-agrupar="setConf.agrupar = !setConf.agrupar"
                @menu-conf-close="menuConf = false"
                @snkb="snackbar = true"
              />
            </v-menu>
          </v-toolbar>
        </template>
        <div ref="resizableDiv" v-resize="onResize">
          <DxDataGrid
            :ref="curGridRefKey"
            class="ma-4"
            :focused-row-enabled="true"
            :data-source="dataSource"
            :remote-operations="false"
            :column-auto-width="true"
            :allow-column-reordering="true"
            :row-alternation-enabled="true"
            :show-borders="true"
            :height="tableHeight"
          >
            <DxColumn
              width="200"
              :allow-grouping="false"
              data-field="SKU"
              name="FOTO"
              caption="Foto"
              cell-template="imgCellTemplate"
              :allow-header-filtering="false"
            />
            <DxColumn
              v-for="xcol in colsConfig"
              :key="xcol.id"
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
              :visible="setConf.agrupar"
              empty-panel-text="Arrastre aquí el encabezado de una columna para agrupar"
            />
            <DxSearchPanel
              :visible="setConf.agrupar"
              :highlight-case-sensitive="true"
            />
            <DxColumnChooser
              mode="select"
              :allow-search="true"
              :height="360"
              title="Ver Columna"
            />
            <DxFilterRow :visible="setConf.filtros" />
            <DxHeaderFilter :visible="true" />
            <DxScrolling mode="virtual" />
            <DxPaging :page-size="100" />
            <DxSelection
              select-all-mode="allPages"
              show-check-boxes-mode="always"
              mode="multiple"
            />
            <DxSummary>
              <template v-for="gcol in colsWithSummary">
                <DxGroupItem
                  :key="'gi' + gcol.id"
                  :column="gcol.configkey"
                  :align-by-column="true"
                  :summary-type="gcol.configval8"
                  :value-format="setFormat(gcol.configval5)"
                  :display-format="setDFormat('gi', gcol.configval8)"
                />
                <DxTotalItem
                  :key="'ti' + gcol.id"
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
        </div>
      </MaterialCard>
      <BaseFilters
        :dialog.sync="showBaseFilters"
        :config="config.filter((el) => el.tipo == 'filter')"
        :numvista="18"
        curstore="linabi/salesdetail"
        @closeDialog="closeDialog"
      />
    </div>
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
import { locale } from 'devextreme/localization'
import {
  DxDataGrid,
  DxColumn,
  DxSummary,
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

const curGridRefKey = 'cur-grid'
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

// Default Breadcrumb item
const defaultBCItem = [
  {
    text: 'DETALLE DE VENTAS',
    exact: true,
    append: true,
    replace: true,
    to: '/linabi/saledocs/details',
    nuxt: true,
  },
]

export default {
  name: 'SalesDetail',
  components: {
    DxDataGrid,
    DxColumn,
    DxSummary,
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
  },
  async asyncData({ $axios, error }) {
    try {
      const { data } = await $axios.get('vistas/18/')
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
      menuConf: false,
      setConf: {
        filtros: false,
        agrupar: false,
        totGrupo: false,
        totGlobal: false,
      },
      colsConfig: [],
      menuFilter: false,
      radioGroup: '1',
      showBaseFilters: false,
      tableHeight: 0,
      snackbar: false,
      onContentReady(e) {
        if (!collapsed) {
          e.component.expandRow(1)
          collapsed = true
        }
      },
      localBCItems: defaultBCItem,
    }
  },
  computed: {
    ...mapState('linabi/favoritos', ['breadCrumbsItems']),
    curGrid() {
      return this.$refs[curGridRefKey].instance
    },
  },
  created() {
    locale(navigator.language)
  },
  mounted() {
    this.colsConfig = this.config.filter((e) => e.tipo === 'col')
  },
  activated() {},
  methods: {
    ...mapActions('linabi/salesdetail', ['fetchData']),
    goBack() {
      this.$router.back()
    },
    clearData() {
      this.dataSource = null
      this.menuFilter = false
    },
    showColumnChooser() {
      this.curGrid.showColumnChooser()
      this.menuConf = false
    },
    closeDialog(refresh) {
      this.showBaseFilters = false
      if (refresh) {
        this.fetchData().then((store) => {
          this.dataSource = store
          // this.setTotalCount(store.length)
        })
      }
    },
    onResize() {
      this.tableHeight =
        window.innerHeight -
        this.$refs.resizableDiv.getBoundingClientRect().y -
        82
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
      // itype = Item type (GroupItem, TotalItem)
      // stype summary type (count, sum, etc.)
      const stypes = {
        sum: (itype) => (itype === 'gi' ? 'Sub Total: {0}' : 'Total: {0}'),
        count: (itype) => (itype === 'gi' ? 'Regs: {0}' : 'Total Regs: {0}'),
      }

      return stypes[stype]?.(itype) ?? ''
    },
    exportGrid(opc) {
      const ax = this.$axios.create({
        baseURL: this.$config.fotosURL,
        headers: {
          common: {
            Accept: 'image/*, application/json, text/plain, */*',
          },
        },
      })

      if (opc === 1) {
        this.doExportExcel(ax)
      }

      if (opc === 2) {
        this.doExportPDF()
      }
    },
    doExportPDF() {
      const pdfDoc = new JsPDF({
        orientation: 'landscape',
        format: 'letter',
      })

      let mch = { minCellHeight: 5 }
      if (this.curGrid.columnOption('FOTO', 'visible')) {
        mch = { minCellHeight: 20 }
      }

      exportDataGridToPdf({
        component: this.curGrid,
        jsPDFDocument: pdfDoc,
        selectedRowsOnly: true,

        autoTableOptions: {
          bodyStyles: mch,
          didDrawCell: (data) => {
            if (this.curGrid.columnOption('FOTO', 'visible')) {
              if (data.column.index === 0 && data.cell.section === 'body') {
                const rowKey = data.cell.raw.content
                const imgsrc =
                  this.$config.fotosURL + rowKey + this.$config.fotosExt
                const tPos = data.cell.getTextPos()
                pdfDoc.addImage(imgsrc, 'JPEG', tPos.x, tPos.y, 22.5, 15)
              }
            }
          },
        },
      }).then(() => {
        pdfDoc.save('detalle_de_ventas.pdf')
      })
    },
    doExportExcel(ax) {
      const PromiseArray = []
      const workbook = new ExcelJS.Workbook()
      const worksheet = workbook.addWorksheet('ventas_det')

      exportDataGridToExcel({
        component: this.curGrid,
        worksheet,
        autoFilterEnabled: true,
        selectedRowsOnly: true,
        customizeCell: ({ excelCell, gridCell }) => {
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
          }
        },
      }).then(() => {
        Promise.all(PromiseArray).then(() => {
          workbook.xlsx.writeBuffer().then((buffer) => {
            saveAs(
              new Blob([buffer], { type: 'application/octet-stream' }),
              'detalle_de_ventas.xlsx'
            )
          })
        })
      })
    },
  },
  head() {
    return {
      title: 'Detalle de Ventas',
    }
  },
}
</script>
