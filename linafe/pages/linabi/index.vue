<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12" md="3">
        <venta-tot
          card-type="V1"
          card-id="V1"
          card-title="Ventas del año"
          card-color="green"
        />
      </v-col>
      <v-col cols="12" md="3">
        <venta-tot
          card-type="V2"
          card-id="V2"
          card-title="Ventas en proceso"
          card-color="blue"
        />
      </v-col>
      <v-col cols="12" md="6">
        <AuxCard card-color="orange" card-title="Últimas ventas" />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="8">
        <ventas-por-mes arg-field="MES" val-field="VENTA" />
      </v-col>
      <v-col cols="12" md="4">
        <venta-rendimiento qry-sel="10" />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="4">
        <ventas-pie
          pie-id="1"
          pie-title="Ventas por Marca"
          pie-palette="Material"
          qry-sel="2"
          arg-field="MARCA"
          val-field="VENTA_TOTAL"
        />
      </v-col>
      <v-col cols="12" md="4">
        <ventas-pie
          pie-id="2"
          pie-title="Ventas por Vendedor"
          pie-palette="Violet"
          qry-sel="4"
          arg-field="VENDEDOR"
          val-field="VENTA_TOTAL"
        />
      </v-col>
      <v-col cols="12" md="4">
        <ventas-pie
          pie-id="3"
          pie-title="Ventas por Cliente"
          pie-palette="Dark Moon"
          qry-sel="6"
          arg-field="NOMCLI"
          val-field="VENTA_TOTAL"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="4">
        <ventas-por-pais />
      </v-col>
      <v-col cols="12" md="8">
        <VentaSKU />
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
import AuxCard from '../../components/linabi/dashboard/AuxCard.vue'
import VentaSKU from '../../components/linabi/dashboard/VentaSKU.vue'

export default {
  components: {
    VentasPorPais,
    VentasPie,
    VentaTot,
    VentasPorMes,
    VentaRendimiento,
    AuxCard,
    VentaSKU,
  },
  data() {
    return {
      page_name: 'BI Dashboard',
    }
  },
  created() {},
}
</script>
