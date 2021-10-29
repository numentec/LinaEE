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
          <v-switch v-model="useBC" label="Use Barcode" class="mx-2" />
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
          <v-col cols="12" md="8" class="d-flex justify-center shrink">
            <ImgForGrid :img-file="product.foto" :swidth="200" :lwidth="350" />
          </v-col>
          <v-col cols="12" md="4">
            <v-row justify="start" align="center" dense>
              <v-card-title class="my-0 py-0 px-2">
                {{ product.sku }}
              </v-card-title>
            </v-row>
            <v-row justify="start" align="center" dense>
              <v-card-text class="my-0 pt-0 px-2">
                <div class="text-subtitle-1">
                  {{ product.descrip }}
                </div>
              </v-card-text>
            </v-row>
            <v-row justify="start" align="center">
              <v-chip color="green" text-color="white" class="mb-4 mx-2">
                {{
                  `Precio: ${product.precio.toLocaleString('es-US', {
                    style: 'currency',
                    currency: 'USD',
                  })}`
                }}
              </v-chip>
            </v-row>
            <v-row justify="start" align="center">
              <v-chip color="light-blue" text-color="white" class="mx-2">
                {{ `Disponible: ${product.disponible}` }}
              </v-chip>
            </v-row>
          </v-col>
        </v-row>
      </v-card-text>
      <v-divider class="mx-4"></v-divider>
      <v-list rounded>
        <v-list-item-group v-model="selectedItem" color="primary">
          <v-list-item v-for="(item, i) in stocklist" :key="i">
            <v-list-item-content>
              <v-list-item-title
                v-text="`${item.name}: ${item.cantidad}`"
              ></v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
      <v-row justify="center" align="center">
        <VueBarcode :value="product.barcode" height="50">No barcode</VueBarcode>
      </v-row>
    </v-card>
    <v-snackbar v-model="snackbar" timeout="4000">
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
  barcode: '000000000000',
  descrip: 'PRODUCT',
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
      useBC: false,
      productID: '',
      dataSource: null,
      selectedKeys: [],
      msgReloc: '',
      msgColor: 'secondary',
      snackbar: false,
      product,
      stocklist: [],
      selectedItem: 0,
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
    async qryProd() {
      if (this.productID) {
        const keyType = this.useBC ? 'BC' : 'SKU'
        await this.$axios
          .get('wms/qryoneprod/', {
            params: { p01: this.productID, p02: keyType, p03: '01' },
          })
          .then((response) => {
            if (response.data) {
              if (response.data.length > 0) {
                const curProd = response.data[0]
                this.product.sku = curProd.SKU
                this.product.barcode = curProd.BARCODE
                this.product.descrip = curProd.DESCRIP
                this.product.disponible = curProd.DISPONIBLE
                this.product.precio = curProd.PRECIO
                this.product.foto = this.$config.fotosURL + curProd.FOTO

                this.stocklist = [
                  { name: 'Existencia', cantidad: curProd.EXISTENCIA },
                  { name: 'Reservado', cantidad: curProd.RESERVADO },
                  { name: 'Futuro', cantidad: curProd.FUTURO },
                ]
              } else {
                const prod = {
                  sku: '*SKU*',
                  barcode: '000000000000',
                  descrip: 'PRODUCT',
                  precio: '0',
                  disponible: 'NON',
                  reservado: '0 / 0',
                  stock: '0 / 0',
                  foto: '/no_image.png',
                }
                this.product = Object.assign({}, prod)
                this.stocklist = []
                this.msgReloc = 'No se encontró el producto'
                this.msgColor = 'yellow'
                this.snackbar = true
              }
            }
          })
      }
    },
    onSelectionChanged(e) {},
    onItemClick(e) {},
  },
}
</script>

<style scoped></style>
