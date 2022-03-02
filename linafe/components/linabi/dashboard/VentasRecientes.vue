/* eslint-disable no-console */
<template>
  <v-card class="mx-auto my-4 card-with-border" :loading="loadingView" outlined>
    <v-app-bar flat dense>
      <v-toolbar-title class="text-h6 text--secondary pl-0">
        Ventas más recientes
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            icon
            color="orange darken-3"
            v-bind="attrs"
            v-on="on"
            @click="refreshData"
          >
            <v-icon>mdi-table-refresh</v-icon>
          </v-btn>
        </template>
        <span>Actualizar</span>
      </v-tooltip>
    </v-app-bar>
    <v-divider />
    <v-card-text>
      <DxDataGrid
        id="dgrid"
        :data-source="dataSource"
        :remote-operations="false"
        :allow-column-reordering="true"
        :row-alternation-enabled="true"
        :focused-row-enabled="true"
        :column-auto-width="true"
        :allow-column-resizing="true"
        column-resizing-mode="widget"
        :show-column-lines="true"
        :show-row-lines="false"
        :hover-state-enabled="true"
        :height="150"
      >
        <DxColumn data-field="SKU" data-type="string" />
        <DxColumn
          data-field="DESCRIP"
          data-type="string"
          caption="Descripción"
        />
        <DxColumn data-field="CANTIDAD" data-type="string" />
        <DxColumn
          data-field="MONTO"
          data-type="number"
          format="#,##0.00"
          alignment="right"
        />
        <DxColumn data-field="NOMCLI" data-type="string" />
        <DxColumn data-field="VENDEDOR" data-type="string" />
        <DxColumn data-field="IDDOC" data-type="string" />
        <DxColumn data-field="FECHA" data-type="date" format="dd/MM/yyyy" />
        <DxScrolling mode="virtual" />
      </DxDataGrid>
    </v-card-text>
    <v-overlay :absolute="true" :value="$fetchState.pending">
      <v-progress-circular indeterminate size="64"></v-progress-circular>
    </v-overlay>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex'
import { DxDataGrid, DxColumn, DxScrolling } from 'devextreme-vue/data-grid'
import DataSource from 'devextreme/data/data_source'

const startDate = new Date(new Date().getFullYear(), 0, 1)
  .toISOString()
  .substring(0, 10)
const endDate = new Date().toISOString().substring(0, 10)

export default {
  name: 'VentasRecientes',

  components: {
    DxDataGrid,
    DxColumn,
    DxScrolling,
  },
  props: {},

  async fetch() {
    const curparams = {
      p01: 13,
      p02: this.getCurCia.extrel,
      p03: this.curPeriod[0],
      p04: this.curPeriod[1],
      p05: 12,
    }

    this.loadingView = true

    const res = await this.$axios
      .get('linabi/extbidashboard/', {
        params: curparams,
      })
      .then((response) => {
        this.loadingView = false
        return response
      })

    this.dataSource = new DataSource({
      store: {
        type: 'array',
        key: 'ID',
        data: res.data,
      },
    })
  },

  data() {
    return {
      loadingView: false,
      perms: this.$auth.user.perms,
      dataSource: null,
      curPeriod: [startDate, endDate],
      psize: 3,
    }
  },
  computed: {
    ...mapGetters('sistema', ['getCurCia']),
  },
  mounted() {},
  activated() {
    this.loadingView = false
  },
  methods: {
    refreshData() {
      this.$fetch()
    },
  },
}
</script>

<style scoped>
.card-with-border {
  border-style: solid;
  border-width: 2px;
  border-color: orangered;
}
</style>
