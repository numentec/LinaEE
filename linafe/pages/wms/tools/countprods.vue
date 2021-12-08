<template>
  <div class="d-flex align-content-start flex-wrap">
    <v-card width="600" class="mx-auto">
      <v-card-title>
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn icon v-bind="attrs" v-on="on" @click="$router.back()">
              <v-icon large color="primary">mdi-chevron-left</v-icon>
            </v-btn>
          </template>
          <span>Volver a vista anterior</span>
        </v-tooltip>
        <span>Conteo físico</span>
      </v-card-title>
      <v-card-text>
        <v-row dense>
          <v-col cols="3">
            <v-switch v-model="useBC1" label="BC" class="mx-2" />
          </v-col>
          <v-col cols="9">
            <v-text-field
              ref="txtUbicacionID"
              v-model="ubicacionID"
              :rules="[rules.required]"
              :append-outer-icon="'mdi-send'"
              clearable
              placeholder="Ubicación"
              type="text"
              class="mx-2"
              @keydown.enter="findLocations"
              @click:append-outer="findLocations"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row dense>
          <v-col cols="3">
            <v-switch v-model="useBC2" label="BC" class="mx-2" />
          </v-col>
          <v-col cols="9">
            <v-text-field
              ref="txtProdID"
              v-model="productID"
              :append-outer-icon="'mdi-send'"
              clearable
              placeholder="Producto"
              type="text"
              class="mx-2"
              @keydown.enter="findLocations"
              @click:append-outer="findLocations"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="4" class="d-flex justify-center shrink">
            <ImgForGrid :img-file="product.foto" :swidth="100" :lwidth="200" />
          </v-col>
          <v-col cols="8">
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
            <v-row justify="start" align="center" dense>
              <v-card-title class="my-0 py-0 px-2">
                {{ product.barcode }}
              </v-card-title>
            </v-row>
            <v-row justify="start" align="center">
              <v-chip color="light-blue" text-color="white" class="mx-2">
                {{ `Físico: ${product.disponible}` }}
              </v-chip>
            </v-row>
          </v-col>
        </v-row>
        <v-divider></v-divider>
        <v-row justify="space-around" align="center" dense>
          <v-col cols="3" class="d-flex justify-center shrink">
            <v-btn
              class="ma-2"
              outlined
              fab
              small
              color="primary"
              @click="countProds('plus')"
            >
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </v-col>
          <v-col cols="6" class="d-flex justify-center shrink">
            <v-text-field
              ref="txtCurCount"
              v-model="curCount"
              placeholder="Cuenta"
              type="text"
              class="centered-input"
              :prepend-inner-icon="cE ? 'mdi-map-marker' : null"
              :append-icon="!cE ? 'mdi-map-marker' : null"
              @click="setPos"
            ></v-text-field>
          </v-col>
          <v-col cols="3" class="d-flex justify-center shrink">
            <v-btn
              class="ma-2"
              outlined
              fab
              small
              color="primary"
              @click="countProds('minus')"
            >
              <v-icon>mdi-minus</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
      <!-- <v-card-actions>
        <v-btn>Aceptar</v-btn>
      </v-card-actions> -->
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
    ImgForGrid,
  },

  data() {
    return {
      useBC1: true,
      useBC2: true,
      productID: '',
      ubicacionID: '',
      countEmpaq: 1,
      countUni: 0,
      xpos1: 0,
      xpos2: 0,
      cE: true,
      dataSource: null,
      selectedKeys: [],
      msgReloc: '',
      msgColor: 'secondary',
      snackbar: false,
      product,
      stocklist: [],
      selectedItem: 0,
      showImg: false,
      rules: {
        required: (v) => !!v || 'Requerido',
      },
    }
  },
  computed: {
    curCount() {
      const cE = this.countEmpaq
      const cU = this.countUni
      return `${cE} / ${cU}`
    },
  },
  mounted() {
    this.$nextTick(() => this.$refs.txtProdID.focus())
  },
  methods: {
    async findLocations() {
      if (this.productID) {
        const keyType = this.useBC1 ? 'BC' : 'SKU'
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
                const prod = {
                  sku: '*****',
                  barcode: '0000000000000',
                  descrip: 'NO DISPONIBLE',
                  um: 'UNI',
                  precio: '0',
                  disponible: 'NON',
                  reservado: '0 / 0',
                  stock: '0 / 0',
                  foto: '/no_image.png',
                }
                this.product = Object.assign({}, prod)
                this.stocklist = []
                this.msgReloc = 'Producto no disponible'
                this.msgColor = 'yellow'
                this.snackbar = true
              }
            }
          })
      }
    },
    countProds(opc) {
      if (opc === 'plus') {
        if (this.xpos1 <= this.xpos2) {
          this.countEmpaq++
        } else {
          this.countUni++
        }
      }

      if (opc === 'minus') {
        if (this.xpos1 <= this.xpos2) {
          if (this.countEmpaq > 1) this.countEmpaq--
        } else {
          this.countUni--
          if (this.countUni < 1) this.countUni = 0
        }
      }
    },
    setPos() {
      const txt = this.$refs.txtCurCount.$refs.input
      const xstr = txt.value
      this.xpos1 = txt.selectionStart
      this.xpos2 = xstr.indexOf('/')
      if (this.xpos1 <= this.xpos2) {
        this.cE = true
      } else {
        this.cE = false
      }
      // console.log(`XSTR: ${xstr}  XPOS1 ${this.xpos1}  XPOS2 ${this.xpos2}`)
    },
  },
}
</script>

<style scoped>
.centered-input >>> input {
  text-align: center;
  font-size: 1.5rem;
}
</style>
