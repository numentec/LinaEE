/* eslint-disable no-console */
<template>
  <div>
    <div>
      <v-breadcrumbs :items="breadCrumbsItems"></v-breadcrumbs>
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
              <v-list nav>
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
                      <v-list-item-title>CSV</v-list-item-title>
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
                <v-list-group
                  prepend-icon="mdi-book-open-page-variant"
                  no-action
                >
                  <template v-slot:activator>
                    <v-list-item>
                      <v-list-item-content>
                        <v-list-item-title>Catálogo</v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                  </template>
                  <v-list-item link>
                    <v-list-item-content>
                      <v-list-item-title>Procesar</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item link>
                    <v-list-item-content>
                      <v-list-item-title>Agregar Selección</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item link>
                    <v-list-item-content>
                      <v-list-item-title>Descargar</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item link>
                    <v-list-item-content>
                      <v-list-item-title @click.stop="savePhotos"
                        >Guardar Fotos</v-list-item-title
                      >
                    </v-list-item-content>
                  </v-list-item>
                </v-list-group>
                <v-list-group prepend-icon="mdi-database-search" no-action>
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
                      <v-list-item-title>Ajustes</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list-group>
              </v-list>
            </v-menu>
            <v-spacer />
            <v-toolbar-title>Catálogo de Productos</v-toolbar-title>
            <v-spacer />
            <!-- <v-btn dark icon @click="testMethod()">
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
                @set-conf-filtros="setConf.filtros = !setConf.filtros"
                @set-conf-agrupar="setConf.agrupar = !setConf.agrupar"
                @menu-conf-close="menuConf = false"
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
              data-field="REFERENCIA"
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
            >
            </DxColumn>
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
              title="Columnas"
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
            <DxSummary :v-show="setConf.totGlobal">
              <DxTotalItem column="SKU" summary-type="count" />
              <DxTotalItem
                column="PRECIO"
                summary-type="sum"
                :value-format="setFormat('currency')"
              />
              <DxTotalItem
                column="PRECIOPUBLICO"
                summary-type="sum"
                :value-format="setFormat('currency')"
              />
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
        :config="viewConf.filter((el) => el.tipo == 'filter')"
        :numvista="14"
        curstore="linabi/catalogo"
        @closeDialog="closeDialog"
      />
    </div>
  </div>
</template>
<script>
import { mapState, mapActions } from 'vuex'
// import config from 'devextreme/core/config'
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
// const fotos = []
const fotos = {}

async function getImageForPDF(imgfile, ax) {
  return await ax
    .get(imgfile, {
      responseType: 'arraybuffer',
    })
    .then((response) => {
      return Buffer.from(response.data, 'binary').toString('base64')
    })
    .catch((err) => {
      if (err.response.status === 404) {
        return ''
      }
    })
}

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
  name: 'Catalogo',
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
      const { data } = await $axios.get('vistas/14/')
      return {
        viewConf: data.configs_x_vista,
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
      onContentReady(e) {
        if (!collapsed) {
          e.component.expandRow(1)
          collapsed = true
        }
      },
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
    // config({ defaultCurrency: 'USD' })
  },
  mounted() {
    this.colsConfig = this.viewConf.filter((e) => e.tipo === 'col')
  },
  methods: {
    ...mapActions('linabi/catalogo', ['fetchData']),
    savePhotos() {
      const selectedRows = this.curGrid.getSelectedRowKeys()

      selectedRows.forEach((rowKey) => {
        const imgfile = rowKey + this.$config.fotosExt
        const imgurl = this.$config.fotosURL + imgfile
        saveAs(imgurl, imgfile)
      })
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
    exportGrid(opc) {
      const PromiseArray = []

      const ax = this.$axios.create({
        baseURL: this.$config.fotosURL,
        headers: {
          common: {
            Accept: 'image/*, application/json, text/plain, */*',
          },
        },
      })

      if (opc === 1) {
        const selectedRows = this.curGrid.getSelectedRowKeys()
        // let i = 0

        selectedRows.forEach((rowKey) => {
          const imgfile = rowKey + this.$config.fotosExt
          getImageForPDF(imgfile, ax).then((b64Img) => {
            const objKey = 'key' + rowKey
            // const xf = [{ sku: objKey, img: b64Img }]
            // fotos.concat(xf)
            // fotos.push({ sku: objKey, img: b64Img })
            fotos[objKey] = b64Img
            // console.log('VALOR DE fotos en getImageForPDF:')
            // console.log(fotos)
          })
        })

        const pdfDoc = new JsPDF({
          orientation: 'landscape',
          format: 'letter',
        })

        const options = {
          component: this.curGrid,
          jsPDFDocument: pdfDoc,
          selectedRowsOnly: true,
          customizeCell: ({ pdfCell, gridCell }) => {
            if (gridCell.column.name === 'FOTO') {
              if (gridCell.rowType === 'data') {
                const rowKey = gridCell.value
                const objKey = 'key' + rowKey

                // console.log('VALOR DE fotos en options:')
                // console.log(fotos)
                // const { img } = fotos.find((obj) => obj.sku === objKey)
                // const b64Img = img
                const b64Img = fotos[objKey]
                // console.log('VALOR DE b64Img: ' + b64Img)

                pdfCell.content = ''
                pdfCell.customDrawCell = function (data) {
                  const tPos = data.cell.getTextPos()
                  pdfDoc.addImage(b64Img, 'JPEG', tPos.x, tPos.y, 22.5, 15)
                }
              }
            }
          },
          autoTableOptions: {
            bodyStyles: { minCellHeight: 20 },
          },
        }

        exportDataGridToPdf(options).then(() => {
          // console.log('CONTENIDO DE fotos:')
          // console.log(fotos)
          pdfDoc.save('Catalogo.pdf')
        })
      }

      if (opc === 2) {
        const workbook = new ExcelJS.Workbook()
        const worksheet = workbook.addWorksheet('Catalogo')

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
                'Catalog.xlsx'
              )
            })
          })
        })
      }
    },
  },
  head() {
    return {
      title: 'Catálogo',
    }
  },
}
</script>
