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
            `Sales Pivot Table (${curPeriodText})`
          }}</v-toolbar-title>
          <v-spacer />
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                icon
                color="secondary"
                :disabled="isLoading"
                v-bind="attrs"
                class="my-0"
                v-on="on"
                @click.stop="filterMarcaExt"
              >
                <v-icon v-show="filtered" color="error"
                  >mdi-filter-remove-outline</v-icon
                >
                <v-icon v-show="!filtered" color="success"
                  >mdi-filter-check-outline</v-icon
                >
              </v-btn>
            </template>
            <span>{{
              filtered
                ? 'Quitar filtro marca externa'
                : 'Aplicar filtro marca externa'
            }}</span>
          </v-tooltip>
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
                    <v-list-item-title @click.stop="exportGridSchema('xlsx')">
                      Excel con Esquema
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

const setFields = (row, hasPermissions) => {
  return [
    {
      dataField: 'CLIENTE',
      area: 'row',
      sortBySummaryField: 'MONTO',
    },
    {
      dataField: 'FECHA',
      dataType: 'date',
      area: 'column',
    },
    {
      dataField: 'QUANTITY',
      dataType: 'number',
      summaryType: 'sum',
      format: '#,##0.##',
      isMeasure: true,
    },
    {
      dataField: 'MONTO',
      dataType: 'number',
      summaryType: 'sum',
      format: '#,##0.00',
      area: 'data',
      isMeasure: true,
    },
    {
      dataField: 'COSTO',
      dataType: 'number',
      summaryType: 'sum',
      format: '#,##0.00',
      isMeasure: true,
      visible: hasPermissions,
    },
    {
      dataField: 'FOB',
      dataType: 'number',
      summaryType: 'sum',
      format: '#,##0.00',
      isMeasure: true,
      visible: hasPermissions,
    },
    {
      dataField: 'CIF',
      dataType: 'number',
      summaryType: 'sum',
      format: '#,##0.00',
      isMeasure: true,
      visible: hasPermissions,
    },
  ]
}

function uniqByKeepLast(data, key) {
  return [...new Map(data.map((x) => [key(x), x])).values()]
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

      fields = setFields(crow, this.hasPermissions)
      // eslint-disable-next-line no-console
      // console.log(fields)
    }

    if (this.curPeriod.length === 1) {
      this.curPeriod.push(this.curPeriod[0])
      this.$refs.dMenu.save(this.curPeriod)
    }

    const curparams = {
      p01: 15,
      p02: this.getCurCia.extrel,
      p03: this.curPeriod[0],
      p04: this.curPeriod[1],
      p05: this.filtered,
      rpt: true,
    }

    await this.renewStore(curparams).then((store) => {
      this.dataSource = new PivotGridDataSource({
        store,
        fields,
      })
    })
  },

  async asyncData({ $axios, store, error }) {
    const loggedInUser = store.getters.loggedInUser
    const groupList = loggedInUser.ugroups.toString()

    try {
      const [resp0, resp1] = await Promise.all([
        $axios.get('vistas/31/'),
        $axios.get('accviewconf-list/', {
          params: { idvista: '31', groups: groupList },
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
        loggedInUser,
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
      dataSource: null,
      curPeriod: [],
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
    ...mapGetters('linabi/pivotsales', ['isLoading']),
    curGrid() {
      return this.$refs[curGridRefKey].instance
    },
    curRow() {
      return this.$route.query.row
    },
    curPeriodText() {
      return this.curPeriod.join(' ~ ')
    },
    hasPermissions() {
      let perm = false

      const conf = this.viewConf.find((obj) => obj.configkey === 'costo')

      if (conf) {
        if (this.loggedInUser.is_superuser) {
          perm = true
        } else {
          perm = conf.configval1 === '1'

          if (this.curView.checkelperms) {
            const acc = this.filterPerms.find((el) => el.configkey === 'costo')
            if (acc) {
              perm = acc.acceso
            }
          }
        }
      }

      return perm
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

        const fields = setFields(crow, this.hasPermissions)
        this.dataSource.fields(fields)

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
          p01: 15,
          p02: this.getCurCia.extrel,
          p03: qryP[0],
          p04: qryP[1],
          p05: this.filtered,
          rpt: true,
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
      this.menuFilter = false

      this.$store.commit('linabi/pivotsales/SET_LOADING_STATUS')

      this.dataSource.expandAll('FECHA')

      setTimeout(() => {
        const fields = this.dataSource.fields()

        const promises = fields
          .filter((obj) => 'area' in obj && obj.area === 'row')
          .map((obj) => this.dataSource.expandAll(obj.dataField))

        Promise.all(promises).then(() => {
          this.$store.commit('linabi/pivotsales/SET_LOADING_STATUS')
        })
      }, 1)

      // fields.forEach((obj) => {
      //   if ('area' in obj) {
      //     if (obj.area === 'row') {
      //       this.dataSource.expandAll(obj.dataField)
      //     }
      //   }
      // })
      // this.$store.commit('linabi/pivotsales/SET_LOADING_STATUS')
    },
    collapseAll() {
      this.menuFilter = false
      this.dataSource.collapseAll('FECHA')
      const fields = this.dataSource.fields()
      fields.forEach((obj) => {
        if ('area' in obj) {
          if (obj.area === 'row') {
            this.dataSource.collapseAll(obj.dataField)
          }
        }
      })
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
    filterMarcaExt() {
      this.filtered = !this.filtered
      this.menuFilter = false

      this.$fetch()
    },
    exportGrid(opc) {
      const workbook = new ExcelJS.Workbook()
      const worksheet = workbook.addWorksheet('ventas')

      this.menuFilter = false

      this.loadingMessage = 'Exportando...'
      this.busyWith = true

      // Obtener el primer campo del área de filas
      const fields = this.dataSource.fields()
      const rowField = fields.find((field) => field.area === 'row')
      const rowName = rowField ? rowField.dataField : 'ventas'

      exportPivotGrid({
        component: this.curGrid,
        worksheet,
        mergeRowFieldValues: false,
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

    async exportGridSchema(opc) {
      const workbook = new ExcelJS.Workbook()
      const worksheet = workbook.addWorksheet('ventas')

      this.menuFilter = false
      this.loadingMessage = 'Exportando con esquema...'
      this.busyWith = true

      // Obtener el primer campo del área de filas
      const fields = this.dataSource.fields()
      const rowField = fields.find((field) => field.area === 'row')
      const rowName = rowField ? rowField.dataField : 'ventas'

      // Guardar el estado actual de expansión
      const expandedPaths = []
      this.curGrid
        .getDataSource()
        .getAreaFields('row', true)
        .forEach((field) => {
          const expanded = this.dataSource.state().expandedPaths
          if (expanded) {
            expandedPaths.push({
              field: field.dataField,
              paths: [...(expanded[field.dataField] || [])],
            })
          }
        })

      try {
        // Expandir todo temporalmente
        this.$store.commit('linabi/pivotsales/SET_LOADING_STATUS')

        await this.dataSource.expandAll('FECHA')

        const rowFields = fields.filter(
          (obj) => 'area' in obj && obj.area === 'row'
        )
        for (const field of rowFields) {
          await this.dataSource.expandAll(field.dataField)
        }

        this.$store.commit('linabi/pivotsales/SET_LOADING_STATUS')

        // Esperar un momento para que se complete la expansión
        await new Promise((resolve) => setTimeout(resolve, 100))

        // Realizar la exportación
        await exportPivotGrid({
          component: this.curGrid,
          worksheet,
          mergeRowFieldValues: false,
          customizeCell: (options) => {
            const { excelCell, pivotCell } = options

            if (
              pivotCell.area === 'row' &&
              pivotCell.rowPath &&
              pivotCell.rowPath.length > 0
            ) {
              const outlineLevel = pivotCell.rowPath.length - 1

              if (excelCell.row && typeof excelCell.row === 'object') {
                excelCell.row.outlineLevel = outlineLevel
              }
            }
          },
        })

        // Aplicar formato adicional
        worksheet.eachRow((row, rowNumber) => {
          if (rowNumber === 1) return

          let indentLevel = 0
          for (let i = 1; i <= row.cellCount; i++) {
            const cell = row.getCell(i)
            if (
              cell.value === null ||
              cell.value === undefined ||
              cell.value === ''
            ) {
              indentLevel++
            } else {
              break
            }
          }

          if (indentLevel > 0) {
            row.outlineLevel = indentLevel
          }
        })

        // Guardar el archivo
        const buffer = await (opc === 'xlsx'
          ? workbook.xlsx.writeBuffer()
          : workbook.csv.writeBuffer())

        saveAs(
          new Blob([buffer], { type: 'application/octet-stream' }),
          `Ventas_${rowName}_esquema.${opc}`
        )
      } catch (error) {
        console.error('Error al exportar:', error)
      } finally {
        // Restaurar el estado original de expansión
        this.dataSource.collapseAll('FECHA')
        fields.forEach((obj) => {
          if ('area' in obj && obj.area === 'row') {
            this.dataSource.collapseAll(obj.dataField)
          }
        })

        // Restaurar las rutas expandidas originales
        expandedPaths.forEach(({ field, paths }) => {
          paths.forEach((path) => {
            this.dataSource.expandHeaderItem(field, path)
          })
        })

        this.busyWith = false
      }
    },
  },
  head() {
    return {
      title: 'Ventas - pivot',
    }
  },
}
</script>
