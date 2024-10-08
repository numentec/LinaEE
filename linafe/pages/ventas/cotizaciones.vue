<template>
  <MaterialCard class="mt-10">
    <template v-slot:heading>
      <v-toolbar dense color="secondary" class="mx-1" dark flat>
        <v-btn dark icon>
          <v-icon>mdi-dots-vertical</v-icon>
        </v-btn>
        <v-spacer />
        <v-toolbar-title>Demo Data</v-toolbar-title>
        <v-spacer />
        <v-btn dark icon @click="showColumnChooser">
          <v-icon>mdi-table-column-plus-after</v-icon>
        </v-btn>
      </v-toolbar>
    </template>
    <DxDataGrid
      :ref="curGridRefKey"
      class="ma-4"
      :data-source="dataSource"
      :remote-operations="false"
      :allow-column-reordering="true"
      :row-alternation-enabled="true"
      :show-borders="true"
      @content-ready="onContentReady"
    >
      <DxColumn :group-index="0" data-field="Product" />
      <DxColumn
        data-field="Amount"
        caption="Sale Amount"
        data-type="number"
        format="currency"
        alignment="right"
      />
      <DxColumn
        :allow-grouping="false"
        data-field="Discount"
        caption="Discount %"
        data-type="number"
        format="percent"
        alignment="right"
        cell-template="discountCellTemplate"
        css-class="bullet"
      />
      <DxColumn data-field="SaleDate" data-type="date" />
      <DxColumn data-field="Region" data-type="string" />
      <DxColumn data-field="Sector" data-type="string" />
      <DxColumn data-field="Channel" data-type="string" />
      <DxColumn :width="150" data-field="Customer" data-type="string" />

      <DxGroupPanel :visible="true" />
      <DxSearchPanel :visible="true" :highlight-case-sensitive="true" />
      <DxColumnChooser mode="select" />
      <DxGrouping :auto-expand-all="false" />
      <DxPager
        :allowed-page-sizes="pageSizes"
        :show-page-size-selector="true"
      />
      <DxPaging :page-size="10" />
      <template #discountCellTemplate="{ data: cellData }">
        <DiscountCell :cell-data="cellData" />
      </template>
    </DxDataGrid>
  </MaterialCard>
</template>
<script>
import {
  DxDataGrid,
  DxColumn,
  DxGrouping,
  DxGroupPanel,
  DxPager,
  DxPaging,
  DxSearchPanel,
  DxColumnChooser,
} from 'devextreme-vue/data-grid'

import DataSource from 'devextreme/data/data_source'
import 'devextreme/data/odata/store'

import DiscountCell from '~/components/core/DiscountCell.vue'

const curGridRefKey = 'my-cur-grid'

let collapsed = false

export default {
  components: {
    DxDataGrid,
    DxColumn,
    DxGrouping,
    DxGroupPanel,
    DxPager,
    DxPaging,
    DxSearchPanel,
    DiscountCell,
    DxColumnChooser,
    MaterialCard: () => import('~/components/core/MaterialCard'),
  },
  data() {
    return {
      curGridRefKey,
      dataSource: new DataSource({
        store: {
          type: 'odata',
          url: 'https://js.devexpress.com/Demos/SalesViewer/odata/DaySaleDtoes',
          beforeSend(request) {
            request.params.startDate = '2018-05-10'
            request.params.endDate = '2018-05-15'
          },
        },
      }),
      pageSizes: [10, 25, 50, 100],
      onContentReady(e) {
        if (!collapsed) {
          e.component.expandRow(['EnviroCare'])
          collapsed = true
        }
      },
    }
  },
  computed: {
    curGrid() {
      return this.$refs[curGridRefKey].instance
    },
  },
  methods: {
    showColumnChooser() {
      this.curGrid.showColumnChooser()
    },
  },
  head() {
    return {
      title: 'Cotizaciones',
    }
  },
}
</script>
