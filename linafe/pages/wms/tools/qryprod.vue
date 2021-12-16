<template>
  <div class="d-flex align-content-start flex-wrap">
    <v-card width="600" class="mx-auto" :loading="loadingView">
      <v-card-title>
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn icon v-bind="attrs" v-on="on" @click="$router.back()">
              <v-icon large color="primary">mdi-chevron-left</v-icon>
            </v-btn>
          </template>
          <span>Volver a vista anterior</span>
        </v-tooltip>
        <span>Ubicación de producto</span>
      </v-card-title>
      <v-card-text>
        <v-row dense>
          <v-switch v-model="useBC" label="Use Barcode" class="mx-2" />
        </v-row>
        <v-row dense>
          <v-col cols="12">
            <v-text-field
              ref="txtProdID"
              v-model="productID"
              :rules="[rules.required]"
              :append-outer-icon="'mdi-send'"
              clearable
              :placeholder="useBC ? 'Barcode de Producto' : 'SKU de Producto'"
              type="text"
              @keydown.enter="findLocations"
              @click:append-outer="findLocations"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row dense>
          <v-col cols="12">
            <v-row justify="start" align="center" dense>
              <v-card-title class="my-0 py-0 px-2">
                {{ `SKU: ${product.sku} (${product.um})` }}
              </v-card-title>
            </v-row>
            <v-row justify="start" align="center" dense>
              <v-card-text class="my-0 pt-0 px-2">
                <div class="text-subtitle-1">
                  {{ product.descrip }}
                </div>
              </v-card-text>
            </v-row>
          </v-col>
        </v-row>
      </v-card-text>
      <template v-for="(item, i) in stocklist">
        <v-card v-if="item.LINALLOW != 'H'" :key="i" tile class="mx-auto mb-2">
          <v-row justify="center" align="center" dense no-gutters>
            <v-btn
              text
              :disabled="item.LINALLOW == 'D'"
              class="mb-0"
              color="primary"
              block
            >
              {{ item.UBIX }}
            </v-btn>
          </v-row>
          <v-row>
            <v-col>
              <v-row justify="center" align="center" dense no-gutters>
                <div
                  class="text-caption font-weight-medium"
                  v-text="$vuetify.breakpoint.mobile ? 'EXI' : 'EXISTENCIA'"
                ></div>
              </v-row>
              <v-row justify="center" align="center" no-gutters>
                <div v-text="item.CANT1"></div>
              </v-row>
              <v-row justify="center" align="center" no-gutters>
                <div v-text="item.BULTOS_FISICO"></div>
              </v-row>
            </v-col>
            <v-col>
              <v-row justify="center" align="center" dense no-gutters>
                <div
                  class="text-caption font-weight-medium"
                  v-text="$vuetify.breakpoint.mobile ? 'RES' : 'RESERVADO'"
                ></div>
              </v-row>
              <v-row justify="center" align="center" no-gutters>
                <div v-text="item.CANT2"></div>
              </v-row>
              <v-row justify="center" align="center" no-gutters>
                <div v-text="item.BULTOS_RESERVA"></div>
              </v-row>
            </v-col>
            <v-col>
              <v-row justify="center" align="center" dense no-gutters>
                <div
                  class="text-caption font-weight-medium"
                  v-text="$vuetify.breakpoint.mobile ? 'DIS' : 'DISPONIBLE'"
                ></div>
              </v-row>
              <v-row justify="center" align="center" no-gutters>
                <div v-text="item.CANT3"></div>
              </v-row>
              <v-row justify="center" align="center" no-gutters>
                <div v-text="item.BULTOS_DISPONIBLE"></div>
              </v-row>
            </v-col>
          </v-row>
        </v-card>
      </template>
      <v-row justify="center" align="center">
        <VueBarcode :value="product.barcode" height="50">No barcode</VueBarcode>
      </v-row>
      <v-card-actions>
        <v-card-text>Ver imagen</v-card-text>
        <v-spacer></v-spacer>
        <v-btn icon @click.stop="showImg = !showImg">
          <v-icon>{{ showImg ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
        </v-btn>
      </v-card-actions>
      <v-expand-transition>
        <div v-show="showImg">
          <v-divider></v-divider>
          <v-row justify="center" align="center">
            <v-col class="shrink">
              <ImgForGrid
                :img-file="product.foto"
                :swidth="200"
                :lwidth="350"
              />
            </v-col>
          </v-row>
        </div>
      </v-expand-transition>
    </v-card>
    <v-snackbar v-model="snackbar" timeout="3000">
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
import VueBarcode from 'vue-barcode'
import ImgForGrid from '~/components/utilities/ImgForGrid'

const product = {
  sku: '*****',
  barcode: '0000000000000',
  descrip: 'PRODUCT',
  um: 'UNI',
  precio: '0',
  disponible: 'NON',
  reservado: '0 / 0',
  stock: '0 / 0',
  foto: '/no_image.png',
}

export default {
  components: {
    VueBarcode,
    ImgForGrid,
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
      product: Object.assign({}, product),
      stocklist: [],
      selectedItem: 0,
      showImg: false,
      loadingView: false,
      rules: {
        required: (v) => !!v || 'Requerido',
      },
    }
  },
  computed: {},
  mounted() {
    this.$nextTick(() => this.$refs.txtProdID.focus())
  },
  methods: {
    async findLocations() {
      if (this.productID) {
        this.loadingView = true
        const keyType = this.useBC ? 'BC' : 'SKU'
        await this.$axios
          .get('wms/qrystockext/', {
            params: { p01: this.productID, p02: keyType, p03: '01', p04: 'T' },
          })
          .then((response) => {
            if (response.data) {
              if (response.data.length > 0) {
                const curProd = response.data[0]
                this.product.sku = curProd.SKU
                this.product.barcode = curProd.BARCODE
                this.product.descrip = curProd.DESCRIP
                this.product.um = curProd.UM
                this.product.disponible = 'NON'
                this.product.precio = 0
                this.product.foto = this.$config.fotosURL + curProd.FOTO

                this.stocklist = response.data
              } else {
                this.product = Object.assign({}, product)
                this.stocklist = []
                this.msgReloc = 'Producto no disponible'
                this.msgColor = 'yellow'
                this.snackbar = true
              }
            }
            this.loadingView = false
          })
      }
    },
  },
}
</script>

<style scoped></style>
