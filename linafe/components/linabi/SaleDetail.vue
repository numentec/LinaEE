/* eslint-disable no-console */
<template>
  <client-only>
    <v-dialog
      :value="showSaleDetail"
      persistent
      max-width="1000px"
      min-width="200px"
      @keydown.esc="$emit('hideSaleDetail')"
    >
      <v-card flat tile class="mx-auto">
        <v-app-bar color="accent darken-3" dark flat>
          <v-tooltip bottom>
            <template #activator="{ on, attrs }">
              <v-btn icon v-bind="attrs" v-on="on" @click="$fetch">
                <v-icon>mdi-refresh</v-icon>
              </v-btn>
            </template>
            <span>Refresh</span>
          </v-tooltip>
          <v-tooltip bottom>
            <template #activator="{ on, attrs }">
              <v-toolbar-title v-bind="attrs" v-on="on">
                SKU: {{ skuForSaleDetail }}
              </v-toolbar-title>
            </template>
            <span>{{ getDescription }}</span>
          </v-tooltip>
          <v-spacer />
          <v-tooltip bottom>
            <template #activator="{ on, attrs }">
              <v-btn
                icon
                class="mr-4"
                v-bind="attrs"
                v-on="on"
                @click="clearFilters"
              >
                <v-icon>mdi-filter-variant-remove</v-icon>
              </v-btn>
            </template>
            <span>Clear all filters</span>
          </v-tooltip>
          <v-app-bar-nav-icon @click="$emit('hideSaleDetail')">
            <v-icon>mdi-window-close</v-icon>
          </v-app-bar-nav-icon>
        </v-app-bar>
        <v-container>
          <DxDataGrid
            ref="dataGrid"
            :show-borders="true"
            :remote-operations="false"
            :data-source="dataSource"
            :width="'100%'"
            :height="600"
            :focused-row-enabled="true"
            :column-auto-width="true"
            :row-alternation-enabled="true"
            :show-column-lines="true"
            :show-row-lines="false"
            :hover-state-enabled="true"
          >
            <DxColumn data-field="CLIENTE" caption="Cliente" />
            <DxColumn data-field="NUM_FAC" caption="Nº Factura" />
            <DxColumn
              data-field="FECHA"
              data-type="date"
              format="dd/MM/yyyy"
              caption="Última Venta"
            />
            <DxColumn
              data-field="CANTIDAD"
              data-type="number"
              caption="Cantidad"
            />
            <DxColumn
              data-field="PRECIO"
              data-type="number"
              format="$#,##0.00"
              caption="Precio"
            />
            <DxColumn
              data-field="MONTO"
              data-type="number"
              format="$#,##0.00"
              caption="Monto"
            />
            <DxFilterRow :visible="true" />
            <DxHeaderFilter :visible="true" />
            <DxScrolling mode="virtual" />
            <DxSummary>
              <DxTotalItem
                column="CLIENTE"
                summary-type="count"
                display-format="{0} Regs."
              />
              <DxTotalItem
                column="CANTIDAD"
                summary-type="sum"
                display-format="{0}"
              />
              <DxTotalItem
                column="MONTO"
                summary-type="sum"
                value-format="$#,##0.00"
                display-format="{0}"
              />
            </DxSummary>
          </DxDataGrid>
        </v-container>
      </v-card>
    </v-dialog>
  </client-only>
</template>

<script>
import { mapGetters } from 'vuex'
import DataSource from 'devextreme/data/data_source'
import {
  DxDataGrid,
  DxColumn,
  DxFilterRow,
  DxHeaderFilter,
  DxScrolling,
  DxSummary,
  DxTotalItem,
} from 'devextreme-vue/data-grid'

export default {
  name: 'SaleDetail',

  components: {
    DxDataGrid,
    DxColumn,
    DxFilterRow,
    DxHeaderFilter,
    DxScrolling,
    DxSummary,
    DxTotalItem,
  },

  props: {
    showSaleDetail: {
      type: Boolean,
      default: false,
    },
    skuForSaleDetail: {
      type: String,
      default: '',
    },
  },

  fetch() {
    if (this.showSaleDetail && this.skuForSaleDetail) {
      const curparams = {
        p01: 16,
        p02: this.getCurCia.extrel,
        p03: '2026-01-01',
        p04: '2026-12-31',
        p05: this.skuForSaleDetail,
        rpt: true,
      }

      this.dataSource = new DataSource({
        key: 'ID',
        load: () =>
          this.$axios
            .get('/linabi/rptpivotsales/', { params: curparams })
            .then((response) => {
              this.lastLoadedSku = this.skuForSaleDetail
              return response.data
            })
            .catch(() => []),
      })
    }
  },

  data() {
    return {
      dataSource: [],
      lastLoadedSku: '',
    }
  },
  computed: {
    ...mapGetters('sistema', ['getCurCia']),

    getDescription() {
      if (!this.dataSource) return
      if (this.dataSource.length === 0) return

      // const dataGridInstance = this.$refs.dataGrid.instance
      // const dataSourceInstance = dataGridInstance.getDataSource()

      // const items = dataSourceInstance.items()

      const items = this.dataSource.items()

      if (items && items.length > 0) {
        const item = items[0]
        return item.DESCRIPTION
      }

      return 'Description not available'
    },
  },

  watch: {
    showSaleDetail(newValue) {
      if (!newValue) {
        return
      }

      if (
        this.skuForSaleDetail &&
        this.skuForSaleDetail !== this.lastLoadedSku
      ) {
        this.$fetch()
      }
    },
    skuForSaleDetail(newSku, oldSku) {
      if (!this.showSaleDetail) {
        return
      }

      if (!newSku || newSku === oldSku || newSku === this.lastLoadedSku) {
        return
      }

      this.$fetch()
    },
  },

  mounted() {},

  methods: {
    clearFilters() {
      this.$refs.dataGrid.instance.clearFilter()
    },
  },
}
</script>

<style scoped>
.borderleftonly {
  border-top: solid white !important;
  border-bottom: solid white !important;
  border-right: solid white !important;
}
</style>
