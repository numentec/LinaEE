/* eslint-disable no-console */
<template>
  <v-card
    class="mx-auto my-4"
    width="600"
    style="height: 100%"
    :shaped="false"
    :loading="loadingView"
  >
    <v-card-text>
      <DxVectorMap
        id="vector-map"
        :bounds="bounds"
        :center="[-79.9, 9.3]"
        :zoom-factor="5"
        theme="material.purple.light"
      >
        <DxLayer :data-source="mapsWorld" name="areas" />
        <DxLayer
          :data-source="markers"
          :min-size="20"
          :max-size="40"
          :opacity="0.8"
          name="bubbles"
          element-type="bubble"
          data-field="value"
        />
        <DxTitle text="Ventas por País">
          <DxSubtitle :text="curPeriodText" />
        </DxTitle>
        <DxTooltip :enabled="true" :customize-tooltip="customizeTooltip" />
        <DxExport :enabled="true" />
      </DxVectorMap>
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
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            icon
            color="success"
            v-bind="attrs"
            v-on="on"
            @click.stop="$emit('goView', { argField: 'PAIS', curPeriod })"
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
import * as mapsData from 'devextreme/dist/js/vectormap-data/world.js'
import {
  DxVectorMap,
  DxLayer,
  DxSubtitle,
  DxTitle,
  DxTooltip,
  DxExport,
} from 'devextreme-vue/vector-map'

const typeOpc = {
  map: {
    icon: 'mdi-text-search',
  },
  chart: {
    icon: 'mdi-file-chart-outline',
  },
  table: {
    icon: 'mdi-tools',
  },
}

const startDate = new Date(new Date().getFullYear(), 0, 1)
  .toISOString()
  .substring(0, 10)
const endDate = new Date().toISOString().substring(0, 10)

export default {
  name: 'VentasPorPais',

  components: {
    DxVectorMap,
    DxLayer,
    DxSubtitle,
    DxTitle,
    DxTooltip,
    DxExport,
  },
  props: {
    cardType: {
      type: String,
      default: 'chart',
    },
  },

  async fetch() {
    if (this.curPeriod.length === 1) {
      this.curPeriod.push(this.curPeriod[0])
      this.$refs.dMenu.save(this.curPeriod)
    }

    const curparams = {
      p01: '3',
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
        this.markers = {
          type: 'FeatureCollection',
          features: response.data.map((data) => ({
            type: 'Feature',
            geometry: {
              type: 'Point',
              coordinates: data.COORD.split(',').map(Number),
            },
            properties: {
              text: data.PAIS,
              value: data.VENTA,
              tooltip: `<b>${data.PAIS}</b>\n${data.VENTA.toLocaleString(
                'en-US',
                {
                  style: 'currency',
                  currency: 'USD',
                }
              )}`,
            },
          })),
        }
        this.loadingView = false
      })
  },

  data() {
    return {
      mapsWorld: mapsData.world,
      bounds: [-180, 85, 180, -60],
      markers: {},
      descrip: false,
      loadingView: false,
      perms: this.$auth.user.perms,
      typeOpc,
      curPeriod: [startDate, endDate],
      dateMenu: false,
    }
  },
  computed: {
    ...mapGetters('sistema', ['getCurCia']),
    curPeriodText() {
      // const fini = new Date(this.curPeriod[0] + 'T00:00:00').toLocaleDateString(
      //   'es-es'
      // )
      // const ffin = new Date(this.curPeriod[1] + 'T00:00:00').toLocaleDateString(
      //   'es-es'
      // )

      // return fini + ' ~ ' + ffin
      return this.curPeriod.join(' ~ ')
    },
  },
  activated() {
    this.loadingView = false
  },
  methods: {
    customizeTooltip(info) {
      if (info.layer.type === 'marker') {
        return { text: info.attribute('tooltip') }
      }
      return null
    },
    refreshData() {
      this.$fetch()
    },
    updatePeriod() {
      this.$refs.dMenu.save(this.curPeriod)
      this.refreshData()
    },
  },
}
</script>

<style scoped>
#vector-map {
  height: 520px;
}
</style>
