/* eslint-disable no-console */
<template>
  <div>
    <h4>{{ curVariant.title }}</h4>
    <DxDataGrid :data-source="dataSource" :show-borders="true">
      <DxColumn :data-field="curVariant.data_field" :width="100" />
      <!-- <DxColumn data-field="BARCODE" /> -->
      <DxColumn
        data-field="BARCODE"
        cell-template="bcTemplate"
        :width="250"
        alignment="center"
      />
      <template #bcTemplate="{ data }">
        <VueBarcode :value="data.key" height="50"> No barcode </VueBarcode>
      </template>
    </DxDataGrid>
  </div>
</template>

<script>
import { DxDataGrid, DxColumn } from 'devextreme-vue/data-grid'
import CustomStore from 'devextreme/data/custom_store'
import VueBarcode from 'vue-barcode'

export default {
  components: { DxDataGrid, DxColumn, VueBarcode },
  props: {
    variantData: {
      type: String,
      default: '',
    },
    curVariant: {
      type: Object,
      default: () => {},
    },
  },
  computed: {
    dataSource() {
      const sku = this.variantData

      const store = this.fetchVariants(sku)

      return store
    },
  },
  methods: {
    fetchVariants(sku) {
      const endpoint = this.curVariant.endpoint
      const ax = this.$axios

      async function load() {
        return await ax
          .get(endpoint, {
            params: { sku },
          })
          .then((response) => response.data)
      }

      const store = new CustomStore({ key: 'BARCODE', load })

      return store
    },
  },
}
</script>

<style lang="scss" scoped></style>
