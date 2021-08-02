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
          <v-toolbar-title>Documentos de Ventas</v-toolbar-title>
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
              v-show="tab == 0"
              ref="settings0"
              :show-column-chooser="showColumnChooser"
              :set-filtros="setConf0.filtros"
              :set-agrupar="setConf0.agrupar"
              @set-conf-filtros="setConf0.filtros = !setConf0.filtros"
              @set-conf-agrupar="setConf0.agrupar = !setConf0.agrupar"
              @clear-all-filters="clearFilters"
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
                <v-list-item v-show="expDetail">
                  <v-list-item-action>
                    <v-switch v-model="variantes"></v-switch>
                  </v-list-item-action>
                  <v-list-item-content>
                    <v-list-item-title>Variantes</v-list-item-title>
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
                <v-list-item link>
                  <v-list-item-content>
                    <v-list-item-title @click.stop="exportGrid(3)">
                      PDF
                    </v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item link>
                  <v-list-item-content>
                    <v-list-item-title @click.stop="snackbar = true">
                      Guardar Fotos
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
                    <v-list-item-title @click.stop="snackbar = true">
                      Guardar
                    </v-list-item-title>
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
                <v-list-item v-show="tab == 0">
                  <v-list-item-action>
                    <v-switch v-model="setConf0.agrupar"></v-switch>
                  </v-list-item-action>
                  <v-list-item-content>
                    <v-list-item-title>Panel Agrupar</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item v-show="tab == 0">
                  <v-list-item-action>
                    <v-switch v-model="setConf0.filtros"></v-switch>
                  </v-list-item-action>
                  <v-list-item-content>
                    <v-list-item-title>Filtro avanzado</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item v-show="tab == 1">
                  <v-list-item-action>
                    <v-switch v-model="setConf1.agrupar"></v-switch>
                  </v-list-item-action>
                  <v-list-item-content>
                    <v-list-item-title>Panel Agrupar</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item v-show="tab == 1">
                  <v-list-item-action>
                    <v-switch v-model="setConf1.filtros"></v-switch>
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
                @row-dbl-click="loadDetailsForOne"
              >
                <DxColumn
                  v-for="xcol in colsConfig0"
                  :key="'tab0' + xcol.id"
                  :allow-grouping="xcol.configval7 == '1'"
                  :data-field="xcol.configkey"
                  :visible="xcol.configval3 == '1'"
                  :caption="xcol.configval2"
                  :data-type="xcol.configval4"
                  :format="setFormat(xcol.configval5)"
                  :alignment="xcol.configval6"
                  :sorting-method="selFunction(xcol.configval9)"
                />
                <DxSorting mode="multiple" />
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
                @cell-click="manageCellClick"
                @context-menu-preparing="addMenuItems"
              >
                <DxColumn
                  width="200"
                  :allow-grouping="false"
                  data-field="FOTO"
                  name="FOTO"
                  caption="Foto"
                  cell-template="imgCellTemplate"
                  css-class="cell-highlighted"
                  :allow-sorting="false"
                  :allow-header-filtering="false"
                />
                <DxColumn
                  v-for="xcol in colsConfig1"
                  :key="'tab1' + xcol.id"
                  :allow-grouping="xcol.configval7 == '1'"
                  :data-field="xcol.configkey"
                  :visible="xcol.configval3 == '1'"
                  :caption="xcol.configval2"
                  :data-type="xcol.configval4"
                  :format="setFormat(xcol.configval5)"
                  :alignment="xcol.configval6"
                  :sorting-method="selFunction(xcol.configval9)"
                />
                <DxSorting mode="multiple" />
                <DxMasterDetail :enabled="true" template="mdTemplate" />
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
                <template #mdTemplate="{ data }">
                  <ProdVariants
                    :variant-data="data.data.SKU"
                    :variant-title="'Códigos de Barra por Talla'"
                  />
                </template>
                <template #imgCellTemplate="{ data }">
                  <ImgForGrid
                    :img-file="data.value"
                    @no-image="storeNoImg(data.value)"
                  />
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
      :perms="filterPerms"
      :cur-view="curView"
      curstore="linabi/saledocsm"
      @closeDialog="closeDialog"
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
      :cur-index="curRowIndex"
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
import { mapState, mapActions } from 'vuex'
import { locale } from 'devextreme/localization'
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
import DxLoadPanel from 'devextreme-vue/load-panel'
import saveAs from 'file-saver'
import { jsPDF as JsPDF } from 'jspdf'
import 'jspdf-autotable'
import ExcelJS from 'exceljs'
import JSZip from 'jszip'
import { exportDataGrid as exportDataGridToPdf } from 'devextreme/pdf_exporter'
import { exportDataGrid as exportDataGridToExcel } from 'devextreme/excel_exporter'
import MaterialCard from '~/components/core/MaterialCard'
import BaseFilters from '~/components/linabi/BaseFilters'
import ProdVariants from '~/components/linabi/ProdVariants.vue'
import TemplatesAdmin from '~/components/linabi/TemplatesAdmin.vue'
import Slideshow from '~/components/linabi/Slideshow'
import ImgForGrid from '~/components/utilities/ImgForGrid'
import TableSettings from '~/components/utilities/TableSettings'
import LoadingView from '~/components/utilities/LoadingView'
import { selFunction } from '~/assets/utilities'

const curGridRefKey0 = 'cur-grid1'
const curGridRefKey1 = 'cur-grid2'
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
      .catch((err) => {
        reject(err.toString())
      })
  })
}

function uniqByKeepLast(data, key) {
  return [...new Map(data.map((x) => [key(x), x])).values()]
}

function getProdVariants(variants, sku) {
  return variants.filter((v) => v.SKU === sku)
}

const contextItems = [
  { text: 'Todos' },
  { text: 'Con foto' },
  { text: 'Sin foto' },
]

export default {
  name: 'SaleDocs',
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
    DxLoadPanel,
    MaterialCard,
    BaseFilters,
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
      const [resp0, resp1, resp2] = await Promise.all([
        $axios.get('vistas/16/'),
        $axios.get('vistas/17/'),
        $axios.get('accviewconf-list/', {
          params: { idvista: '16', groups: groupList },
        }),
      ])
      const filterPerms = uniqByKeepLast(resp2.data, (it) => it.vistaconf)
      return {
        curView: {
          num: resp0.data.id,
          checkelperms: resp0.data.checkelperms,
        },
        config0: resp0.data.configs_x_vista,
        config1: resp1.data.configs_x_vista,
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
      tab: 0,
      curGridRefKey0,
      curGridRefKey1,
      selFunction,
      dataSource0: null,
      dataSource1: null,
      variantes: false,
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
      showSelTemplate: false,
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
      plantilla: {
        name: '',
        savingFilename: '',
        row: 1,
        col: 1,
      },
      slideshow: false,
      curRowKey: '',
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
    }
  },
  computed: {
    ...mapState('linabi/favoritos', ['breadCrumbsItems']),
    ...mapState('linabi/saledocsm', ['filters']),
    ...mapState('linabi/saledocsd', ['getCurStore']),
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
        if (!result) {
          this.makeVariantFalse()
        }
      }
      return result
    },
    noImgFilters() {
      return [
        {
          text: 'Con foto',
          value: ['SKU', 'noneof', this.noImgList],
        },
        {
          text: 'Sin foto',
          value: ['SKU', 'anyof', this.noImgList],
        },
      ]
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
    savePhotos() {
      this.menuFilter = false

      // const selRowsData = this.curGrid.getSelectedRowsData()
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
      if (this.tab === 1) {
        this.dataSource1 = null
      } else {
        this.dataSource0 = null
        this.dataSource1 = null
      }

      this.menuFilter = false
    },
    clearFilters(opc = 'all') {
      if (this.tab === 0) {
        if (opc !== 'all') {
          this.curGrid0.clearFilter(opc)
        } else {
          this.curGrid0.clearFilter()
        }
      }

      if (opc !== 'all') {
        this.curGrid1.clearFilter(opc)
      } else {
        this.curGrid1.clearFilter()
      }

      this.menuConf = false
      this.menuFilter = false
    },
    clearSorting() {
      if (this.tab === 0) {
        this.curGrid0.clearSorting()
      }
      this.curGrid1.clearSorting()
      this.menuFilter = false
    },
    clearGrouping() {
      if (this.tab === 0) {
        this.curGrid0.clearGrouping()
      }
      this.curGrid1.clearGrouping()
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
        this.tab = 0
      }
    },
    loadDetails() {
      const selectedRows = this.curGrid0.getSelectedRowKeys()
      this.menuFilter = false
      if (selectedRows.length > 0) {
        this.noImgList = []
        const numdocs = selectedRows.toString()
        this.fetchDatails(numdocs)
        this.tab = 1
      }
    },
    loadDetailsForOne(e) {
      if (e.rowType === 'data') {
        this.noImgList = []
        this.fetchDatails(e.key)
        this.tab = 1
      }
    },
    fetchDatails(numdocs) {
      const tipodoc = this.filters.p15
      this.setFiltersDetails({ p01: numdocs, p15: tipodoc })
      this.fetchDataDetails().then((store) => {
        this.dataSource1 = store
      })
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
    selTemplate() {
      this.showSelTemplate = true
      this.menuFilter = false
    },
    doExportTemplate(e) {
      let curGrid

      if (this.tab === 0) {
        curGrid = this.curGrid0
      } else {
        curGrid = this.curGrid1
      }

      this.plantilla.name = e.name.toLowerCase() + '.xlsx'
      this.plantilla.row = e.inirow
      this.plantilla.col = e.inicol
      this.plantilla.savingFilename = e.name + '.xlsx'

      curGrid.beginCustomLoading('Cargando plantilla')

      setTimeout(() => {
        // Current visible columns
        const vc = curGrid
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
          curGrid.columnOption(col.name, {
            visible: true,
            visibleIndex: col.ordinal,
          })
        })

        // Hide extra columns
        cth.forEach((col) => {
          curGrid.columnOption(col.name, { visible: false })
        })
      }, 500)

      setTimeout(() => {
        curGrid.endCustomLoading()
        this.exportGrid(2)
      }, 500)
    },
    closeSelTemplate() {
      this.showSelTemplate = false
    },
    exportGrid(opc) {
      this.menuFilter = false

      let curGrid

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

      // const selectedRows = curGrid.component.getSelectedRowKeys()
      const selectedRowsData = curGrid.component.getSelectedRowsData()
      if (selectedRowsData.length > 0) {
        const selectedRows = selectedRowsData.map((obj) => obj.SKU)

        // Exportar a Excel
        if (opc === 1) {
          const savingFilename = curGrid.docname + '.xlsx'
          const workbook = new ExcelJS.Workbook()
          const worksheet = workbook.addWorksheet(curGrid.docname)
          const tLC = { row: 1, column: 1 }
          if (this.variantes) {
            // Exportar a Excel con detalle de códigos de barra
            this.fetchVariants({ sku: selectedRows }).then((vv) => {
              this.doExportExcel(
                workbook,
                worksheet,
                savingFilename,
                tLC,
                vv,
                curGrid
              )
            })
          } else {
            this.doExportExcel(
              workbook,
              worksheet,
              savingFilename,
              tLC,
              [],
              curGrid
            )
          }
        }

        // Exportar a Excel usando plantilla (Tova)
        if (opc === 2) {
          customTemplate = true
          const template = 'plantillas/' + this.plantilla.name
          const axx = this.$axios.create({
            baseURL: this.$config.mediaURL,
            headers: {
              common: {
                Accept: 'application/json, text/plain, */*',
              },
            },
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

                if (this.variantes) {
                  // Exportar a Excel con detalle de códigos de barra
                  this.fetchVariants({ sku: selectedRows }).then((vv) => {
                    this.doExportExcel(
                      workbook,
                      worksheet,
                      savingFilename,
                      topLeftCell,
                      [vv],
                      curGrid
                    )
                  })
                } else {
                  this.doExportExcel(
                    workbook,
                    worksheet,
                    savingFilename,
                    topLeftCell,
                    [],
                    curGrid
                  )
                }
              })
            })
        }

        // Exportar a PDF
        if (opc === 3) {
          this.doExportPDF(curGrid)
        }
      }
    },

    doExportPDF(curGrid) {
      this.busyWith = true
      const pdfDoc = new JsPDF({
        orientation: 'landscape',
        format: 'letter',
      })

      let mch = { minCellHeight: 5 }
      // Foto column index
      let fci = -1
      if (curGrid.docname === 'ventas_detalle') {
        if (curGrid.component.columnOption('FOTO', 'visible')) {
          mch = { minCellHeight: 20 }
        }

        fci = curGrid.component.getVisibleColumnIndex('FOTO') - 2
      }

      exportDataGridToPdf({
        component: curGrid.component,
        jsPDFDocument: pdfDoc,
        selectedRowsOnly: true,
        autoTableOptions: {
          bodyStyles: mch,
          didDrawCell: (data) => {
            if (curGrid.docname === 'ventas_detalle') {
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
            }
          },
        },
      }).then(() => {
        pdfDoc.save(curGrid.docname + '.pdf')
        this.busyWith = false
      })
    },

    doExportExcel(
      workbook,
      worksheet,
      savingFilename,
      topLeftCell = { row: 1, column: 1 },
      vv = [],
      curGrid
    ) {
      const PromiseArray = []
      const masterRows = []

      this.rowHeaderIndex = [topLeftCell.row + 1]

      this.busyWith = true

      exportDataGridToExcel({
        component: curGrid.component,
        worksheet,
        topLeftCell,
        autoFilterEnabled: !customTemplate,
        selectedRowsOnly: true,
        customizeCell: ({ excelCell, gridCell }) => {
          if (curGrid.docname === 'ventas_detalle') {
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
              }

              if (gridCell.column.dataField === 'TALLA' && vv.length > 0) {
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
          }
        },
      })
        .then((cellRange) => {
          if (customTemplate) {
            const row = worksheet.getRow(cellRange.from.row)
            row.values = []
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
              // worksheet.getRow(row.number).height = 15

              for (let j = worksheet.rowCount + 1; j > currentIndex; j--) {
                worksheet.getRow(j).outlineLevel = worksheet.getRow(
                  j - 1
                ).outlineLevel
              }

              row.outlineLevel = outlineLevel

              return row
            }

            for (let i = 0; i < masterRows.length; i++) {
              const columnIndex = cellRange.from.column + 1
              // const columnIndex =
              //   curGrid.component.columnOption('TALLA', 'visibleIndex') - 1
              const prodSKU = masterRows[i].data.SKU

              const prodvv = getProdVariants(vv, prodSKU)

              // if (prodvv.length > 0) {
              const columns = ['TALLA', 'BARCODE']

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
              // console.log('INSERTED ROW', xrow)

              prodvv.forEach((variant, index) => {
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
              // }
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
            this.curRowKey = e.key.toString()
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
              e.component.filter((item) => true)
            },
          },
          {
            text: 'Con foto',
            icon: 'photo',
            onItemClick: () => {
              e.component.filter((item) => !this.noImgList.includes(item.FOTO))
            },
          },
          {
            text: 'Sin foto',
            icon: 'isblank',
            onItemClick: () => {
              e.component.filter((item) => this.noImgList.includes(item.FOTO))
            },
          }
        )
      }
    },
    async addImageExcel(url, workbook, worksheet, excelCell, inirow, resolve) {
      let indx = excelCell.row
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
          // worksheet.getRow(indx).height = 100
          resolve()
        })
    },
    makeVariantFalse() {
      this.variantes = false
    },
    // testMethod() {
    //   const fp = uniqByKeepLast(this.filterPerms, (it) => it.vistaconf)
    //   console.log('filterPerms', fp[0].configkey)
    // },
  },
  head() {
    return {
      title: 'Docs Ventas',
    }
  },
}
</script>
