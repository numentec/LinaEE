/* eslint-disable no-console */
<template>
  <v-card
    class="mx-auto my-4"
    width="500"
    style="height: 100%"
    :shaped="false"
    :loading="loadingView"
    @click="goView"
  >
    <v-card-text>
      <DxPieChart
        id="pieId"
        :data-source="dataSource"
        :palette="piePalette"
        :title="setTitle"
      >
        <DxSeries :argument-field="argField" :value-field="valField">
          <DxLabel :visible="false" :customize-text="formatLabel">
            <DxConnector :visible="true" :width="1" />
          </DxLabel>
          <DxSmallValuesGrouping
            :threshold="umbral"
            mode="smallValueThreshold"
          />
        </DxSeries>
        <DxTooltip :enabled="true" :customize-tooltip="cusTooltip" />
        <DxLegend
          :visible="showLegend"
          :row-count="4"
          vertical-alignment="bottom"
          horizontal-alignment="center"
          item-text-position="right"
        />
        <DxExport :enabled="true" />
      </DxPieChart>
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
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" color="success" v-on="on">
            <v-icon>mdi-calendar-refresh-outline</v-icon>
          </v-btn>
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
      <v-spacer></v-spacer>
      <v-btn icon color="success" @click.stop="showLegend = !showLegend">
        <v-icon>mdi-view-gallery-outline</v-icon>
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex'
import DxPieChart, {
  DxSeries,
  DxLabel,
  DxLegend,
  DxConnector,
  DxExport,
  DxSmallValuesGrouping,
  DxTooltip,
} from 'devextreme-vue/pie-chart'

const startDate = new Date(new Date().getFullYear(), 0, 1)
  .toISOString()
  .substring(0, 10)
const endDate = new Date().toISOString().substring(0, 10)

export default {
  name: 'VentasPie',

  components: {
    DxPieChart,
    DxSeries,
    DxLabel,
    DxLegend,
    DxConnector,
    DxExport,
    DxSmallValuesGrouping,
    DxTooltip,
  },
  props: {
    cardType: {
      type: String,
      default: 'chart',
    },
    qrySel: {
      type: String,
      required: true,
    },
    pieId: {
      type: String,
      default: 'pie1',
    },
    pieTitle: {
      type: String,
      default: 'Pie Chart',
    },
    piePalette: {
      type: String,
      default: 'Bright',
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
      p01: this.qrySel,
      p02: this.getCurCia.extrel,
      p03: this.curPeriod[0],
      p04: this.curPeriod[1],
      p05: '1000000',
    }

    this.loadingView = true

    await this.$axios
      .get('linabi/extbidashboard', {
        params: curparams,
      })
      .then((response) => {
        this.dataSource = response.data

        const xumbral = this.dataSource[10][this.valField]

        this.umbral = xumbral

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
        text: this.pieTitle,
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
    goView() {
      // this.loadingView = true
      // this.$router.push(this.el.link)
    },
    refreshData() {
      this.$fetch()
    },
    updatePeriod() {
      this.$refs.dMenu.save(this.curPeriod)
      this.refreshData()
    },
    cusTooltip(pointInfo) {
      const aT = pointInfo.argumentText
      const pT = pointInfo.percentText
      return {
        html: `<b>${aT}</b><br>${pT}`,
      }
    },
    formatLabel(pointInfo) {
      return `${pointInfo.valueText} (${pointInfo.percentText})`
    },
  },
}
</script>

<style scoped></style>
