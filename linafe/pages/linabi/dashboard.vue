<template>
  <v-container fluid>
    <v-row dense align="start">
      <v-col>
        <v-card flat max-height="32" class="my-0 py-0">
          <v-card-text>
            <p class="text-h4 text--grey">SALES DASHBOARD</p>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col></v-col>
      <v-col align="end">
        <v-card outlined max-height="32" class="my-0 py-0">
          <v-card-actions class="my-0 py-0">
            <v-spacer></v-spacer>
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  icon
                  color="secondary"
                  v-bind="attrs"
                  class="my-0"
                  v-on="on"
                  @click.stop="showLegend = !showLegend"
                >
                  <v-icon>mdi-view-gallery-outline</v-icon>
                </v-btn>
              </template>
              <span>Filtrar por tipo de marca</span>
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
      <v-col cols="12" md="4"> </v-col>
      <v-col cols="12" md="4"> </v-col>
      <v-col cols="12" md="4"> </v-col>
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
      <v-col cols="12" md="8">
        <VentasPorMes ref="vpmes" arg-field="MES" val-field="VENTA" />
      </v-col>
      <v-col cols="12" md="4">
        <venta-rendimiento ref="vrdto" qry-sel="10" />
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
        },
      })
    },
    updatePeriod() {
      this.dateMenu = false

      this.$refs.vtot1.updatePeriod(this.globalPeriod)
      this.$refs.vtot2.updatePeriod(this.globalPeriod)
      this.$refs.vtot3.updatePeriod(this.globalPeriod)

      this.$refs.vpie1.updatePeriod(this.globalPeriod)
      this.$refs.vpie2.updatePeriod(this.globalPeriod)
      this.$refs.vpie3.updatePeriod(this.globalPeriod)

      this.$refs.vpmes.updatePeriod(this.globalPeriod)
      this.$refs.vrdto.updatePeriod(this.globalPeriod)
      this.$refs.vpais.updatePeriod(this.globalPeriod)
      this.$refs.vsku.updatePeriod(this.globalPeriod)
    },
  },
}
</script>
