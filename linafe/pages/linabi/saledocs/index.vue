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
                    v-show="tab == 0"
                    v-model="showPanels0"
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
                  <v-list-item-group
                    v-show="tab == 1"
                    v-model="showPanels1"
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
            <v-toolbar-title>Documentos de Ventas</v-toolbar-title>
            <v-spacer />
            <v-btn dark icon @click="showColumnChooser">
              <v-icon>mdi-table-column-plus-after</v-icon>
            </v-btn>
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
                  class="ma-4"
                  :focused-row-enabled="true"
                  :data-source="dataSource0"
                  :remote-operations="false"
                  :column-auto-width="true"
                  :allow-column-reordering="true"
                  :row-alternation-enabled="true"
                  :show-borders="true"
                  :height="tableHeight"
                >
                  <DxColumn
                    v-for="xcol in colsConfig0"
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
                  <DxGroupPanel
                    :visible="showPanels0.includes(0)"
                    empty-panel-text="Arrastre aquí el encabezado de una columna para agrupar"
                  />
                  <DxSearchPanel
                    :visible="showPanels0.includes(0)"
                    :highlight-case-sensitive="true"
                  />
                  <DxColumnChooser
                    mode="select"
                    :allow-search="true"
                    :height="360"
                    title="Ver Columna"
                  />
                  <DxGrouping :auto-expand-all="false" />
                  <DxFilterRow :visible="showPanels0.includes(1)" />
                  <DxHeaderFilter :visible="true" />
                  <DxScrolling mode="virtual" />
                  <DxPaging :page-size="100" />
                </DxDataGrid>
              </v-tab-item>
              <v-tab-item key="tab1">
                <DxDataGrid
                  :ref="curGridRefKey1"
                  class="ma-4"
                  :focused-row-enabled="true"
                  :data-source="dataSource1"
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
                    v-for="xcol in colsConfig1"
                    :key="xcol.id"
                    :allow-grouping="xcol.configval7 == '1'"
                    :data-field="xcol.configkey"
                    :visible="xcol.configval2 == '1'"
                    :caption="xcol.configval3"
                    :data-type="xcol.configval4"
                    :format="xcol.configval5"
                    :alignment="xcol.configval6"
                  />
                  <DxGrouping :auto-expand-all="false" />
                  <DxGroupPanel
                    :visible="showPanels1.includes(0)"
                    empty-panel-text="Arrastre aquí el encabezado de una columna para agrupar"
                  />
                  <DxSearchPanel
                    :visible="showPanels1.includes(0)"
                    :highlight-case-sensitive="true"
                  />
                  <DxColumnChooser
                    ref="chooser1"
                    mode="select"
                    :allow-search="true"
                    :height="360"
                    title="Ver Columna"
                  />
                  <DxFilterRow :visible="showPanels1.includes(1)" />
                  <DxHeaderFilter :visible="true" />
                  <DxScrolling mode="virtual" />
                  <DxPaging :page-size="100" />
                  <DxSelection
                    select-all-mode="allPages"
                    show-check-boxes-mode="always"
                    mode="multiple"
                  />
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
  </div>
</template>
<script>
import { mapState, mapActions, mapGetters } from 'vuex'
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
import saveAs from 'file-saver'
import { jsPDF as JsPDF } from 'jspdf'
import 'jspdf-autotable'
import ExcelJS from 'exceljs'
import { exportDataGrid as exportDataGridToPdf } from 'devextreme/pdf_exporter'
import { exportDataGrid as exportDataGridToExcel } from 'devextreme/excel_exporter'
import MaterialCard from '~/components/core/MaterialCard'
import BaseFilters from '~/components/linabi/BaseFilters'

const curGridRefKey0 = 'cur-grid1'
const curGridRefKey1 = 'cur-grid2'
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
  // url = process.env.PUBLIC_URL + url
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
    .catch((err) => {
      if (err.response.status === 404) {
        worksheet.getRow(excelCell.row).height = 100
        resolve()
      }
    })
}

export default {
  name: 'SaleDocs',
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
      showPanels0: [],
      showPanels1: [],
      colsConfig0: [],
      colsConfig1: [],
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
    ...mapGetters('linabi/saledocsm', ['getFilters']),
    curGrid0() {
      return this.$refs[curGridRefKey0].instance
    },
    curGrid1() {
      return this.$refs[curGridRefKey1].instance
    },
  },
  created() {},
  mounted() {
    this.colsConfig0 = this.config0.filter((e) => e.tipo === 'col')
    this.colsConfig1 = this.config1.filter((e) => e.tipo === 'col')
  },
  methods: {
    ...mapActions('linabi/saledocsm/', [
      'setFilters',
      'setTotalCount',
      'fetchData',
    ]),
    ...mapActions({
      setFiltersDetails: 'linabi/saledocsd/setFilters',
      fetchDataDetails: 'linabi/saledocsd/fetchData',
    }),
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
        const tipodoc = this.getFilters.p15

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
    },
    exportGrid(opc) {
      let curComponent
      let curNameDoc

      const PromiseArray = []

      const ax = this.$axios.create({
        baseURL: process.env.FOTOS_URL,
        headers: {
          common: {
            Accept: 'text/plain, */*',
          },
        },
      })

      if (this.tab === 0) {
        curComponent = this.curGrid0
        curNameDoc = 'Ventas'
      } else {
        curComponent = this.curGrid1
        curNameDoc = 'Ventas_Detalle'
      }

      if (opc === 1) {
        const selectedRows = this.curGrid0.getSelectedRowKeys()

        selectedRows.forEach((rowKey) => {
          const imgfile = rowKey + process.env.FOTOS_EXT
          getImageForPDF(imgfile, ax).then((b64Img) => {
            const objKey = 'key' + rowKey
            // fotos.push({ sku: objKey, img: b64Img })
            fotos[objKey] = b64Img
          })
        })

        const pdfDoc = new JsPDF({
          orientation: 'landscape',
          format: 'letter',
        })

        const options = {
          component: curComponent,
          jsPDFDocument: pdfDoc,
          selectedRowsOnly: true,
          customizeCell: ({ pdfCell, gridCell }) => {
            if (gridCell.column.name === 'FOTO') {
              if (gridCell.rowType === 'data') {
                const rowKey = gridCell.value
                const objKey = 'key' + rowKey

                // console.log('VALOR DE fotos en options:')
                // console.log(fotos)
                // const imgitem = fotos.find((obj) => obj.sku === objKey).value
                // const b64Img = imgitem.img
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
          pdfDoc.save(`${curNameDoc}.pdf`)
        })
      }

      if (opc === 2) {
        const workbook = new ExcelJS.Workbook()
        const worksheet = workbook.addWorksheet(curNameDoc)

        exportDataGridToExcel({
          component: curComponent,
          worksheet,
          autoFilterEnabled: true,
          selectedRowsOnly: true,
          customizeCell: ({ excelCell, gridCell }) => {
            if (gridCell.rowType === 'data') {
              if (gridCell.column.name === 'FOTO') {
                excelCell.value = undefined
                const imgfile = gridCell.value + process.env.FOTOS_EXT
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
                `${curNameDoc}.xlsx`
              )
            })
          })
        })
      }
    },
  },
  head() {
    return {
      title: 'Docs Ventas',
    }
  },
}
</script>
