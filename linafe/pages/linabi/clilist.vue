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
          <v-toolbar-title>Lista de Clientes</v-toolbar-title>
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
              panel-title="Panel Buscar"
              @set-conf-filtros="setConf.filtros = !setConf.filtros"
              @set-conf-agrupar="setConf.agrupar = !setConf.agrupar"
              @clear-all-filters="clearFilters"
              @menu-conf-close="menuConf = false"
              @snkb="snackbar = true"
            />
          </v-menu>
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
                <v-list-item-title @click.stop="refreshData">
                  Descargar Datos
                </v-list-item-title>
              </v-list-item>
              <v-list-item link>
                <v-list-item-icon>
                  <v-icon>mdi-table-remove</v-icon>
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
                <v-list-item link>
                  <v-list-item-content>
                    <v-list-item-title @click.stop="exportGrid(2)">
                      PDF
                    </v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list-group>
              <v-list-group prepend-icon="mdi-close-outline" no-action>
                <template v-slot:activator>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title>Remover</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </template>
                <v-list-item link>
                  <v-list-item-content>
                    <v-list-item-title @click.stop="clearFilters('header')">
                      Filtros de encabezados
                    </v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item link>
                  <v-list-item-content>
                    <v-list-item-title @click.stop="clearFilters('row')">
                      Filtros avanzados
                    </v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item link>
                  <v-list-item-content>
                    <v-list-item-title @click.stop="clearFilters()">
                      Todos los filtros
                    </v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item link>
                  <v-list-item-content>
                    <v-list-item-title @click.stop="clearSorting">
                      Ordenamiento
                    </v-list-item-title>
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
                    <v-list-item-title>Panel Buscar</v-list-item-title>
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
          :data-source="dataSource"
          :remote-operations="false"
          :allow-column-reordering="true"
          :row-alternation-enabled="true"
          :show-borders="true"
          :focused-row-enabled="true"
          :column-auto-width="true"
          :allow-column-resizing="true"
          column-resizing-mode="widget"
          :show-column-lines="true"
          :show-row-lines="false"
          :hover-state-enabled="true"
          :height="tableHeight"
        >
          <DxColumn data-field="NUMCLI" data-type="string" />
          <DxColumn data-field="NOMCLI" data-type="string" caption="NOMBRE" />
          <DxColumn data-field="EMAIL" data-type="string" />
          <DxColumn data-field="PAIS" data-type="string" />
          <DxColumn data-field="DIRECCION" data-type="string" />
          <DxColumn data-field="TEL1" data-type="string" />
          <DxColumn data-field="TEL2" data-type="string" />
          <DxColumn data-field="TEL3" data-type="string" />
          <DxColumn data-field="TIPO" data-type="string" />
          <DxColumn data-field="VENDEDOR" data-type="string" />
          <DxSelection
            select-all-mode="allPages"
            show-check-boxes-mode="always"
            mode="multiple"
          />
          <DxSearchPanel
            :visible="setConf.agrupar"
            :highlight-case-sensitive="true"
          />
          <DxColumnChooser
            mode="select"
            :allow-search="true"
            :height="360"
            title="Columnas"
          />
          <DxFilterRow :visible="setConf.filtros" />
          <DxHeaderFilter :visible="true" />
          <DxSummary>
            <DxTotalItem
              column="NUMCLI"
              summary-type="count"
              display-format="{0} Regs."
            />
          </DxSummary>
          <DxLoadPanel :enable="true" />
          <DxPager
            :allowed-page-sizes="[5, 10, 20]"
            :show-page-size-selector="true"
          />
          <DxPaging :page-size="psize" />
        </DxDataGrid>
      </div>
    </MaterialCard>
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
import { mapGetters } from 'vuex'
import { locale } from 'devextreme/localization'
import {
  DxDataGrid,
  DxColumn,
  DxSummary,
  DxTotalItem,
  DxSearchPanel,
  DxColumnChooser,
  DxFilterRow,
  DxHeaderFilter,
  DxPager,
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
import DataSource from 'devextreme/data/data_source'
import MaterialCard from '~/components/core/MaterialCard'
import TableSettings from '~/components/utilities/TableSettings'
import LoadingView from '~/components/utilities/LoadingView'

const curGridRefKey = 'cur-grid'

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

function uniqByKeepLast(data, key) {
  return [...new Map(data.map((x) => [key(x), x])).values()]
}

export default {
  name: 'SKUSales',
  components: {
    DxDataGrid,
    DxColumn,
    DxSummary,
    DxTotalItem,
    DxSearchPanel,
    DxColumnChooser,
    DxFilterRow,
    DxHeaderFilter,
    DxPager,
    DxPaging,
    DxLoadPanel,
    DxSelection,
    MaterialCard,
    TableSettings,
    LoadingView,
  },
  async fetch() {
    const curparams = {
      p01: 'CLIFULL',
      p02: this.getCurCia.extrel,
    }

    // this.loadingView = true
    await this.$axios
      .get('linabi/clists', {
        params: curparams,
      })
      .then((response) => {
        this.dataSource = new DataSource({
          store: {
            type: 'array',
            key: 'ID',
            data: response.data,
          },
        })

        // this.loadingView = false
      })
  },
  async asyncData({ $axios, store, error }) {
    const loggedInUser = store.getters.loggedInUser
    const groupList = loggedInUser.ugroups.toString()
    try {
      const [resp0, resp1] = await Promise.all([
        $axios.get('vistas/18/'),
        $axios.get('accviewconf-list/', {
          params: { idvista: '18', groups: groupList },
        }),
      ])
      const filterPerms = uniqByKeepLast(resp1.data, (it) => it.vistaconf)
      return {
        curView: {
          num: resp0.data.id,
          checkelperms: resp0.data.checkelperms,
        },
        config: resp0.data.configs_x_vista,
        filterPerms,
      }
    } catch (err) {
      if (err.response) {
        error({
          statusCode: err.response.status,
          message: err.response.data.message,
        })
      } else if (error.request) {
        error({
          statusCode: 503,
          message: 'No hubo respuesta del servidor',
        })
      } else {
        error({
          statusCode: 1010,
          message: err.message,
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
      },
      colsConfig: [],
      menuFilter: false,
      radioGroup: '1',
      tableHeight: 0,
      snackbar: false,
      busyWith: false,
      loadingMessage: 'Exportando...',
      noImgList: [],
      psize: 20,
    }
  },
  computed: {
    ...mapGetters('sistema', ['getCurCia']),
    curGrid() {
      return this.$refs[curGridRefKey].instance
    },
  },
  created() {
    locale(navigator.language)
  },
  mounted() {
    this.colsConfig = this.config.filter((e) => e.tipo === 'col')
    this.setConf.filtros = false
    this.setConf.agrupar = true
  },
  activated() {},
  methods: {
    goBack() {
      this.$router.back()
    },
    clearData() {
      this.dataSource = null
      this.menuFilter = false
    },
    clearFilters(opc = 'all') {
      if (opc !== 'all') {
        this.curGrid.clearFilter(opc)
      } else {
        this.curGrid.clearFilter()
      }
      this.menuConf = false
      this.menuFilter = false
    },
    clearSorting() {
      this.curGrid.clearSorting()
      this.menuFilter = false
    },
    showColumnChooser() {
      this.curGrid.showColumnChooser()
      this.menuConf = false
    },
    refreshData() {
      this.menuFilter = false
      this.$fetch()
    },
    onResize() {
      this.tableHeight =
        window.innerHeight -
        this.$refs.resizableDiv.getBoundingClientRect().y -
        100
    },
    exportGrid(opc) {
      this.menuFilter = false

      const selectedRows = this.curGrid.getSelectedRowKeys()

      if (selectedRows.length > 0) {
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
      }
    },
    doExportPDF() {
      this.busyWith = true
      const pdfDoc = new JsPDF({
        orientation: 'landscape',
        format: 'letter',
      })

      let mch = { minCellHeight: 5 }
      if (this.curGrid.columnOption('FOTO', 'visible')) {
        mch = { minCellHeight: 20 }
      }

      // Foto column index
      const fci = this.curGrid.getVisibleColumnIndex('FOTO') - 2

      exportDataGridToPdf({
        component: this.curGrid,
        jsPDFDocument: pdfDoc,
        selectedRowsOnly: true,

        autoTableOptions: {
          bodyStyles: mch,
          didDrawCell: (data) => {
            if (fci >= 0) {
              if (data.column.index === fci && data.cell.section === 'body') {
                const rowImg = data.cell.raw.content
                if (rowImg) {
                  if (!this.noImgList.includes(rowImg)) {
                    const imgsrc = this.$config.fotosURL + rowImg
                    const tPos = data.cell.getTextPos()
                    pdfDoc.addImage(imgsrc, 'JPEG', tPos.x, tPos.y, 22.5, 15)
                  }
                }
              }
            }
          },
        },
      }).then(() => {
        pdfDoc.save('detalle_de_ventas.pdf')
        this.busyWith = false
      })
    },
    doExportExcel(ax) {
      const PromiseArray = []
      const workbook = new ExcelJS.Workbook()
      const worksheet = workbook.addWorksheet('ventas_det')

      this.busyWith = true

      exportDataGridToExcel({
        component: this.curGrid,
        worksheet,
        autoFilterEnabled: true,
        selectedRowsOnly: true,
        customizeCell: ({ excelCell, gridCell }) => {
          if (gridCell.rowType === 'data') {
            if (gridCell.column.name === 'FOTO') {
              excelCell.value = undefined
              const imgfile = gridCell.value
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
            this.busyWith = false
          })
        })
      })
    },
  },
  head() {
    return {
      title: 'Ventas por SKU',
    }
  },
}
</script>
