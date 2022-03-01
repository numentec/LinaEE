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
            `Ventas por ${getRow} (${curPeriodText})`
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
    </MaterialCard>
    <LoadingView :busy-with="busyWith" :message="loadingMessage" />
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

const startDate = new Date(new Date().getFullYear(), 0, 1)
  .toISOString()
  .substring(0, 10)
const endDate = new Date().toISOString().substring(0, 10)

const arrayEquals = (a, b) => {
  return a.length === b.length && a.every((v, i) => v === b[i])
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
    // if (this.getPeriod) {
    //   this.curPeriod = this.getPeriod
    // }

    if (this.curPeriod.length === 1) {
      this.curPeriod.push(this.curPeriod[0])
      this.$refs.dMenu.save(this.curPeriod)
    }

    const curparams = {
      p01: 14,
      p02: this.getCurCia.extrel,
      p03: this.curPeriod[0],
      p04: this.curPeriod[1],
    }

    // const row = this.getRow

    this.loadingMessage = 'Cargando...'
    this.busyWith = true

    await this.renewStore(curparams).then((store) => {
      this.dataSource = new PivotGridDataSource({
        store,
        fields: [
          {
            dataField: this.getRow,
            area: 'row',
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
          },
        ],
      })

      this.busyWith = false
    })
  },
  data() {
    return {
      curGridRefKey,
      dataSource: null,
      curPeriod: [startDate, endDate],
      setPeriod: false,
      menuFilter: false,
      showSetPeriod: false,
      tableHeight: 0,
      snackbar: false,
      busyWith: false,
      loadingMessage: 'Exportando...',
    }
  },
  computed: {
    ...mapGetters('sistema', ['getCurCia']),
    ...mapGetters('linabi/pivotsales', ['getRow', 'getPeriod']),
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
      this.dataSource.fields([
        {
          dataField: this.getRow,
          area: 'row',
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
        },
      ])

      let fetchCalled = false
      const gP = this.getPeriod
      const cP = this.curPeriod

      if (gP.length > 0) {
        if (!arrayEquals(gP, cP)) {
          this.curPeriod = [...gP]
          fetchCalled = true
          this.$fetch()
        }
      }

      if (!fetchCalled) {
        this.dataSource.load()
      }
    }
  },
  methods: {
    ...mapActions('linabi/pivotsales', ['renewStore']),
    goBack() {
      this.$router.back()
    },
    clearData() {
      this.dataSource = null
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
      const rowName = this.getRow

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
