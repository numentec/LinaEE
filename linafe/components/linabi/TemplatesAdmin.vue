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
                  <v-list-item-title> ***** </v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
            <v-toolbar-title>Administrar Plantillas de Excel</v-toolbar-title>
            <v-spacer />
            <v-btn icon @click="closeDialog()">
              <v-icon>mdi-window-close</v-icon>
            </v-btn>
          </v-toolbar>
          <v-card-text class="mt-2">
            <v-tabs v-model="tab">
              <v-tab key="tab0" dense> Lista </v-tab>
              <v-tab key="tab1" dense> Procesar </v-tab>
              <v-tabs-items v-model="tab">
                <v-tab-item key="tab0">
                  <DxDataGrid
                    :ref="curGridRefKey"
                    :focused-row-enabled="true"
                    :data-source="dataSource"
                    :remote-operations="false"
                    :allow-column-resizing="true"
                    column-resizing-mode="widget"
                    :row-alternation-enabled="true"
                    :show-column-lines="true"
                    :show-row-lines="false"
                    :show-borders="true"
                    height="500px"
                  >
                    <DxColumn
                      :allow-grouping="false"
                      data-field="id"
                      caption="ID"
                      :width="100"
                      :allow-header-filtering="false"
                    />
                    <DxColumn
                      :allow-grouping="false"
                      data-field="name"
                      caption="Plantilla"
                      :width="200"
                      :allow-header-filtering="true"
                    />
                    <DxColumn
                      :allow-grouping="false"
                      data-field="descrip"
                      caption="Descripción"
                      :width="300"
                      :allow-header-filtering="true"
                    />
                    <DxColumn
                      :width="75"
                      caption="Sel"
                      cell-template="btnSelTemplate"
                    />
                    <DxSummary>
                      <DxTotalItem
                        column="id"
                        summary-type="count"
                        display-format="{0}  Registros"
                      />
                    </DxSummary>
                    <DxSearchPanel
                      :visible="true"
                      :highlight-case-sensitive="true"
                    />
                    <DxHeaderFilter :visible="true" />
                    <DxScrolling mode="virtual" />
                    <DxSelection mode="single" />
                    <DxLoadPanel :enable="true" />
                    <template #btnSelTemplate="{ data: cellData }">
                      <v-btn icon @click="selTemplate(cellData)">
                        <v-icon color="primary lightn-2">
                          mdi-check-circle-outline
                        </v-icon>
                      </v-btn>
                    </template>
                  </DxDataGrid>
                </v-tab-item>
                <v-tab-item key="tab1">
                  <v-card flat>
                    <v-form>
                      <DxFileUploader
                        select-button-text="Explorar"
                        label-text="(Arrastre el archivo aquí)"
                        :allowed-file-extensions="['.xlsx']"
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
    </div>
  </client-only>
</template>

<script>
import { mapActions } from 'vuex'
import {
  DxDataGrid,
  DxColumn,
  DxSummary,
  DxTotalItem,
  DxSearchPanel,
  DxHeaderFilter,
  DxScrolling,
  DxSelection,
} from 'devextreme-vue/data-grid'
import DxLoadPanel from 'devextreme-vue/load-panel'
import DxFileUploader from 'devextreme-vue/file-uploader'

const curGridRefKey = 'cur-grid'

export default {
  name: 'TemplatesAdmin',
  components: {
    DxDataGrid,
    DxColumn,
    DxSummary,
    DxTotalItem,
    DxSearchPanel,
    DxHeaderFilter,
    DxScrolling,
    DxSelection,
    DxLoadPanel,
    DxFileUploader,
  },
  props: {
    dialog: Boolean,
    numvista: {
      type: Number,
      default: 0,
    },
  },

  async fetch() {
    // Lista de plantillas xlsx
    await this.fetchTemplates().then((store) => {
      this.dataSource = store
    })
  },

  data() {
    return {
      curGridRefKey,
      dataSource: null,
      menu: false,
      tab: 0,
      files: [],
      rules: {
        required: (value) => !!value || 'Requerido.',
      },
    }
  },
  computed: {
    curGrid() {
      return this.$refs[curGridRefKey].instance
    },
  },
  created() {},
  methods: {
    ...mapActions('linabi/common', ['fetchTemplates']),
    selTemplate(e) {
      const templateInfo = {
        id: e.data.id,
        name: e.data.name,
        inirow: e.data.row,
        inicol: e.data.col,
        cols: e.data.cols_x_plantilla,
      }
      this.closeDialog()
      this.$emit('setTemplate', templateInfo)
    },
    closeDialog() {
      this.$emit('closeDialog')
    },
    uploadStarter(e) {
      e.request.abort()
    },
    uploadAborted() {},
    readFile(file) {},
  },
}
</script>

<style lang="scss" scoped></style>
