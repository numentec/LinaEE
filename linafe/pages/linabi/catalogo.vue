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
                  <!-- <v-list-item link>
                    <v-list-item-content>
                      <v-list-item-title>CSV</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item> -->
                  <v-list-item link>
                    <v-list-item-content>
                      <v-list-item-title @click.stop="exportGrid(3)">
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
                      <v-list-item-title @click.stop="showCatalogBuilder = true"
                        >Procesar</v-list-item-title
                      >
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item link>
                    <v-list-item-content>
                      <v-list-item-title @click.stop="addToCatalog"
                        >Agregar Selección</v-list-item-title
                      >
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item link>
                    <v-list-item-content>
                      <v-list-item-title @click.stop="downloadCatalog"
                        >Descargar</v-list-item-title
                      >
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
            <v-toolbar-title>Catálogo de Productos</v-toolbar-title>
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
                @set-conf-filtros="setConf.filtros = !setConf.filtros"
                @set-conf-agrupar="setConf.agrupar = !setConf.agrupar"
                @menu-conf-close="menuConf = false"
                @snkb="snackbar = true"
              />
            </v-menu>
          </v-toolbar>
        </template>
        <div id="tableDiv" ref="resizableDiv" v-resize="onResize">
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
            @content-ready="onContentReady"
          >
            <DxColumn
              width="200"
              :allow-grouping="false"
              data-field="REFERENCIA"
              name="FOTO"
              caption="Foto"
              cell-template="imgCellTemplate"
              :allow-header-filtering="false"
              :allow-reordering="false"
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
            <DxMasterDetail :enabled="true" template="mdTemplate" />
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
            <template #mdTemplate="{ data }">
              <ProdVariants
                :variant-data="data"
                :variant-title="'Códigos de Barra por Talla'"
              />
            </template>
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
        @closeDialog="closeBaseFilters"
      />
      <CatalogBuilder
        :dialog.sync="showCatalogBuilder"
        :numvista="14"
        curstore="linabi/catalogo"
        @downloadCatalog="downloadCatalog"
        @closeDialog="closeCatalogBuilder"
      />
      <LoadingView :busy-with="busyWith" :message="loadingMessage" />
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
import { mapState, mapActions, mapGetters } from 'vuex'
import { locale } from 'devextreme/localization'
import DataSource from 'devextreme/data/data_source'
import {
  DxDataGrid,
  DxColumn,
  DxMasterDetail,
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
import saveAs from 'file-saver'
import { jsPDF as JsPDF } from 'jspdf'
import 'jspdf-autotable'
import ExcelJS from 'exceljs'
import { exportDataGrid as exportDataGridToPdf } from 'devextreme/pdf_exporter'
import { exportDataGrid as exportDataGridToExcel } from 'devextreme/excel_exporter'
import MaterialCard from '~/components/core/MaterialCard'
import BaseFilters from '~/components/linabi/BaseFilters'
import CatalogBuilder from '~/components/linabi/CatalogBuilder'
import ProdVariants from '~/components/linabi/ProdVariants.vue'
import ImgForGrid from '~/components/utilities/ImgForGrid'
import TableSettings from '~/components/utilities/TableSettings'
import LoadingView from '~/components/utilities/LoadingView'

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

export default {
  name: 'Catalogo',
  components: {
    DxDataGrid,
    DxColumn,
    DxMasterDetail,
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
    MaterialCard,
    BaseFilters,
    CatalogBuilder,
    ImgForGrid,
    TableSettings,
    LoadingView,
    ProdVariants,
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
      curDetail: [],
      menuConf: false,
      snackbar: false,
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
      showCatalogBuilder: false,
      tableHeight: 0,
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
    ...mapState('linabi/catalogo', ['curStore']),
    ...mapGetters('linabi/catalogo', ['getCurCatalog']),
    curGrid() {
      return this.$refs[curGridRefKey].instance
    },
    colsWithSummary() {
      return this.colsConfig.filter((obj) => obj.configval8 !== '')
    },
    expDetail() {
      let result = false
      if (this.menuFilter) {
        if (this.$refs[curGridRefKey]) {
          const grd = this.$refs[curGridRefKey].instance
          result = grd.columnOption('TALLA', 'visible')
        }
      }
      return result
    },
  },
  // watch: {
  //   menuFilter(val) {
  //     if (val) {
  //       this.expDetail = this.curGrid.columnOption('TALLA', 'visible')
  //     }
  //   },
  // },
  created() {
    locale(navigator.language)
    // config({ defaultCurrency: 'USD' })
  },
  mounted() {
    this.colsConfig = this.viewConf.filter((e) => e.tipo === 'col')
  },
  methods: {
    ...mapActions('linabi/catalogo', ['fetchData', 'addToCurCatalog']),
    ...mapActions('linabi/common', ['fetchVariants']),
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
    closeBaseFilters(refresh) {
      this.showBaseFilters = false
      if (refresh) {
        this.fetchData().then((store) => {
          this.dataSource = store
        })
      }
    },
    closeCatalogBuilder() {
      this.showCatalogBuilder = false
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
        count: (itype) => (itype === 'gi' ? '{0} Regs. ' : '{0} Registros'),
      }

      return stypes[stype]?.(itype) ?? ''
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

        // Exportar a Excel
        if (opc === 1) {
          this.doExportExcel([], ax)
        }

        // Exportar a Excel con detalle de códigos de barra
        if (opc === 2) {
          this.fetchVariants({ sku: selectedRows }).then((vv) => {
            this.doExportExcel(vv, ax)
          })
        }

        // Exportar a PDF
        if (opc === 3) {
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

      exportDataGridToPdf({
        component: this.curGrid,
        jsPDFDocument: pdfDoc,
        selectedRowsOnly: true,
        // customizeCell: ({ pdfCell, gridCell }) => {
        //   if (gridCell.rowType === 'data') {
        //     if (gridCell.column.name === 'FOTO') {
        //       const rowKey = gridCell.value

        //       pdfCell.content = ''

        //       const imgsrc =
        //         this.$config.fotosURL + rowKey + this.$config.fotosExt

        //       pdfCell.customDrawCell = function (data) {
        //         const tPos = data.cell.getTextPos()
        //         pdfDoc.addImage(imgsrc, 'JPEG', tPos.x, tPos.y, 22.5, 15)
        //       }
        //     }
        //   }
        // },
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
        pdfDoc.save('Catalogo.pdf')
        this.busyWith = false
      })
    },

    doExportExcel(vv, ax) {
      const PromiseArray = []
      const workbook = new ExcelJS.Workbook()
      const worksheet = workbook.addWorksheet('Catalogo')

      const masterRows = []

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
              // const columnIndex = cellRange.from.column + 1
              const columnIndex =
                this.curGrid.columnOption('TALLA', 'visibleIndex') - 1

              // const prodData = this.curStore.find(
              //   (item) => item.SKU === masterRows[i].data.SKU
              // )
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

              getProdVariants(vv, prodSKU).forEach((variant, index) => {
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
                'Catalog.xlsx'
              )
              this.busyWith = false
            })
          })
        })
    },
    // testMethod() {
    //   this.busyWith = !this.busyWith
    // },
    addToCatalog() {
      const selected = this.curGrid.getSelectedRowsData()
      this.addToCurCatalog(selected)
      this.menuFilter = false
      this.showCatalogBuilder = true
    },
    downloadCatalog() {
      this.dataSource = new DataSource({
        store: {
          type: 'array',
          key: 'SKU',
          data: this.getCurCatalog,
        },
      })
      this.showCatalogBuilder = false
      this.menuFilter = false
    },
  },
  head() {
    return {
      title: 'Catálogo',
    }
  },
}

const getProdVariants = (variants, sku) => {
  return variants.filter((v) => v.SKU === sku)
}
</script>
