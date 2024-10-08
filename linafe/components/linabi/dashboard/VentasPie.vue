/* eslint-disable no-console */
<template>
  <v-card
    class="mx-auto my-4"
    width="500"
    style="height: 100%"
    :shaped="false"
    :loading="loadingView"
  >
    <v-card-text>
      <DxPieChart
        id="pieId"
        ref="vpie1"
        :data-source="dataSource"
        :palette="piePalette"
        :title="setTitle"
        @point-click="pointClickHandler($event)"
        @legend-click="legendClickHandler($event)"
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
      <v-spacer></v-spacer>
      <!-- <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            icon
            color="success"
            v-bind="attrs"
            v-on="on"
            @click="dsFilter"
          >
            <v-icon>mdi-test-tube</v-icon>
          </v-btn>
        </template>
        <span>Aplicar filtro</span>
      </v-tooltip> -->
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            icon
            color="success"
            v-bind="attrs"
            v-on="on"
            @click.stop="showLegend = !showLegend"
          >
            <v-icon>mdi-view-gallery-outline</v-icon>
          </v-btn>
        </template>
        <span>Ver leyenda</span>
      </v-tooltip>
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            icon
            color="success"
            v-bind="attrs"
            v-on="on"
            @click.stop="
              $emit('goView', { argField, curPeriod, path, filtered })
            "
          >
            <v-icon>mdi-open-in-new</v-icon>
          </v-btn>
        </template>
        <span>Ir a tabla</span>
      </v-tooltip>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex'
import DataSource from 'devextreme/data/data_source'
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
      p05: this.filtered,
      p06: '1000000',
    }

    this.loadingView = true

    await this.$axios
      .get('linabi/extbidashboard/', {
        params: curparams,
      })
      .then((response) => {
        this.dataSource = new DataSource({
          store: {
            type: 'array',
            key: this.argField,
            data: response.data,
          },
        })
      })
      .then(() => {
        // this.dataSource = response.data
        const dsitems = this.dataSource.items()
        const xumbral = dsitems[10][this.valField]

        this.umbral = xumbral

        this.loadingView = false
      })
  },

  data() {
    return {
      loadingView: false,
      perms: this.$auth.user.perms,
      dataSource: null,
      showLegend: false,
      umbral: 0,
      curPeriod: [startDate, endDate],
      dateMenu: false,
      path: '/linabi/dashboardqueries/pivotsales/',
      filtered: false,
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
    refreshData(updateFilter = false) {
      this.filtered = updateFilter
      this.$fetch()
    },
    updatePeriod(up = []) {
      if (up.length > 0) {
        this.curPeriod[0] = up[0]
        this.curPeriod[1] = up[1]
      }
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
    pointClickHandler(e) {
      this.toggleVisibility(e.target)
    },
    legendClickHandler(e) {
      const arg = e.target
      const item = e.component.getAllSeries()[0].getPointsByArg(arg)[0]

      this.toggleVisibility(item)
    },
    toggleVisibility(item) {
      item.isVisible() ? item.hide() : item.show()
    },
    // dsFilter() {
    //   this.filtered = !this.filtered

    //   const dS = this.dataSource

    //   if (this.filtered) {
    //     dS.filter(['MARCA_EXT', 'contains', 'EXTERNA'])
    //   } else {
    //     dS.filter(null)
    //   }

    //   dS.load()
    // },
  },
}
</script>

<style scoped></style>
