<template>
  <div class="d-flex align-content-start flex-wrap">
    <v-card max-width="600" class="mx-auto">
      <v-card-title>
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn icon v-bind="attrs" v-on="on" @click="$router.back()">
              <v-icon large color="primary">mdi-chevron-left</v-icon>
            </v-btn>
          </template>
          <span>Volver a vista anterior</span>
        </v-tooltip>
        <span>Consultar producto</span>
      </v-card-title>
      <v-card-text>
        <v-row>
          <v-switch v-model="useBC" label="Use Barcode"></v-switch>
        </v-row>
        <v-row>
          <v-col cols="12">
            <v-text-field
              ref="txtProdID"
              v-model="productID"
              :rules="[rules.required]"
              :append-outer-icon="'mdi-send'"
              clearable
              :placeholder="useBC ? 'Barcode de Producto' : 'SKU de Producto'"
              type="text"
              @keydown.enter="qryProd"
              @click:append-outer="qryProd"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="8">
            <v-row justify="center" align="center">
              <v-img
                src="/no_image.png"
                contain
                :max-width="$vuetify.breakpoint.mobile ? 200 : 400"
              ></v-img>
            </v-row>
          </v-col>
          <v-col cols="12" md="4">
            <v-row justify="start" align="center">
              <v-chip color="green" text-color="white" class="mb-4">
                Precio: 45.95
              </v-chip>
            </v-row>
            <v-row justify="start" align="center">
              <v-chip color="light-blue" text-color="white">
                Disponible: 100 / 0
              </v-chip>
            </v-row>
          </v-col>
        </v-row>
      </v-card-text>
      <v-divider class="mx-4"></v-divider>
      <v-card-text>
        <v-row>
          <div>
            <DxList
              ref="locationsList"
              :data-source="dataSource"
              selection-mode="single"
              :selected-item-keys="selectedKeys"
              :hover-state-enabled="true"
              :height="200"
              @selection-changed="onSelectionChanged"
              @item-click="onItemClick"
            >
              <template #item="{ data: item }">
                <div>
                  <div class="ubix-container">
                    <div class="ubix">{{ item.UBIX }}</div>
                    <div class="ubixbc">{{ `${item.UBIXBC}` }}</div>
                  </div>
                  <div class="stock-container">
                    <div class="stock">{{ item.CANT1 }}</div>
                  </div>
                </div>
              </template>
            </DxList>
          </div>
        </v-row>
      </v-card-text>
    </v-card>
    <v-snackbar v-model="snackbar" timeout="2000">
      {{ msgReloc }}
      <template v-slot:action="{ attrs }">
        <v-btn :color="msgColor" text v-bind="attrs" @click="snackbar = false">
          Cerrar
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import DxList from 'devextreme-vue/list'
import DataSource from 'devextreme/data/data_source'

export default {
  components: {
    DxList,
  },
  data() {
    return {
      useBC: true,
      productID: '',
      dataSource: null,
      selectedKeys: [],
      msgReloc: '',
      msgColor: 'secondary',
      snackbar: false,
      rules: {
        required: (v) => !!v || 'Requerido',
        isNumber: (v) =>
          (!isNaN(parseFloat(v)) && parseFloat(v) >= 0) || 'Solo números',
      },
    }
  },
  computed: {},
  mounted() {
    this.$nextTick(() => this.$refs.txtProdID.focus())
  },
  methods: {
    async qryProd() {
      if (this.productID) {
        const keyType = this.useBC ? 'BC' : 'SKU'
        await this.$axios
          .get('wms/qrystockext/', {
            params: { p01: this.productID, p02: keyType, p03: '01' },
          })
          .then((response) => {
            let ds = null
            if (response.data) {
              if (response.data.length > 0) {
                ds = new DataSource({
                  store: {
                    type: 'array',
                    key: 'UBIXBC',
                    data: response.data,
                  },
                  searchExpr: ['UBIXBC', 'UBIX'],
                })
              }
            }

            this.dataSource = ds

            this.$nextTick(() => this.$refs.txtOrigen.focus())
          })
      }
    },
    onSelectionChanged(e) {},
    onItemClick(e) {},
  },
}
</script>

<style scoped></style>
