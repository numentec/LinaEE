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
                  <v-list-item-title @click.stop="snackbar = true">
                    Publicar
                  </v-list-item-title>
                </v-list-item>
                <v-list-item link>
                  <v-list-item-icon>
                    <v-icon>mdi-content-save-all</v-icon>
                  </v-list-item-icon>
                  <v-list-item-title @click.stop="doExportExcel">
                    Exportar
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
              <v-tab key="tab0" dense> En proceso </v-tab>
              <v-tab key="tab1" dense> Importar </v-tab>
              <v-tab key="tab2" dense> Publicados </v-tab>
              <v-tabs-items v-model="tab">
                <v-tab-item key="tab0">
                  <DxDataGrid
                    :ref="curGridRefKey"
                    key-expr="SKU"
                    :focused-row-enabled="true"
                    :data-source="getCurCatalog"
                    :remote-operations="false"
                    :allow-column-resizing="true"
                    column-resizing-mode="widget"
                    :row-alternation-enabled="true"
                    :show-column-lines="true"
                    :show-row-lines="false"
                    :show-borders="true"
                    height="500px"
                    @saving="onSaving"
                    @cell-click="showDetail"
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
                      :width="150"
                      :allow-header-filtering="true"
                      :allow-exporting="keyCatalog == 'SKU' ? true : false"
                    />
                    <DxColumn
                      :allow-grouping="false"
                      data-field="BARCODE"
                      caption="BARCODE"
                      :width="150"
                      :allow-header-filtering="true"
                      :allow-exporting="keyCatalog == 'BC' ? true : false"
                    />
                    <DxColumn
                      :allow-grouping="false"
                      data-field="DESCRIP"
                      caption="Descripción"
                      :width="250"
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
                      <div id="dropzone-frame">
                        <v-hover v-slot="{ hover }">
                          <v-card
                            clas="mx-auto"
                            :class="{ 'on-hover': hover }"
                            flat
                            tile
                            :outlined="hover || isDropZoneActive"
                          >
                            <DxTileView
                              :items="photosByKey(cellData.key)"
                              :height="200"
                              :base-item-height="120"
                              :base-item-width="185"
                              width="100%"
                              :item-margin="10"
                            >
                              <template #item="{ data }">
                                <div
                                  :style="{
                                    backgroundImage: 'url(' + data.imgsrc + ')',
                                  }"
                                  class="dx-tile-image"
                                />
                              </template>
                            </DxTileView>
                          </v-card>
                        </v-hover>
                      </div>
                    </template>
                  </DxDataGrid>
                </v-tab-item>
                <v-tab-item key="tab1">
                  <v-card flat>
                    <v-form>
                      <DxFileUploader
                        id="file-uploader1"
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
      <DxFileUploader
        id="file-uploader2"
        dialog-trigger="#dropzone-frame"
        drop-zone="#dropzone-frame"
        :multiple="false"
        :allowed-file-extensions="allowedFileExtensions"
        upload-mode="instantly"
        upload-url=""
        :visible="false"
        @drop-zone-enter="onDropZoneEnter"
        @drop-zone-leave="onDropZoneLeave"
        @uploaded="onUploaded"
        @progress="onProgress"
        @upload-started="onUploadStarted"
      />
      <v-snackbar v-model="snackbar" timeout="2000">
        No implementado
        <template v-slot:action="{ attrs }">
          <v-btn
            color="secondary"
            text
            v-bind="attrs"
            @click="snackbar = false"
          >
            Cerrar
          </v-btn>
        </template>
      </v-snackbar>
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
import DxTileView from 'devextreme-vue/tile-view'
import saveAs from 'file-saver'
import ExcelJS from 'exceljs'
import { exportDataGrid as exportDataGridToExcel } from 'devextreme/excel_exporter'
import XLSX from 'xlsx'

const curGridRefKey = 'cur-grid'

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
    DxTileView,
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
      showdetails: false,
      curRowIndex: -1,
      isDropZoneActive: false,
      allowedFileExtensions: ['.jpg', '.jpeg', '.gif', '.png'],
      snackbar: false,
    }
  },
  computed: {
    ...mapGetters('linabi/catalogo', ['getCurCatalog', 'getPhotosList']),
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
      if (e.rowType === 'data') {
        if (this.curRowIndex !== e.rowIndex) {
          this.showdetails = false
          this.curRowIndex = e.rowIndex
        }
        this.showdetails = !this.showdetails
        if (this.showdetails) {
          e.component.collapseAll(-1)
          e.component.expandRow(e.key)
          // e.component.expandRow(e.currentSelectedRowKeys[0])
        } else {
          e.component.collapseAll(-1)
        }
      }
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
    photosByKey(key) {
      return this.getPhotosList.filter((item) => item.sku === key)
    },
    // Upload image methods
    onDropZoneEnter(e) {
      if (e.dropZoneElement.id === 'dropzone-frame') {
        this.isDropZoneActive = true
      }
    },
    onDropZoneLeave(e) {
      if (e.dropZoneElement.id === 'dropzone-frame') {
        this.isDropZoneActive = false
      }
    },
    onUploaded(e) {
      // const file = e.file
    },
    onProgress(e) {},
    onUploadStarted() {},
  },
}
</script>

<style scoped>
.dx-tile-image {
  height: 100%;
  width: 100%;
  background-position: center;
  background-size: cover;
  display: block;
}
</style>
