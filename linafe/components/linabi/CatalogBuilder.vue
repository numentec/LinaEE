/* eslint-disable no-console */
<template>
  <client-only>
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
                  <v-icon>mdi-folder-open</v-icon>
                </v-list-item-icon>
                <v-list-item-title @click.stop="doAlert('Abrir')">
                  Abrir
                </v-list-item-title>
              </v-list-item>
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
                    <v-radio label="SKU" :value="1"></v-radio>
                    <v-radio label="Código de barra" :value="2"></v-radio>
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
            </v-list>
          </v-menu>
          <v-toolbar-title>Catálogo Personalizado</v-toolbar-title>
          <v-spacer />
          <v-btn icon @click="closeDialog()">
            <v-icon>mdi-window-close</v-icon>
          </v-btn>
        </v-toolbar>
        <v-card-text class="mt-2">
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
              :allow-exporting="keyCatalog == 1 ? true : false"
            />
            <DxColumn
              :allow-grouping="false"
              data-field="BARCODE"
              caption="BARCODE"
              :allow-header-filtering="true"
              :allow-exporting="keyCatalog == 2 ? true : false"
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
            <DxSearchPanel :visible="true" :highlight-case-sensitive="true" />
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
        </v-card-text>
      </v-card>
    </v-dialog>
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
import saveAs from 'file-saver'
import ExcelJS from 'exceljs'
import { exportDataGrid as exportDataGridToExcel } from 'devextreme/excel_exporter'
import ImgForGrid from '../utilities/ImgForGrid.vue'

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
      keyCatalog: 1,
      valid: true,
      verify: '',
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
    ...mapActions('linabi/catalogo', ['setCurCatalog', 'setChanges']),
    reset() {
      this.$refs.basefilters_form.reset()
    },
    closeDialog() {
      this.$emit('closeDialog')
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
            excelCell.value = ''
          }
          // if (gridCell.rowType === 'header') {
          //   excelCell.value = ''
          // }
        },
      }).then(() => {
        workbook.xlsx.writeBuffer().then((buffer) => {
          saveAs(
            new Blob([buffer], { type: 'application/octet-stream' }),
            'catalogo.xlsx'
          )
        })
      })
      this.menu = false
    },
    doAlert(msg) {
      this.menu = false
      alert(msg)
    },
  },
}
</script>

<style lang="scss" scoped></style>
