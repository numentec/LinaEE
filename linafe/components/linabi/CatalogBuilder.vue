/* eslint-disable no-console */
<template>
  <client-only>
    <div>
      <v-dialog
        :value="dialog"
        persistent
        max-width="800px"
        min-width="400px"
        max-height="750px"
        @input="$emit('update:dialog', false)"
        @keydown.esc="closeDialog()"
      >
        <v-card max-height="700px">
          <v-toolbar color="accent darken-3" dark dense>
            <v-menu
              v-model="menu"
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
                    <v-icon>mdi-content-save-all</v-icon>
                  </v-list-item-icon>
                  <v-list-item-title @click.stop="doExportExcel">
                    Guardar
                  </v-list-item-title>
                </v-list-item>
                <v-list-item>
                  <v-list-item-content>
                    <v-radio-group v-model="keyCatalog">
                      <v-radio label="SKU" value="SKU"></v-radio>
                      <v-radio label="Código de barra" value="BC"></v-radio>
                    </v-radio-group>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item link>
                  <v-list-item-icon>
                    <v-icon>mdi-table-cancel</v-icon>
                  </v-list-item-icon>
                  <v-list-item-title @click.stop="clearCatalog">
                    Limpiar
                  </v-list-item-title>
                </v-list-item>
                <v-list-item link>
                  <v-list-item-icon>
                    <v-icon>mdi-table-arrow-down</v-icon>
                  </v-list-item-icon>
                  <v-list-item-title @click="downloadCatalog()">
                    Descargar
                  </v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
            <v-toolbar-title>Catálogo Personalizado</v-toolbar-title>
            <v-spacer />
            <v-btn icon @click="closeDialog()">
              <v-icon>mdi-window-close</v-icon>
            </v-btn>
          </v-toolbar>
          <v-card-text class="mt-2">
            <v-tabs v-model="tab">
              <v-tab key="tab0" dense> En construcción </v-tab>
              <v-tab key="tab1" dense> Cargar archivo </v-tab>
              <v-tabs-items v-model="tab">
                <v-tab-item key="tab0">
                  <DxDataGrid
                    :ref="curGridRefKey"
                    key-expr="SKU"
                    :focused-row-enabled="true"
                    :data-source="getCurCatalog"
                    :remote-operations="false"
                    :column-auto-width="true"
                    :allow-column-resizing="true"
                    column-resizing-mode="widget"
                    :row-alternation-enabled="true"
                    :show-column-lines="true"
                    :show-row-lines="false"
                    :show-borders="true"
                    height="500px"
                    @selection-changed="showDetail"
                    @saving="onSaving"
                  >
                    <DxEditing
                      :changes="changes"
                      :allow-deleting="true"
                      mode="row"
                      :confirm-delete="false"
                    />
                    <DxColumn
                      :allow-grouping="false"
                      data-field="SKU"
                      caption="SKU"
                      :allow-header-filtering="true"
                      :allow-exporting="keyCatalog == 'SKU' ? true : false"
                    />
                    <DxColumn
                      :allow-grouping="false"
                      data-field="BARCODE"
                      caption="BARCODE"
                      :allow-header-filtering="true"
                      :allow-exporting="keyCatalog == 'BC' ? true : false"
                    />
                    <DxColumn
                      :allow-grouping="false"
                      data-field="DESCRIP"
                      caption="Descripción"
                      :allow-header-filtering="true"
                      :allow-exporting="false"
                    />
                    <DxSummary>
                      <DxTotalItem
                        column="SKU"
                        summary-type="count"
                        display-format="{0}  Registros"
                      />
                    </DxSummary>
                    <DxMasterDetail :enabled="false" template="mdTemplate" />
                    <DxSearchPanel
                      :visible="true"
                      :highlight-case-sensitive="true"
                    />
                    <DxHeaderFilter :visible="true" />
                    <DxScrolling mode="virtual" />
                    <DxSelection mode="single" />
                    <DxLoadPanel :enable="true" />
                    <template #mdTemplate="{ data: cellData }">
                      <v-row>
                        <v-col>
                          <ImgForGrid :img-file="{ value: cellData.key }" />
                        </v-col>
                        <v-col>
                          <p>{{ cellData.data.DESCRIP_EN }}</p>
                        </v-col>
                      </v-row>
                    </template>
                  </DxDataGrid>
                </v-tab-item>
                <v-tab-item key="tab1">
                  <v-card flat>
                    <v-form>
                      <DxFileUploader
                        select-button-text="Explorar"
                        label-text="(Arrastre el archivo aquí)"
                        :allowed-file-extensions="['.xlsx', '.xls']"
                        upload-mode="instantly"
                        @value-changed="(e) => (files = e.value)"
                        @upload-started="uploadStarter"
                        @upload-aborted="uploadAborted"
                      />
                    </v-form>
                  </v-card>
                </v-tab-item>
              </v-tabs-items>
            </v-tabs>
          </v-card-text>
        </v-card>
      </v-dialog>
      <v-dialog v-model="replaceDialog" max-width="300">
        <v-card>
          <v-card-title class="headline"> ¿Reemplazar artículos? </v-card-title>

          <v-card-text>
            El catálogo en construcción ya tiene artículos. Indique que
            operación desea realizar.
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" text @click="addFileToCatalog(true)">
              Reemplazar
            </v-btn>

            <v-btn color="green darken-1" text @click="addFileToCatalog(false)">
              Añadir
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
  </client-only>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import {
  DxDataGrid,
  DxEditing,
  DxColumn,
  DxSummary,
  DxTotalItem,
  DxMasterDetail,
  DxSearchPanel,
  DxHeaderFilter,
  DxScrolling,
  DxSelection,
} from 'devextreme-vue/data-grid'
import DxLoadPanel from 'devextreme-vue/load-panel'
import DxFileUploader from 'devextreme-vue/file-uploader'
import saveAs from 'file-saver'
import ExcelJS from 'exceljs'
import { exportDataGrid as exportDataGridToExcel } from 'devextreme/excel_exporter'
import XLSX from 'xlsx'
import ImgForGrid from '../utilities/ImgForGrid.vue'

const curGridRefKey = 'cur-grid'
// const makeCols = (refstr) =>
//   Array(XLSX.utils.decode_range(refstr).e.c + 1)
//     .fill(0)
//     .map((x, i) => ({ name: XLSX.utils.encode_col(i), key: i }))

export default {
  name: 'CatalogBuilder',
  components: {
    DxDataGrid,
    DxEditing,
    DxColumn,
    DxSummary,
    DxTotalItem,
    DxMasterDetail,
    DxSearchPanel,
    DxHeaderFilter,
    DxScrolling,
    DxSelection,
    DxLoadPanel,
    DxFileUploader,
    ImgForGrid,
  },
  props: {
    dialog: Boolean,
    numvista: {
      type: Number,
      default: 0,
    },
    curstore: {
      type: String,
      default: '',
    },
  },

  data() {
    return {
      curGridRefKey,
      menu: false,
      tab: 0,
      keyCatalog: 'SKU',
      valid: true,
      verify: '',
      files: [],
      fileData: [],
      fileCols: [],
      replaceDialog: false,
      rules: {
        required: (value) => !!value || 'Requerido.',
      },
    }
  },
  computed: {
    ...mapGetters('linabi/catalogo', ['getCurCatalog']),
    changes: {
      get() {
        return this.$store.state.linabi.catalogo.changes
      },
      set(value) {
        this.setChanges(value)
      },
    },
    curGrid() {
      return this.$refs[curGridRefKey].instance
    },
  },
  created() {},
  methods: {
    ...mapActions('linabi/catalogo', [
      'fetchCatalogData',
      'setCurCatalog',
      'setChanges',
    ]),
    reset() {
      this.$refs.catalogbuilder_form.reset()
    },
    closeDialog() {
      this.$emit('closeDialog')
    },
    downloadCatalog() {
      this.$emit('downloadCatalog')
    },
    clearCatalog() {
      this.setCurCatalog([])
      this.menu = false
    },
    showDetail(e) {
      e.component.collapseAll(-1)
      e.component.expandRow(e.currentSelectedRowKeys[0])
    },
    onSaving(e) {
      e.cancel = true
      const rwkey = e.changes[0].key
      const data = this.getCurCatalog.filter((el) => el.SKU !== rwkey)
      this.setCurCatalog(data)
    },
    doExportExcel() {
      const workbook = new ExcelJS.Workbook()
      const worksheet = workbook.addWorksheet('Catalogo')

      exportDataGridToExcel({
        component: this.curGrid,
        worksheet,
        customizeCell: ({ excelCell, gridCell }) => {
          if (gridCell.rowType === 'totalFooter' && excelCell.value) {
            excelCell.value = null
          }
          // if (gridCell.rowType === 'header') {
          //   excelCell.value = ''
          // }
        },
      })
        .then((cellRange) => {
          worksheet.spliceRows(cellRange.from.row, 1)
          worksheet.spliceRows(cellRange.to.row, 1)
        })
        .then(() => {
          workbook.xlsx.writeBuffer().then((buffer) => {
            saveAs(
              new Blob([buffer], { type: 'application/octet-stream' }),
              'catalogo.xlsx'
            )
          })
        })

      this.menu = false
    },
    addFileToCatalog(opc) {
      this.replaceDialog = false
      if (opc) {
        this.setCurCatalog([])
      }
      this.readFile(this.files[0])
    },
    uploadAborted() {
      if (this.getCurCatalog.length > 0) {
        this.replaceDialog = true
      } else {
        this.addFileToCatalog(false)
      }
    },
    uploadStarter(e) {
      e.request.abort()
    },
    readFile(file) {
      const reader = new FileReader()
      reader.onload = (e) => {
        const bstr = e.target.result
        const wb = XLSX.read(bstr, { type: 'binary' })
        const wsname = wb.SheetNames[0]
        const ws = wb.Sheets[wsname]
        const data = XLSX.utils.sheet_to_json(ws, { header: ['SKU'] })
        const strdata = data.map(({ SKU }) => SKU)
        const params = { p01: strdata, p02: this.keyCatalog }
        this.fetchCatalogData(params).then(() => (this.tab = 0))
      }
      reader.readAsBinaryString(file)
    },
    doAlert(msg) {
      this.menu = false
      alert(msg)
    },
  },
}
</script>

<style lang="scss" scoped></style>
