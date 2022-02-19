/* eslint-disable no-console */
<template>
  <v-card
    class="mx-auto my-4"
    style="height: 100%"
    :loading="loadingView"
    color="cyan"
    dark
    @click="goView"
  >
    <v-card-title>Ventas por SKU</v-card-title>
    <v-card-subtitle>{{ curPeriodText }}</v-card-subtitle>
    <v-card-text>
      <DxDataGrid
        :data-source="dataSource"
        :remote-operations="false"
        :allow-column-reordering="true"
        :row-alternation-enabled="true"
        :show-borders="true"
        :focused-row-enabled="true"
        :column-auto-width="true"
        :allow-column-resizing="true"
        column-resizing-mode="widget"
        :show-column-lines="true"
        :show-row-lines="false"
        :hover-state-enabled="true"
      >
        <DxColumn data-field="SKU" data-type="string" />
        <DxColumn
          data-field="DESCRIP"
          data-type="string"
          caption="Descripción"
        />
        <DxColumn
          data-field="T1"
          data-type="number"
          format="#,##0.00"
          alignment="right"
        />
        <DxColumn
          data-field="T2"
          data-type="number"
          format="#,##0.00"
          alignment="right"
        />
        <DxColumn
          data-field="T3"
          data-type="number"
          format="#,##0.00"
          alignment="right"
        />
        <DxColumn
          data-field="T4"
          data-type="number"
          format="#,##0.00"
          alignment="right"
        />
        <DxColumn
          data-field="TOT"
          data-type="number"
          format="#,##0.00"
          alignment="right"
          caption="Total"
        />
        <DxPager
          :allowed-page-sizes="[5, 10, 20]"
          :show-page-size-selector="true"
        />
        <DxPaging :page-size="psize" />
      </DxDataGrid>
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
          <v-btn icon v-bind="attrs" v-on="on">
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
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex'
import {
  DxDataGrid,
  DxColumn,
  DxPager,
  DxPaging,
} from 'devextreme-vue/data-grid'
import DataSource from 'devextreme/data/data_source'

const startDate = new Date(new Date().getFullYear(), 0, 1)
  .toISOString()
  .substring(0, 10)
const endDate = new Date().toISOString().substring(0, 10)

export default {
  name: 'VentaSKU',

  components: {
    DxDataGrid,
    DxColumn,
    DxPager,
    DxPaging,
  },
  props: {},

  async fetch() {
    if (this.curPeriod.length === 1) {
      this.curPeriod.push(this.curPeriod[0])
      this.$refs.dMenu.save(this.curPeriod)
    }

    const curparams = {
      p01: '11',
      p02: this.getCurCia.extrel,
      p03: this.curPeriod[0],
      p04: this.curPeriod[1],
      p05: 100,
    }

    this.loadingView = true

    await this.$axios
      .get('linabi/extbidashboard', {
        params: curparams,
      })
      .then((response) => {
        // this.dataSource = response.data

        this.dataSource = new DataSource({
          store: {
            type: 'array',
            key: 'SKU',
            data: response.data,
          },
        })

        this.loadingView = false
      })
  },

  data() {
    return {
      loadingView: false,
      perms: this.$auth.user.perms,
      dataSource: [],
      umbral: 0,
      curPeriod: [startDate, endDate],
      dateMenu: false,
      psize: 10,
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
    updatePeriod() {
      this.$refs.dMenu.save(this.curPeriod)
      this.refreshData()
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
