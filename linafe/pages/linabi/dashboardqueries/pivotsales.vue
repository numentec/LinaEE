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
          <v-toolbar-title>{{
            `Ventas por ${curRow} (${curPeriodText})`
          }}</v-toolbar-title>
          <v-spacer />
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
                <v-list-item-title @click.stop="showSetPeriod = true">
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
              <v-list-item link>
                <v-list-item-icon>
                  <v-icon>mdi-expand-all-outline</v-icon>
                </v-list-item-icon>
                <v-list-item-title @click.stop="expandAll">
                  Expandir todo
                </v-list-item-title>
              </v-list-item>
              <v-list-item link>
                <v-list-item-icon>
                  <v-icon>mdi-collapse-all-outline</v-icon>
                </v-list-item-icon>
                <v-list-item-title @click.stop="collapseAll">
                  Contraer todo
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
                    <v-list-item-title @click.stop="exportGrid('xlsx')">
                      Excel
                    </v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item link>
                  <v-list-item-content>
                    <v-list-item-title @click.stop="exportGrid('csv')">
                      CSV
                    </v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list-group>
              <v-list-item link>
                <v-list-item-icon>
                  <v-icon>mdi-cog-outline</v-icon>
                </v-list-item-icon>
                <v-list-item-title @click.stop="snackbar = true"
                  >Ajustes</v-list-item-title
                >
              </v-list-item>
            </v-list>
          </v-menu>
        </v-toolbar>
      </template>
      <div ref="resizableDiv" v-resize="onResize">
        <DxPivotGrid
          :ref="curGridRefKey"
          :data-source="dataSource"
          row-header-layout="tree"
          :allow-sorting-by-summary="true"
          :allow-sorting="true"
          :allow-filtering="true"
          :allow-expand-all="true"
          :height="tableHeight"
          :show-borders="true"
          :remote-operations="false"
        >
          <DxFieldChooser :enabled="true" />
        </DxPivotGrid>
      </div>
      <LoadingView :busy-with="busyWith" :message="loadingMessage" />
      <v-overlay :absolute="true" :value="$fetchState.pending">
        <v-progress-circular indeterminate size="64"></v-progress-circular>
      </v-overlay>
    </MaterialCard>
    <v-snackbar v-model="snackbar" timeout="2000">
      No implementado
      <template v-slot:action="{ attrs }">
        <v-btn color="secondary" text v-bind="attrs" @click="snackbar = false">
          Cerrar
        </v-btn>
      </template>
    </v-snackbar>
    <v-dialog
      ref="periodDialog"
      v-model="showSetPeriod"
      :return-value.sync="curPeriod"
      persistent
      width="290px"
    >
      <v-date-picker
        v-model="curPeriod"
        range
        scrollable
        locale="es-pa"
        color="blue lighten-1"
      >
        <v-spacer></v-spacer>
        <v-btn text color="primary" @click="showSetPeriod = false">
          Cancelar
        </v-btn>
        <v-btn text color="primary" @click="updatePeriod"> Aceptar </v-btn>
      </v-date-picker>
    </v-dialog>
  </div>
</template>
<script>
import { mapActions, mapGetters } from 'vuex'
import { locale } from 'devextreme/localization'
import DxPivotGrid, { DxFieldChooser } from 'devextreme-vue/pivot-grid'
import PivotGridDataSource from 'devextreme/ui/pivot_grid/data_source'

import saveAs from 'file-saver'
import ExcelJS from 'exceljs'
import { exportPivotGrid } from 'devextreme/excel_exporter'
import MaterialCard from '~/components/core/MaterialCard'
import LoadingView from '~/components/utilities/LoadingView'

const curGridRefKey = 'cur-grid'

const arrayEquals = (a, b) => {
  return a.length === b.length && a.every((v, i) => v === b[i])
}

const setFields = (row) => {
  return [
    {
      dataField: row,
      area: 'row',
      sortBySummaryField: 'MONTO',
    },
    {
      dataField: 'FECHA',
      dataType: 'date',
      area: 'column',
    },
    {
      dataField: 'MONTO',
      dataType: 'number',
      summaryType: 'sum',
      format: '#,##0.00',
      area: 'data',
      isMeasure: true,
    },
  ]
}

export default {
  name: 'PivotSales',
  components: {
    DxPivotGrid,
    DxFieldChooser,
    MaterialCard,
    LoadingView,
  },
  async fetch() {
    let fields = []

    if (this.dataSource) {
      fields = this.dataSource.fields()
      // eslint-disable-next-line no-console
      // console.log(fields)
    } else {
      const fi = this.$route.query.fechini
      const ff = this.$route.query.fechfin
      const crow = this.$route.query.row

      this.filtered = this.$route.query.filtered

      this.curPeriod = [fi, ff]

      fields = setFields(crow)
      // eslint-disable-next-line no-console
      // console.log(fields)
    }

    if (this.curPeriod.length === 1) {
      this.curPeriod.push(this.curPeriod[0])
      this.$refs.dMenu.save(this.curPeriod)
    }

    const curparams = {
      p01: 14,
      p02: this.getCurCia.extrel,
      p03: this.curPeriod[0],
      p04: this.curPeriod[1],
      p05: this.filtered,
    }

    await this.renewStore(curparams).then((store) => {
      this.dataSource = new PivotGridDataSource({
        store,
        fields,
      })
    })
  },
  data() {
    return {
      curGridRefKey,
      dataSource: null,
      curPeriod: [],
      curRow: '',
      forceRefresh: false,
      menuFilter: false,
      showSetPeriod: false,
      tableHeight: 0,
      snackbar: false,
      busyWith: false,
      loadingMessage: 'Exportando...',
      filtered: false,
    }
  },
  computed: {
    ...mapGetters('sistema', ['getCurCia']),
    curGrid() {
      return this.$refs[curGridRefKey].instance
    },
    curPeriodText() {
      return this.curPeriod.join(' ~ ')
    },
  },
  created() {
    locale(navigator.language)
  },
  mounted() {},
  activated() {
    if (this.dataSource) {
      const fi = this.$route.query.fechini
      const ff = this.$route.query.fechfin
      const crow = this.$route.query.row
      const prevFiltered = this.filtered
      this.filtered = this.$route.query.filtered

      if (fi && ff && crow) {
        const qryP = [fi, ff]
        const cP = this.curPeriod

        const fields = setFields(crow)
        this.dataSource.fields(fields)

        this.curRow = crow
        this.curPeriod = qryP

        if (!arrayEquals(qryP, cP) || prevFiltered !== this.filtered) {
          this.$fetch()
        } else {
          this.dataSource.load()
        }
      }
    }
  },
  methods: {
    ...mapActions('linabi/pivotsales', ['renewStore']),
    async reloadData(qryP, fields, reload) {
      if (reload) {
        const curparams = {
          p01: 14,
          p02: this.getCurCia.extrel,
          p03: qryP[0],
          p04: qryP[1],
          p05: this.filtered,
        }

        this.loadingMessage = 'Cargando...'

        await this.renewStore(curparams).then((store) => {
          this.dataSource = new PivotGridDataSource({
            store,
            fields,
          })
        })
      } else {
        this.loadingMessage = 'Cargando...'
        this.dataSource.fields(fields)
        this.dataSource.load()
      }
    },
    goBack() {
      this.$router.back()
    },
    clearData() {
      this.dataSource = null
      this.menuFilter = false
    },
    expandAll() {
      this.dataSource.expandAll('FECHA')

      const fields = this.dataSource.fields()
      fields.forEach((obj) => {
        if ('area' in obj) {
          if (obj.area === 'row') {
            this.dataSource.expandAll(obj.dataField)
          }
        }
      })

      this.menuFilter = false
    },
    collapseAll() {
      const rowField = this.$route.query.row
      this.dataSource.collapseAll('FECHA')
      this.dataSource.collapseAll(rowField)
      this.menuFilter = false
    },
    updatePeriod() {
      this.$refs.periodDialog.save(this.curPeriod)
      this.showSetPeriod = false
      this.$fetch()
    },
    onResize() {
      this.tableHeight =
        window.innerHeight -
        this.$refs.resizableDiv.getBoundingClientRect().y -
        100
    },

    exportGrid(opc) {
      const workbook = new ExcelJS.Workbook()
      const worksheet = workbook.addWorksheet('ventas')

      this.menuFilter = false

      this.loadingMessage = 'Exportando...'
      this.busyWith = true
      const rowName = this.curRow

      exportPivotGrid({
        component: this.curGrid,
        worksheet,
      })
        .then(function () {
          if (opc === 'xlsx') {
            workbook.xlsx.writeBuffer().then((buffer) => {
              saveAs(
                new Blob([buffer], { type: 'application/octet-stream' }),
                `Ventas_${rowName}.xlsx`
              )
            })
          } else {
            workbook.csv.writeBuffer().then((buffer) => {
              saveAs(
                new Blob([buffer], { type: 'application/octet-stream' }),
                `Ventas_${rowName}.csv`
              )
            })
          }
        })
        .then(() => (this.busyWith = false))
      // e.cancel = true
    },
  },
  head() {
    return {
      title: 'Ventas - pivot',
    }
  },
}
</script>
