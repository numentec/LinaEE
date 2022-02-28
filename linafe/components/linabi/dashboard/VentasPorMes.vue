/* eslint-disable no-console */
<template>
  <v-card
    class="mx-auto my-4"
    style="height: 100%"
    :loading="loadingView"
    @click="goView"
  >
    <v-card-text>
      <DxChart
        id="chart"
        :data-source="dataSource"
        palette="Harmony Light"
        :title="setTitle"
      >
        <DxCommonSeriesSettings :argument-field="argField" />
        <DxSeries
          name="Venta del mes"
          :value-field="valField"
          axis="venta"
          type="bar"
          color="#fac29a"
        />
        <DxSeries
          name="Porcentaje acumulado"
          value-field="cumulativePercentage"
          axis="percentage"
          type="spline"
          color="#6b71c3"
        />

        <DxArgumentAxis>
          <DxLabel :customize-text="cusLabel" overlapping-behavior="stagger" />
        </DxArgumentAxis>

        <DxValueAxis :tick-interval="300" name="venta" position="left" />
        <DxValueAxis
          :tick-interval="20"
          :show-zero="true"
          :value-margins-enabled="false"
          name="percentage"
          position="right"
        >
          <DxLabel :customize-text="customizePercentageText" />
        </DxValueAxis>

        <DxTooltip
          :id="1"
          :enabled="true"
          :shared="true"
          :customize-tooltip="customizeTooltip"
        />

        <DxExport :enabled="true" />

        <DxLegend vertical-alignment="top" horizontal-alignment="center" />
      </DxChart>
    </v-card-text>

    <v-card-actions>
      <v-menu
        ref="dMenu"
        v-model="dateMenu"
        :close-on-content-click="false"
        :return-value.sync="curPeriod"
        transition="scale-transition"
        offset-x
        offset-y
        min-width="auto"
      >
        <template v-slot:activator="{ on: menu, attrs }">
          <v-tooltip bottom>
            <template v-slot:activator="{ on: tooltip }">
              <v-btn
                icon
                v-bind="attrs"
                color="success"
                v-on="{ ...tooltip, ...menu }"
              >
                <v-icon>mdi-calendar-refresh-outline</v-icon>
              </v-btn>
            </template>
            <span>Establecer periodo</span>
          </v-tooltip>
        </template>
        <v-date-picker
          v-model="curPeriod"
          range
          no-title
          scrollable
          locale="es-pa"
          color="blue lighten-1"
        >
          <v-spacer></v-spacer>
          <v-btn text color="primary" @click="dateMenu = false">
            Cancelar
          </v-btn>
          <v-btn text color="primary" @click="updatePeriod"> Aceptar </v-btn>
        </v-date-picker>
      </v-menu>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex'
import DxChart, {
  DxArgumentAxis,
  DxCommonSeriesSettings,
  DxLabel,
  DxLegend,
  DxSeries,
  DxTooltip,
  DxValueAxis,
  DxExport,
} from 'devextreme-vue/chart'

const startDate = new Date(new Date().getFullYear(), 0, 1)
  .toISOString()
  .substring(0, 10)
const endDate = new Date().toISOString().substring(0, 10)

export default {
  name: 'VentasPorMes',

  components: {
    DxChart,
    DxArgumentAxis,
    DxCommonSeriesSettings,
    DxLabel,
    DxLegend,
    DxSeries,
    DxTooltip,
    DxValueAxis,
    DxExport,
  },
  props: {
    cardType: {
      type: String,
      default: 'chart',
    },
    argField: {
      type: String,
      required: true,
    },
    valField: {
      type: String,
      required: true,
    },
  },

  async fetch() {
    if (this.curPeriod.length === 1) {
      this.curPeriod.push(this.curPeriod[0])
      this.$refs.dMenu.save(this.curPeriod)
    }

    const curparams = {
      p01: '1',
      p02: this.getCurCia.extrel,
      p03: this.curPeriod[0],
      p04: this.curPeriod[1],
    }

    this.loadingView = true

    await this.$axios
      .get('linabi/extbidashboard', {
        params: curparams,
      })
      .then((response) => {
        // const data = complaintsData.sort((a, b) => b.count - a.count)
        const data = response.data
        const totalCount = data.reduce(
          (prevValue, item) => prevValue + item.VENTA,
          0
        )
        let cumulativeCount = 0

        const dataSource = data.map((item) => {
          cumulativeCount += item.VENTA
          return {
            MES: item.MES,
            VENTA: item.VENTA,
            cumulativePercentage: Math.round(
              (cumulativeCount * 100) / totalCount
            ),
            percent: Math.round((item.VENTA * 100) / totalCount),
          }
        })
        // ******************************************
        this.dataSource = dataSource

        // const xumbral = this.dataSource[10][this.valField]

        // this.umbral = xumbral

        this.loadingView = false
      })
  },

  data() {
    return {
      loadingView: false,
      perms: this.$auth.user.perms,
      dataSource: [],
      showLegend: false,
      umbral: 0,
      curPeriod: [startDate, endDate],
      dateMenu: false,
    }
  },
  computed: {
    ...mapGetters('sistema', ['getCurCia']),
    curPeriodText() {
      return this.curPeriod.join(' ~ ')
    },
    setTitle() {
      const title = {
        text: 'Ventas por mes',
        subtitle: {
          text: this.curPeriodText,
          font: {
            color: 'gray',
            opacity: 0.9,
          },
        },
      }

      return title
    },
  },
  activated() {
    this.loadingView = false
  },
  methods: {
    goView() {},
    refreshData() {
      this.$fetch()
    },
    formatLabel(pointInfo) {
      return `${pointInfo.valueText} (${pointInfo.percentText})`
    },
    updatePeriod() {
      this.$refs.dMenu.save(this.curPeriod)
      this.refreshData()
    },
    customizePercentageText({ valueText }) {
      return `${valueText}%`
    },
    customizeTooltip(pointInfo) {
      const argText = new Date(pointInfo.argumentText)
      let aT = argText.toLocaleString('default', { month: 'long' })
      aT = aT.toUpperCase()
      const sN0 = pointInfo.points[0].seriesName
      const vT0 = Number(pointInfo.points[0].valueText)
      const vT0x = vT0.toLocaleString('en-US', {
        style: 'currency',
        currency: 'USD',
      })

      let sN1 = pointInfo.points[1].seriesName
      let vT1 = pointInfo.points[1].valueText

      if (pointInfo.seriesName === 'Venta del mes') {
        sN1 = 'Aporte a ventas'
        vT1 = pointInfo.point.data.percent
      }

      // console.log('FECHA', aT)
      return {
        // html: `<b>${pointInfo.argumentText}</b><br>${pointInfo.valueText}%`,
        html: `<b>${aT}</b><br>${sN0}: ${vT0x}<br>${sN1}: ${vT1}%`,
      }
    },
    cusLabel(lbl) {
      return lbl.valueText.substring(0, 7)
    },
  },
}
</script>

<style scoped>
.tooltip-header {
  margin-bottom: 5px;
  font-size: 16px;
  font-weight: 500;
  padding-bottom: 5px;
  border-bottom: 1px solid #c5c5c5;
}

.tooltip-body {
  width: 170px;
}

.tooltip-body .series-name {
  font-weight: normal;
  opacity: 0.6;
  display: inline-block;
  line-height: 1.5;
  padding-right: 10px;
  width: 126px;
}

.tooltip-body .value-text {
  display: inline-block;
  line-height: 1.5;
  width: 30px;
}
</style>
