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
      <DxCircularGauge
        id="gauge1"
        :value="value"
        :subvalues="subvalues"
        :title="setTitle"
      >
        <DxScale :start-value="0" :end-value="100" :tick-interval="10">
          <DxTick color="#536878" />
          <DxLabel :indent-from-tick="3" />
        </DxScale>
        <DxTooltip :enabled="true" :customize-tooltip="cusTooltip" />
        <DxRangeContainer :offset="10">
          <DxRange :start-value="0" :end-value="30" color="#92000A" />
          <DxRange :start-value="30" :end-value="70" color="#E6E200" />
          <DxRange :start-value="70" :end-value="100" color="#77DD77" />
        </DxRangeContainer>
        <DxExport :enabled="true" />
      </DxCircularGauge>
    </v-card-text>

    <v-card-actions>
      <v-menu
        ref="dMenu"
        v-model="dateMenu"
        :close-on-content-click="false"
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
        <v-card>
          <v-list>
            <v-list-item>
              <v-menu
                ref="dMenuYear"
                v-model="menuDateYear"
                :close-on-content-click="false"
                transition="scale-transition"
                offset-y
                min-width="auto"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    slot="activator"
                    v-model="fechIni"
                    label="Año de referencia"
                    prepend-icon="mdi-calendar"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker
                  ref="pickerYear"
                  v-model="fechIni"
                  :active-picker.sync="activePickerYear"
                  min="1950-01-01"
                  :max="
                    new Date(
                      Date.now() - new Date().getTimezoneOffset() * 60000
                    )
                      .toISOString()
                      .substr(0, 10)
                  "
                  reactive
                  no-title
                  @input="saveYear"
                ></v-date-picker>
              </v-menu>
            </v-list-item>

            <v-list-item>
              <v-menu
                ref="dMenuFechfin"
                v-model="menuFechfin"
                :close-on-content-click="false"
                :return-value.sync="fechFin"
                transition="scale-transition"
                offset-y
                min-width="auto"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="fechFin"
                    label="Fecha de comparación"
                    prepend-icon="mdi-calendar"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker v-model="fechFin" no-title scrollable>
                  <v-spacer></v-spacer>
                  <v-btn text color="primary" @click="closeMenu">
                    Cancelar
                  </v-btn>
                  <v-btn text color="primary" @click="updatePeriod">
                    Aceptar
                  </v-btn>
                </v-date-picker>
              </v-menu>
            </v-list-item>
          </v-list>
        </v-card>
      </v-menu>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex'
import {
  DxCircularGauge,
  DxScale,
  DxTick,
  DxLabel,
  DxTooltip,
  DxRangeContainer,
  DxRange,
  DxExport,
} from 'devextreme-vue/circular-gauge'

const currentYear = new Date().getFullYear()
const startDate = new Date(currentYear - 1, 0, 2).toISOString().substring(0, 10)
const endDate = new Date().toISOString().substring(0, 10)

export default {
  name: 'VentaRendimiento',

  components: {
    DxCircularGauge,
    DxScale,
    DxTick,
    DxLabel,
    DxTooltip,
    DxRangeContainer,
    DxRange,
    DxExport,
  },
  props: {
    qrySel: {
      type: String,
      required: true,
    },
    gaugeId: {
      type: String,
      default: 'gauge1',
    },
  },

  async fetch() {
    const curparams = {
      p01: this.qrySel,
      p02: this.getCurCia.extrel,
      p03: this.fechIni,
      p04: this.fechFin,
      p05: this.filtered,
    }

    this.loadingView = true

    await this.$axios
      .get('linabi/extbidashboard/', {
        params: curparams,
      })
      .then((response) => {
        this.dataSource = response.data

        const curv = this.dataSource[0].VTOTCUR

        const v1 = this.dataSource[0].VENTAQ
        const v2 = this.dataSource[1].VENTAQ
        const v3 = this.dataSource[2].VENTAQ
        const v4 = this.dataSource[3].VENTAQ

        const markValue = Math.round((curv * 100) / (v1 + v2 + v3 + v4))

        this.value = markValue

        const q1 = this.dataSource[0].PERCENTQ
        const q2 = this.dataSource[1].PERCENTQ
        const q3 = this.dataSource[2].PERCENTQ

        this.subvalues = [q1, q1 + q2, q1 + q2 + q3, 100]

        this.ventasQ = [v1, v1 + v2, v1 + v2 + v3, v1 + v2 + v3 + v4]

        this.loadingView = false
      })
  },

  data() {
    return {
      loadingView: false,
      perms: this.$auth.user.perms,
      subvalues: [],
      value: 0,
      ventasQ: [],
      dataSource: [],
      showLegend: false,
      umbral: 0,
      fechIni: startDate,
      fechFin: endDate,
      dateMenu: false,
      curPeriod: [],
      menuDateYear: false,
      activePickerYear: null,
      menuFechfin: false,
      filtered: false,
    }
  },
  computed: {
    ...mapGetters('sistema', ['getCurCia']),
    setTitle() {
      const refYear = new Date(this.fechIni).getFullYear()
      const title = {
        text: `Desempeño de ventas con respecto a ${refYear}`,
        subtitle: {
          text: `Ventas hasta ${this.fechFin}`,
          font: {
            color: 'gray',
            opacity: 0.9,
          },
        },
      }

      return title
    },
  },
  watch: {
    menuDateYear(val) {
      val && this.$nextTick(() => (this.$refs.pickerYear.activePicker = 'YEAR'))
      // val && setTimeout(() => (this.activePickerYear = 'YEAR'))
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
    refreshData(updateFilter = false) {
      this.filtered = updateFilter
      this.$fetch()
    },
    updatePeriod(up = []) {
      if (up.length > 0) {
        this.fechIni = up[0]
        this.fechFin = up[1]
      }
      // this.$refs.dMenuFechfin.save(this.fechFin)
      this.menuFechfin = false
      this.dateMenu = false
      this.refreshData()
    },
    formatLabel(pointInfo) {
      return `${pointInfo.valueText} (${pointInfo.percentText})`
    },
    cusTooltip(pval) {
      // console.log('POINTVALUE: ', pval)

      let vTxt = `${pval.valueText}% Ref`
      let v = '0.00'

      if (pval.type === 'value-indicator') {
        vTxt = `${pval.valueText}% a la fecha`
        v = Number(this.dataSource[0].VTOTCUR)
      } else {
        vTxt = `${pval.valueText}% Trimestre ${pval.index + 1}`
        v = Number(this.ventasQ[pval.index])
      }

      const vx = v.toLocaleString('en-US', {
        style: 'currency',
        currency: 'USD',
      })

      return {
        html: `<b>${vTxt}</b><br>${vx}`,
      }
    },
    saveYear(date) {
      this.$refs.dMenuYear.save(date)
      this.$refs.pickerYear.activePicker = 'YEAR'
      this.menuDateYear = false
    },
    closeMenu() {
      this.menuFechfin = false
      this.dateMenu = false
    },
  },
}
</script>

<style scoped>
#gauge1 {
  height: 440px;
  width: 100%;
}
</style>
