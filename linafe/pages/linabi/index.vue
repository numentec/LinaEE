<template>
  <v-container fluid>
    <v-row dense align="start">
      <v-col></v-col>
      <v-col></v-col>
      <v-col align="end">
        <v-card outlined max-height="32" class="my-0 py-0">
          <v-card-actions class="my-0 py-0">
            <v-card-text
              v-show="filtered"
              class="text-h6 my-0 py-0 grey--text text--lighten-1"
            >
              Marcas Externas
            </v-card-text>
            <v-spacer></v-spacer>
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  icon
                  color="secondary"
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
              <span>Filtro marca externa</span>
            </v-tooltip>
            <v-menu
              ref="dMenu"
              v-model="dateMenu"
              :close-on-content-click="false"
              :return-value.sync="globalPeriod"
              transition="scale-transition"
              left
              offset-y
              offset-x
              min-width="auto"
            >
              <template v-slot:activator="{ on: menu, attrs }">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on: tooltip }">
                    <v-btn
                      icon
                      v-bind="attrs"
                      color="secondary"
                      class="my-0"
                      v-on="{ ...tooltip, ...menu }"
                    >
                      <v-icon>mdi-calendar-refresh-outline</v-icon>
                    </v-btn>
                  </template>
                  <span>Establecer periodo global</span>
                </v-tooltip>
              </template>
              <v-date-picker
                v-model="globalPeriod"
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
                <v-btn text color="primary" @click="updatePeriod">
                  Aceptar
                </v-btn>
              </v-date-picker>
            </v-menu>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="4">
        <VentaTot
          ref="vtot1"
          card-type="V1"
          card-id="V1"
          card-title="Ventas del año"
          card-color="green"
        />
      </v-col>
      <v-col cols="12" md="4">
        <VentaTot
          ref="vtot2"
          card-type="V2"
          card-id="V2"
          card-title="Costo promedio"
          card-color="blue"
        />
      </v-col>
      <v-col cols="12" md="4">
        <VentaTot
          ref="vtot3"
          card-type="V3"
          card-id="V3"
          card-title="Ventas en proceso"
          card-color="red"
        />
      </v-col>
      <!-- <v-col cols="12" md="6">
        <VentasRecientes />
      </v-col> -->
    </v-row>
    <v-row>
      <v-col cols="12" md="8">
        <VentasPorMes ref="vpmes" arg-field="MES" val-field="VENTA" />
      </v-col>
      <v-col cols="12" md="4">
        <venta-rendimiento ref="vrdto" qry-sel="10" />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="4">
        <VentasPie
          ref="vpie1"
          pie-id="1"
          pie-title="Ventas por Marca"
          pie-palette="Material"
          qry-sel="2"
          arg-field="MARCA"
          val-field="VENTA_TOTAL"
          @goView="goView"
        />
      </v-col>
      <v-col cols="12" md="4">
        <VentasPie
          ref="vpie2"
          pie-id="2"
          pie-title="Ventas por Vendedor"
          pie-palette="Violet"
          qry-sel="4"
          arg-field="VENDEDOR"
          val-field="VENTA_TOTAL"
          @goView="goView"
        />
      </v-col>
      <v-col cols="12" md="4">
        <VentasPie
          ref="vpie3"
          pie-id="3"
          pie-title="Ventas por Cliente"
          pie-palette="Dark Moon"
          qry-sel="6"
          arg-field="CLIENTE"
          val-field="VENTA_TOTAL"
          @goView="goView"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="4">
        <ventas-por-pais ref="vpais" @goView="goView" />
      </v-col>
      <v-col cols="12" md="8">
        <VentaSKU ref="vsku" @goView="goView" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import VentaTot from '../../components/linabi/dashboard/VentaTot.vue'
import VentasPie from '../../components/linabi/dashboard/VentasPie.vue'
import VentasPorPais from '../../components/linabi/dashboard/VentasPorPais.vue'
import VentasPorMes from '../../components/linabi/dashboard/VentasPorMes.vue'
import VentaRendimiento from '../../components/linabi/dashboard/VentaRendimiento.vue'
// import AuxCard from '../../components/linabi/dashboard/AuxCard.vue'
import VentaSKU from '../../components/linabi/dashboard/VentaSKU.vue'
// import VentasRecientes from '../../components/linabi/dashboard/VentasRecientes.vue'

const startDate = new Date(new Date().getFullYear(), 0, 1)
  .toISOString()
  .substring(0, 10)
const endDate = new Date().toISOString().substring(0, 10)

export default {
  components: {
    VentasPorPais,
    VentasPie,
    VentaTot,
    VentasPorMes,
    VentaRendimiento,
    // AuxCard,
    VentaSKU,
    // VentasRecientes,
  },
  data() {
    return {
      page_name: 'BI Dashboard',
      globalPeriod: [startDate, endDate],
      dateMenu: false,
      filtered: false,
    }
  },
  created() {},
  mounted() {},
  methods: {
    goView(obj) {
      this.$router.push({
        path: obj.path,
        query: {
          row: obj.argField,
          fechini: obj.curPeriod[0],
          fechfin: obj.curPeriod[1],
          filtered: obj.filtered,
        },
      })
    },
    upP() {
      this.dateMenu = false
      // this.$refs.dMenuFechfin
      this.$refs.vtot1.updatePeriodExternal(this.globalPeriod)
      this.$refs.vtot2.updatePeriodExternal(this.globalPeriod)
      this.$refs.vtot3.updatePeriodExternal(this.globalPeriod)

      this.$refs.vpie1.updatePeriod(this.globalPeriod)
      this.$refs.vpie2.updatePeriod(this.globalPeriod)
      this.$refs.vpie3.updatePeriod(this.globalPeriod)

      this.$refs.vpmes.updatePeriod(this.globalPeriod)
      this.$refs.vpais.updatePeriod(this.globalPeriod)
      this.$refs.vsku.updatePeriod(this.globalPeriod)
      // this.$refs.vrdto.updatePeriod(this.globalPeriod)
    },
    updatePeriod() {
      setTimeout(this.upP)
    },
    filterMarcaExt() {
      this.dateMenu = false

      this.filtered = !this.filtered

      this.$refs.vtot1.refreshData(this.filtered)
      this.$refs.vtot2.refreshData(this.filtered)
      this.$refs.vtot3.refreshData(this.filtered)

      this.$refs.vpie1.refreshData(this.filtered)
      this.$refs.vpie2.refreshData(this.filtered)
      this.$refs.vpie3.refreshData(this.filtered)

      this.$refs.vpmes.refreshData(this.filtered)
      this.$refs.vpais.refreshData(this.filtered)
      this.$refs.vsku.refreshData(this.filtered)
      this.$refs.vrdto.refreshData(this.filtered)
    },
  },
}
</script>
