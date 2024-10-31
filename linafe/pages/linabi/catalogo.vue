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
            <v-list nav>
              <v-list-item link>
                <v-list-item-icon>
                  <v-icon>mdi-cloud-download</v-icon>
                </v-list-item-icon>
                <v-list-item-title
                  @click.stop="
                    showBaseFilters = true
                    menuFilter = false
                  "
                >
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
                <v-list-item v-show="isTallaVisible">
                  <v-list-item-action>
                    <v-switch
                      v-model="setvart"
                      @change="verifVar(1)"
                    ></v-switch>
                  </v-list-item-action>
                  <v-list-item-content>
                    <v-list-item-title>Tallas</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item v-show="isColorVisible">
                  <v-list-item-action>
                    <v-switch
                      v-model="setvarc"
                      @change="verifVar(2)"
                    ></v-switch>
                  </v-list-item-action>
                  <v-list-item-content>
                    <v-list-item-title>Colores</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item link>
                  <v-list-item-content>
                    <v-list-item-title @click.stop="exportGrid(1)">
                      Excel
                    </v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item link>
                  <v-list-item-content>
                    <v-list-item-title @click.stop="selTemplate">
                      Excel - Plantilla
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
              <v-list-group prepend-icon="mdi-book-open-page-variant" no-action>
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
                <v-list-item link>
                  <v-list-item-content>
                    <v-list-item-title @click.stop="clearGrouping">
                      Grupos
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
          :hover-state-enabled="true"
          @cell-click="manageCellClick"
          @context-menu-preparing="addMenuItems"
          @option-changed="handlePropertyChange"
        >
          <template v-for="xcol in colsConfig">
            <DxColumn
              v-if="xcol.configkey == 'FOTO'"
              id="FOTO"
              :key="xcol.id"
              width="200"
              :allow-grouping="false"
              data-field="FOTO"
              name="FOTO"
              caption="Foto"
              :visible="xcol.configval3 == '1'"
              cell-template="imgCellTemplate"
              css-class="cell-highlighted"
              :allow-sorting="false"
              :allow-header-filtering="false"
            />
            <DxColumn
              v-else-if="xcol.configkey == 'FICHA'"
              id="FICHA"
              :key="xcol.id"
              width="200"
              :allow-grouping="false"
              data-field="SKU"
              name="FICHA"
              caption="Ficha"
              :visible="xcol.configval3 == '1'"
              cell-template="fichaCellTemplate"
              :allow-sorting="false"
              :allow-header-filtering="false"
            />
            <DxColumn
              v-else
              :id="xcol.configkey"
              :key="xcol.id"
              :allow-grouping="xcol.configval7 == '1'"
              :data-field="xcol.configkey"
              :visible="xcol.configval3 == '1'"
              :caption="xcol.configval2"
              :data-type="xcol.configval4"
              :format="setFormat(xcol.configval5)"
              :alignment="xcol.configval6"
              :sorting-method="selFunction(xcol.configval9)"
            />
          </template>
          <DxSorting mode="multiple" />
          <DxMasterDetail :enabled="true" template="mdTemplate" />
          <DxGrouping :auto-expand-all="false" />
          <DxGroupPanel
            :visible="setConf.agrupar"
            empty-panel-text="Arrastre aquí el encabezado de una columna para agrupar"
          />
          <DxSearchPanel
            :visible="setConf.agrupar"
            :highlight-case-sensitive="true"
            placeholder="Buscar..."
          />
          <DxColumnChooser
            mode="select"
            :allow-search="true"
            :height="360"
            title="Columnas"
          />
          <DxFilterRow :visible="setConf.filtros" />
          <DxHeaderFilter :visible="true" :allow-search="true" />
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
            <v-row>
              <v-col>
                <ProdVariants
                  v-show="isTallaVisible"
                  :variant-data="data.data.SKU"
                  :cur-variant="var_talla"
                />
              </v-col>
              <v-col>
                <ProdVariants
                  v-show="isColorVisible"
                  :variant-data="data.data.SKU"
                  :cur-variant="var_color"
                />
              </v-col>
            </v-row>
          </template>
          <template #imgCellTemplate="{ data }">
            <ImgForGrid
              :img-file="$config.fotosURL + data.value"
              @no-image="storeNoImg(data.value)"
            />
          </template>
          <template #fichaCellTemplate="{ data }">
            <p style="font-size: 0.8rem">
              SKU: {{ data.data.SKU }}<br />
              Descrip: {{ data.data.DESCRIP }}<br />
              Marca: {{ data.data.MARCA }}<br />
              Tallas: {{ data.data.TALLA }}<br />
              Dist.: {{ data.data.DISTRIBUCION }}
            </p>
          </template>
        </DxDataGrid>
      </div>
    </MaterialCard>
    <BaseFilters
      :dialog.sync="showBaseFilters"
      :config="viewConf.filter((el) => el.tipo == 'filter')"
      :perms="filterPerms"
      :cur-view="curView"
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
    <TemplatesAdmin
      :dialog.sync="showSelTemplate"
      :numvista="14"
      @closeDialog="closeSelTemplate"
      @setTemplate="doExportTemplate"
    />
    <Slideshow
      :data-source="getCurStore"
      :cur-key="curRowKey"
      :show-slideshow="slideshow"
      :no-img-list="noImgList"
      @hideSlideshow="slideshow = false"
    />
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
  DxSorting,
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
import JSZip from 'jszip'
import { exportDataGrid as exportDataGridToPdf } from 'devextreme/pdf_exporter'
import { exportDataGrid as exportDataGridToExcel } from 'devextreme/excel_exporter'
import MaterialCard from '~/components/core/MaterialCard'
import BaseFilters from '~/components/linabi/BaseFilters'
import CatalogBuilder from '~/components/linabi/CatalogBuilder'
import ProdVariants from '~/components/linabi/ProdVariants.vue'
import TemplatesAdmin from '~/components/linabi/TemplatesAdmin.vue'
import Slideshow from '~/components/linabi/Slideshow'
import ImgForGrid from '~/components/utilities/ImgForGrid'
import TableSettings from '~/components/utilities/TableSettings'
import LoadingView from '~/components/utilities/LoadingView'
import { selFunction } from '~/assets/utilities'

const curGridRefKey = 'cur-grid'
let collapsed = false
let customTemplate = false

function fileDownloader(url, ax) {
  // url = this.$config.publicURL + url
  // ax.onResponse((response) => {
  //   if (response.status === 404) {
  //       console.log('Oh no it returned a 404')
  //   }
  // })
  return new Promise((resolve, reject) => {
    ax.get(url, {
      responseType: 'arraybuffer',
    })
      .then((response) => {
        resolve(response.data)
      })
      .catch(() => {
        // reject(err.toString())
        resolve()
      })
  })
}

function uniqByKeepLast(data, key) {
  return [...new Map(data.map((x) => [key(x), x])).values()]
}
// function curWorkSheet(wb, src) {
//   if (src === 'new') {
//     return wb.addWorksheet('Catalogo')
//   } else {
//     wb.xlsx.readFile(src).then((w) => {
//       return w
//     })
//   }
// }

const VARTALLA = {
  data_field: 'TALLA',
  endpoint: 'linabi/tallasbc',
  title: 'Códigos de Barra por Talla',
}

const VARCOLOR = {
  data_field: 'COLORES',
  endpoint: 'linabi/coloresbc',
  title: 'Códigos de Barra por Color',
}

const contextItems = [
  { text: 'Todos' },
  { text: 'Con foto' },
  { text: 'Sin foto' },
]

export default {
  name: 'Catalogo',
  components: {
    DxDataGrid,
    DxColumn,
    DxSorting,
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
    TemplatesAdmin,
    Slideshow,
  },
  async asyncData({ $axios, store, error }) {
    const loggedInUser = store.getters.loggedInUser
    const groupList = loggedInUser.ugroups.toString()
    try {
      const [resp0, resp1] = await Promise.all([
        $axios.get('vistas/14/'),
        $axios.get('accviewconf-list/', {
          params: { idvista: '14', groups: groupList },
        }),
      ])
      const filterPerms = uniqByKeepLast(resp1.data, (it) => it.vistaconf)
      return {
        curView: {
          num: resp0.data.id,
          checkelperms: resp0.data.checkelperms,
        },
        viewConf: resp0.data.configs_x_vista,
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
      selFunction,
      dataSource: null,
      setvart: false,
      setvarc: false,
      cur_variante: '',
      var_talla: VARTALLA,
      var_color: VARCOLOR,
      isTallaVisible: false,
      isColorVisible: false,
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
      showBaseFilters: false,
      showCatalogBuilder: false,
      showSelTemplate: false,
      tableHeight: 0,
      testfilename: '',
      onContentReady(e) {
        if (!collapsed) {
          e.component.expandRow(1)
          collapsed = true
        }
      },
      busyWith: false,
      loadingMessage: 'Exportando...',
      plantilla: {
        name: '',
        savingFilename: '',
        row: 1,
        col: 1,
      },
      slideshow: false,
      curRowKey: 0,
      curRowIndex: 0,
      noImgList: [],
      contextItems,
      curImgList: [],
      rowHeaderIndex: [2],
      imgax: this.$axios.create({
        baseURL: this.$config.fotosURL,
        headers: {
          common: {
            Accept: 'image/*, application/json, text/plain, */*',
          },
        },
      }),
      imgListForPDF: {},
    }
  },
  computed: {
    ...mapState('linabi/catalogo', ['curStore']),
    ...mapGetters('linabi/catalogo', ['getCurCatalog', 'getCurStore']),
    curGrid() {
      return this.$refs[curGridRefKey].instance
    },
    colsWithSummary() {
      return this.colsConfig.filter((obj) => obj.configval8 !== '')
    },
    noImgFilters() {
      return [
        {
          text: 'Con foto',
          value: ['FOTO', 'noneof', this.noImgList],
        },
        {
          text: 'Sin foto',
          value: ['FOTO', 'anyof', this.noImgList],
        },
      ]
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
    ...mapActions('linabi/catalogo', ['fetchData', 'addToCurCatalog']),
    ...mapActions('linabi/common', ['fetchVariants', 'setSlidecurkey']),
    savePhotos() {
      this.menuFilter = false

      const selectedRows = this.curGrid
        .getSelectedRowsData()
        .map((obj) => obj.FOTO)

      if (selectedRows.length === 1) {
        const imgfile = selectedRows[0]
        const imgurl = this.$config.fotosURL + imgfile
        saveAs(imgurl, imgfile)
      } else if (selectedRows.length > 1) {
        const zipobj = new JSZip()
        const zipFilename = 'photos.zip'
        const promises = []

        const ax = this.$axios.create({
          baseURL: this.$config.fotosURL,
          headers: {
            common: {
              Accept: 'image/*, application/json, text/plain, */*',
            },
          },
        })

        selectedRows.forEach((rowKey) => {
          const imgfile = rowKey
          const imgurl = this.$config.fotosURL + imgfile

          if (!this.noImgList.includes(rowKey)) {
            const promise = fileDownloader(imgurl, ax).then((data) => {
              if (data) {
                zipobj.file(imgfile, data, { binary: true })
              }
            })

            promises.push(promise)
          }
        })

        if (promises.length === 0) return

        Promise.all(promises).then(() => {
          zipobj.generateAsync({ type: 'blob' }).then((content) => {
            saveAs(content, zipFilename)
          })
        })
      }
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
    clearGrouping() {
      this.curGrid.clearGrouping()
      this.menuFilter = false
    },
    showColumnChooser() {
      this.curGrid.showColumnChooser()
      this.menuConf = false
    },
    closeBaseFilters(refresh) {
      this.showBaseFilters = false
      if (refresh) {
        this.noImgList = []
        this.fetchData().then((store) => {
          this.dataSource = store
        })
      }
    },
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
          key: 'ID',
          data: this.getCurCatalog,
        },
      })
      this.showCatalogBuilder = false
      this.menuFilter = false
    },
    closeCatalogBuilder() {
      this.showCatalogBuilder = false
    },
    selTemplate() {
      this.showSelTemplate = true
      this.menuFilter = false
    },
    doExportTemplate(e) {
      this.plantilla.name = e.name.toLowerCase() + '.xlsx'
      this.plantilla.row = e.inirow
      this.plantilla.col = e.inicol
      this.plantilla.savingFilename = e.name + '.xlsx'

      this.curGrid.beginCustomLoading('Cargando plantilla')

      setTimeout(() => {
        // Current visible columns
        const vc = this.curGrid
          .getVisibleColumns()
          .filter((obj) => obj.showInColumnChooser)

        // Columns to hide
        const cth = vc.filter((el) => {
          return !e.cols.find((element) => {
            return element.name === el.name
          })
        })

        // Show and order template's columns
        e.cols.forEach((col) => {
          this.curGrid.columnOption(col.name, {
            visible: true,
            visibleIndex: col.ordinal,
          })
        })

        // Hide extra columns
        cth.forEach((col) => {
          this.curGrid.columnOption(col.name, { visible: false })
        })
      }, 500)

      setTimeout(() => {
        this.curGrid.endCustomLoading()
        this.exportGrid(2)
      }, 500)
    },
    closeSelTemplate() {
      this.showSelTemplate = false
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

      // const selectedRows = this.curGrid.getSelectedRowKeys()
      const selectedRows = this.curGrid
        .getSelectedRowsData()
        .map((obj) => obj.SKU)

      if (selectedRows.length > 0) {
        // Exportar a Excel
        if (opc === 1) {
          const savingFilename = 'Catalog.xlsx'
          const workbook = new ExcelJS.Workbook()
          const tLC = { row: 1, column: 1 }
          const worksheet = workbook.addWorksheet(savingFilename)
          if (this.cur_variante !== '') {
            // Exportar a Excel con detalle de códigos de barra
            const cv = this.cur_variante
            this.fetchVariants({ sku: selectedRows, cv }).then((vv) => {
              this.doExportExcel(workbook, worksheet, savingFilename, tLC, vv)
            })
          } else {
            this.doExportExcel(workbook, worksheet, savingFilename, tLC, [])
          }
        }

        // Exportar a PDF
        if (opc === 3) {
          // If column FOTO is visible, then all photos are downloaded before build the PDF
          if (this.curGrid.columnOption('FOTO', 'visible')) {
            const PromiseArray = []
            const imgList = this.curGrid
              .getSelectedRowsData()
              .map((obj) => obj.FOTO)

            this.busyWith = true

            imgList.forEach((imgfile) => {
              PromiseArray.push(
                new Promise((resolve, reject) => {
                  this.addImgForPDF(imgfile, resolve)
                })
              )
            })

            Promise.all(PromiseArray).then(() => {
              this.doExportPDF()
            })
          } else {
            this.doExportPDF()
          }
        }

        // Exportar a Excel usando plantilla
        if (opc === 2) {
          customTemplate = true
          const template = 'plantillas/' + this.plantilla.name
          const axx = this.$axios.create({
            baseURL: this.$config.mediaURL,
          })
          axx
            .get(template, {
              responseType: 'arraybuffer',
            })
            .then((response) => {
              const workbook = new ExcelJS.Workbook()
              const buffer = response.data

              workbook.xlsx.load(buffer).then((workbook) => {
                const worksheet = workbook.worksheets[0]

                const savingFilename = this.plantilla.savingFilename
                const topLeftCell = {
                  row: this.plantilla.row,
                  column: this.plantilla.col,
                }

                if (this.cur_variante !== '') {
                  // Exportar a Excel con detalle de códigos de barra
                  const cv = this.cur_variante
                  this.fetchVariants({ sku: selectedRows, cv }).then((vv) => {
                    this.doExportExcel(
                      workbook,
                      worksheet,
                      savingFilename,
                      topLeftCell,
                      [vv]
                    )
                  })
                } else {
                  this.doExportExcel(
                    workbook,
                    worksheet,
                    savingFilename,
                    topLeftCell,
                    []
                  )
                }
              })
            })
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
        customizeCell: ({ pdfCell, gridCell }) => {
          if (gridCell.rowType === 'data') {
            if (gridCell.column.name === 'FICHA') {
              if (gridCell.value) {
                pdfCell.content =
                  'SKU: ' +
                  gridCell.data.SKU +
                  '\n' +
                  gridCell.data.DESCRIP +
                  '\n' +
                  'Marca: ' +
                  gridCell.data.MARCA +
                  '\n' +
                  'Talla: ' +
                  gridCell.data.TALLA +
                  '\n' +
                  'Dist.: ' +
                  gridCell.data.DISTRIBUCION
                // pdfCell.alignment = { horizontal: 'justify', vertical: 'top' }
              }
            }
          }
        },
        autoTableOptions: {
          bodyStyles: mch,
          willDrawCell: (data) => {
            if (fci >= 0) {
              if (data.column.index === fci && data.cell.section === 'body') {
                data.doc.setTextColor(255)
              }
            }
          },
          didDrawCell: (data) => {
            if (fci >= 0) {
              if (data.column.index === fci && data.cell.section === 'body') {
                const rowImg = data.cell.raw.content
                if (rowImg) {
                  if (this.imgListForPDF[rowImg]) {
                    const imgfile = this.imgListForPDF[rowImg]
                    const tPos = data.cell.getTextPos()
                    pdfDoc.addImage(imgfile, 'JPEG', tPos.x, tPos.y, 23.0, 15.0)
                  }
                }
              }
            }
          },
        },
      }).then(() => {
        pdfDoc.save('Catalogo.pdf')
        this.busyWith = false
      })
    },

    doExportExcel(
      workbook,
      worksheet,
      savingFilename,
      topLeftCell = { row: 1, column: 1 },
      vv = []
    ) {
      const PromiseArray = []
      const masterRows = []

      this.busyWith = true

      exportDataGridToExcel({
        component: this.curGrid,
        worksheet,
        topLeftCell,
        autoFilterEnabled: !customTemplate,
        selectedRowsOnly: true,
        customizeCell: ({ excelCell, gridCell }) => {
          if (gridCell.rowType === 'data') {
            if (gridCell.column.name === 'FOTO') {
              excelCell.value = undefined
              if (gridCell.value) {
                const imgfile = gridCell.value

                PromiseArray.push(
                  new Promise((resolve, reject) => {
                    this.addImageExcel(
                      imgfile,
                      workbook,
                      worksheet,
                      excelCell,
                      topLeftCell.row,
                      resolve
                    )
                  })
                )
              }

              // if (gridCell.value) {
              //   console.log('FULL GRIDCELL', gridCell)
              //   console.log('FULL EXCEL CELL', excelCell)
              //   console.log('EXCEL FULL ADDRESS ROW', excelCell.fullAddress.row)
              //   const b64img = this.curImgList.find(
              //     (el) => el.sku === gridCell.value
              //   )

              //   const image = workbook.addImage({
              //     base64: b64img.img,
              //     extension: 'JPEG',
              //   })

              //   worksheet.getRow(excelCell.row).height = 100
              //   worksheet.addImage(image, {
              //     tl: { col: excelCell.col - 1, row: excelCell.row - 1 },
              //     br: { col: excelCell.col, row: excelCell.row },
              //     editAs: undefined,
              //   })
              // }
            }

            if (gridCell.column.name === 'FICHA') {
              if (gridCell.value) {
                excelCell.value =
                  'SKU: ' +
                  gridCell.data.SKU +
                  '\n' +
                  gridCell.data.DESCRIP +
                  '\n' +
                  'Marca: ' +
                  gridCell.data.MARCA +
                  '\n' +
                  'Talla: ' +
                  gridCell.data.TALLA +
                  '\n' +
                  'Dist.: ' +
                  gridCell.data.DISTRIBUCION
                excelCell.alignment = { horizontal: 'justify', vertical: 'top' }
              }
            }

            if (
              gridCell.column.dataField === this.cur_variante &&
              vv.length > 0
            ) {
              masterRows.push({
                rowIndex: excelCell.fullAddress.row + 1,
                data: gridCell.data,
              })
            }
          }
          if (customTemplate) {
            if (gridCell.rowType === 'totalFooter' && excelCell.value) {
              excelCell.value = null
            }
          }
        },
      })
        .then((cellRange) => {
          if (customTemplate) {
            const row = worksheet.getRow(cellRange.from.row)
            row.values = []
            // row.hidden = true
            // worksheet.spliceRows(cellRange.from.row, 1)
            // console.log('FROMROW VALUE:', cellRange.from.row)
          }
          if (vv.length > 0) {
            const borderStyle = {
              style: 'thin',
              color: { argb: 'FF7E7E7E' },
            }
            let offset = 0
            let xrow

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
              // const columnIndex =
              //   this.curGrid.columnOption(this.cur_variante, 'visibleIndex') - 1
              const columnIndex =
                this.curGrid.getVisibleColumnIndex(this.cur_variante) - 1

              // const prodData = this.curStore.find(
              //   (item) => item.SKU === masterRows[i].data.SKU
              // )
              const prodSKU = masterRows[i].data.SKU

              const columns = [this.cur_variante, 'BARCODE']

              const row = insertRow(masterRows[i].rowIndex + i, offset++, 2)
              row.height = 15
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

              xrow = row

              getProdVariants(vv, prodSKU).forEach((variant, index) => {
                const row = insertRow(masterRows[i].rowIndex + i, offset++, 2)
                row.height = 15
                xrow = row

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
              if (xrow) {
                this.rowHeaderIndex.push(xrow.number + 1)
              }
            }
          }
        })
        .then(() => {
          Promise.all(PromiseArray).then(() => {
            workbook.xlsx.writeBuffer().then((buffer) => {
              saveAs(
                new Blob([buffer], { type: 'application/octet-stream' }),
                savingFilename
              )
              this.busyWith = false
              // this.rowHeaderIndex = [2]
              this.rowHeaderIndex = [topLeftCell.row + 1]
            })
          })
        })
    },
    manageCellClick(e) {
      if (e.column) {
        if (e.column.name === 'FOTO') {
          if (e.rowType === 'data') {
            // this.setSlidecurkey(e.key)
            this.curRowKey = e.key
            this.curRowIndex = e.rowIndex
            this.slideshow = true
          }
        }
      }
    },
    storeNoImg(imgfile) {
      if (!this.noImgList.includes(imgfile)) {
        this.noImgList.push(imgfile)
      }
    },
    addMenuItems(e) {
      if (e.target === 'header' && e.column.name === 'FOTO') {
        if (!e.items) e.items = []
        e.items.push(
          {
            text: 'Todos',
            icon: 'selectall',
            onItemClick: () => {
              this.curGrid.filter((item) => true)
            },
          },
          {
            text: 'Con foto',
            icon: 'photo',
            onItemClick: () => {
              this.curGrid.filter((item) => !this.noImgList.includes(item.FOTO))
            },
          },
          {
            text: 'Sin foto',
            icon: 'isblank',
            onItemClick: () => {
              this.curGrid.filter((item) => this.noImgList.includes(item.FOTO))
            },
          }
        )
      }
    },
    handlePropertyChange(e) {
      // console.log('***** PROP FULL NAME *****', e.fullName)
      if (e.name === 'columns') {
        this.$nextTick(() => {
          this.isTallaVisible = this.curGrid.columnOption('TALLA', 'visible')
        })

        this.$nextTick(() => {
          this.isColorVisible = this.curGrid.columnOption('COLORES', 'visible')
        })
      }

      if (!this.isTallaVisible && !this.isColorVisible) {
        this.makeVariantFalse()
      }
    },
    async addImageExcel(url, workbook, worksheet, excelCell, inirow, resolve) {
      await this.imgax
        .get(url, {
          responseType: 'arraybuffer',
        })
        .then((response) => {
          const base64Img = Buffer.from(response.data, 'binary').toString(
            'base64'
          )

          const image = workbook.addImage({
            base64: base64Img,
            extension: 'JPEG',
          })

          let indx = excelCell.row

          if (this.rowHeaderIndex.length > 1) {
            const imgIndex = excelCell.row - (inirow + 1)
            indx = this.rowHeaderIndex[imgIndex]
          }

          worksheet.getRow(indx).height = 100

          worksheet.addImage(image, {
            tl: { col: excelCell.col - 1, row: indx - 1 },
            br: { col: excelCell.col, row: indx },
          })

          resolve()
        })
        .catch(() => {
          // worksheet.getRow(excelCell.row).height = 15
          resolve()
        })
    },
    async addImagePDF(url, tPos, pdfDoc, resolve) {
      await this.imgax
        .get(url, {
          responseType: 'arraybuffer',
        })
        .then((response) => {
          const base64Img = Buffer.from(response.data, 'binary').toString(
            'base64'
          )

          pdfDoc.addImage(base64Img, 'JPEG', tPos.x, tPos.y, 22.5, 15)

          resolve()
        })
        .catch(() => {
          // worksheet.getRow(excelCell.row).height = 15
          resolve()
        })
    },
    async addImgForPDF(imgfile, resolve) {
      const imgurl = this.$config.fotosURL + imgfile
      await this.imgax
        .get(imgurl, {
          responseType: 'arraybuffer',
        })
        .then((response) => {
          const base64Img = Buffer.from(response.data, 'binary').toString(
            'base64'
          )

          this.imgListForPDF[imgfile] = base64Img
          resolve()
        })
        .catch(() => {
          resolve()
        })
    },
    makeVariantFalse() {
      this.cur_variante = ''
    },
    verifVar(v) {
      if (v === 1) {
        if (this.setvart) {
          this.setvarc = false
          this.cur_variante = 'TALLA'
        }
      }

      if (v === 2) {
        if (this.setvarc) {
          this.setvart = false
          this.cur_variante = 'COLORES'
        }
      }

      if (!this.setvart && !this.setvarc) {
        this.cur_variante = ''
      }
    },
    // testMethod() {
    //   const columnIndex = this.curGrid.getVisibleColumnIndex(this.cur_variante)
    //   console.log('***** COL_INDEX *****', columnIndex)
    // },
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

<style scoped>
.dx-data-row.dx-state-hover:not(.dx-selection):not(.dx-row-inserted):not(.dx-row-removed):not(.dx-edit-row)
  .cell-highlighted
  > td:not(.dx-focused) {
  background-color: #aed6f1 !important;
  cursor: pointer;
}
</style>
