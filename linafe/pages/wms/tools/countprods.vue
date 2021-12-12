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
        <v-spacer></v-spacer>
        <v-menu bottom left>
          <template v-slot:activator="{ on, attrs }">
            <v-btn icon v-bind="attrs" color="primary" v-on="on">
              <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item link>
              <v-list-item-title>Ver conteo</v-list-item-title>
            </v-list-item>
            <v-list-item link>
              <v-list-item-title>Limpiar conteo</v-list-item-title>
            </v-list-item>
            <v-list-item link @click.stop="showConfig = true">
              <v-list-item-title>Configuración</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
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
              :disabled="fijarUbicacion"
              :rules="[rules.required]"
              :append-outer-icon="'mdi-send'"
              clearable
              placeholder="Ubicación"
              type="text"
              class="mx-2"
              @keydown.enter="loadProdsPerLocation"
              @click:append-outer="loadProdsPerLocation"
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
              :disabled="countDisabled"
              type="text"
              class="mx-2"
              @keydown.enter="findProduct"
              @click:append-outer="findProduct"
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
        <v-row
          v-show="showPackageCount"
          justify="space-around"
          align="center"
          dense
        >
          <v-col cols="3" class="d-flex justify-center shrink">
            <v-btn
              class="ma-2"
              outlined
              fab
              small
              color="primary"
              @click="countPackage('plus')"
            >
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </v-col>
          <v-col cols="6" class="d-flex justify-center shrink">
            <v-text-field
              ref="txtPackageCount"
              v-model="packageCount"
              label="Bultos"
              placeholder="Bultos"
              type="text"
              class="centered-input"
            ></v-text-field>
          </v-col>
          <v-col cols="3" class="d-flex justify-center shrink">
            <v-btn
              class="ma-2"
              outlined
              fab
              small
              color="primary"
              @click="countPackage('minus')"
            >
              <v-icon>mdi-minus</v-icon>
            </v-btn>
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
    <v-dialog v-model="showConfig" max-width="300">
      <v-card>
        <v-card-title class="text-h5"> Configuración </v-card-title>
        <v-divider />
        <v-card-text>
          <v-row no-gutters>
            <v-switch
              v-model="fijarUbicacion"
              label="Fijar Ubicación"
            ></v-switch>
          </v-row>
          <v-row no-gutters>
            <v-switch
              v-model="countPerPackage"
              label="Contar por bulto"
              @click="!countPerPackage ? (showPackageCount = false) : null"
            ></v-switch>
          </v-row>
          <v-row no-gutters>
            <v-switch
              v-model="showPackageCount"
              label="Ver conteo de bultos"
              :disabled="!countPerPackage"
            ></v-switch>
          </v-row>
        </v-card-text>
        <v-divider />
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="showConfig = false">
            Cerrar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
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
      prodsPerLocation: [],
      fijarUbicacion: false,
      countDisabled: true,
      countPerPackage: false,
      showPackageCount: false,
      showConfig: false,
      packageCount: 1, // Cuenta de bultos
      packingCount: 1, // Cuenta de empaques
      uniCount: 0, // Cuenta de unidades
      xpos1: 0,
      xpos2: 0,
      cE: true,
      dataSource: null,
      selectedKeys: [],
      msgReloc: '',
      msgColor: 'secondary',
      snackbar: false,
      product: Object.assign({}, product),
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
      const cE = this.packingCount
      const cU = this.uniCount
      return `${cE} / ${cU}`
    },
  },
  mounted() {
    this.$nextTick(() => this.$refs.txtUbicacionID.focus())
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
    findProduct() {
      if (!this.fijarUbicacion) {
        if (this.prodsPerLocation.length > 0) {
          const xProd = () => {
            if (this.useBC2) {
              return this.prodsPerLocation.find(
                (o) => o.BARCODE === this.productID
              )
            } else {
              return this.prodsPerLocation.find((o) => o.SKU === this.productID)
            }
          }

          const p = xProd()

          if (p) {
            this.product.sku = p.SKU
            this.product.barcode = p.BARCODE
            this.product.descrip = p.DESCRIP
            this.product.um = p.UM
            this.product.disponible = p.CANT1
            this.product.precio = 0
            this.product.foto = this.$config.fotosURL + p.FOTO
          } else {
            this.product = Object.assign({}, product)
            this.msgReloc = `El producto ${this.productID} no debe estar en esta ubicación`
            this.msgColor = 'red'
            this.snackbar = true
          }

          this.productID = ''
          this.$nextTick(() => this.$refs.txtProdID.focus())
        }
      }
    },
    async loadProdsPerLocation() {
      if (this.ubicacionID) {
        const keyType = this.useBC1 ? 'BC' : 'SKU'
        await this.$axios
          .get('wms/prodsperloc/', {
            params: {
              p01: this.ubicacionID,
              p02: keyType,
              p03: '01',
            },
          })
          .then((response) => {
            if (response.data) {
              if (response.data.length > 0) {
                this.prodsPerLocation = response.data
                this.countDisabled = false
                this.product = Object.assign({}, product)
                this.$nextTick(() => this.$refs.txtProdID.focus())
                this.msgReloc = 'Ubicación cargada con éxito'
                this.msgColor = 'green'
                this.snackbar = true
              } else {
                this.prodsPerLocation = []
                this.countDisabled = true
                this.product = Object.assign({}, product)
                this.msgReloc = 'Ubicación no encontrada'
                this.msgColor = 'red'
                this.snackbar = true
              }
            }
          })
      }
    },
    countPackage(opc) {
      if (opc === 'plus') {
        this.packageCount++
      }

      if (opc === 'minus') {
        if (this.packageCount > 0) this.packageCount--
      }
    },
    countProds(opc) {
      if (opc === 'plus') {
        if (this.xpos1 <= this.xpos2) {
          this.packingCount++
        } else {
          this.uniCount++
        }
      }

      if (opc === 'minus') {
        if (this.xpos1 <= this.xpos2) {
          if (this.packingCount > 1) this.packingCount--
        } else {
          this.uniCount--
          if (this.uniCount < 1) this.uniCount = 0
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
