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
        <span>Conteo físico</span>
        <v-spacer></v-spacer>
        <v-menu bottom left>
          <template v-slot:activator="{ on, attrs }">
            <v-btn icon v-bind="attrs" color="primary" v-on="on">
              <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item link @click.stop="showCount = true">
              <v-list-item-title>Ver conteo</v-list-item-title>
            </v-list-item>
            <v-list-item link @click="clearForm(1)">
              <v-list-item-title>Limpiar</v-list-item-title>
            </v-list-item>
            <v-list-item link @click.stop="showProdsPerLocarion = true">
              <v-list-item-content>
                <v-list-item-title>Ver productos</v-list-item-title>
                <v-list-item-subtitle>
                  Productos de la ubicación
                </v-list-item-subtitle>
              </v-list-item-content>
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
              @click:clear="clearForm"
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
              :disabled="countDisabled"
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
              :disabled="countDisabled"
            ></v-text-field>
          </v-col>
          <v-col cols="3" class="d-flex justify-center shrink">
            <v-btn
              class="ma-2"
              outlined
              fab
              small
              color="primary"
              :disabled="countDisabled"
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
              :disabled="countDisabled"
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
              :disabled="countDisabled"
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
              :disabled="countDisabled"
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
    <v-dialog v-model="showProdsPerLocarion" max-width="400">
      <v-card min-height="250">
        <v-toolbar color="secondary" dark>
          <v-toolbar-title>Productos en la ubicación</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn icon @click="showProdsPerLocarion = false">
            <v-icon>mdi-window-close</v-icon>
          </v-btn>
        </v-toolbar>
        <v-row justify="center" align="center" no-gutters>
          <div class="ubix">{{ curUBIX }}</div>
        </v-row>
        <v-divider />
        <div class="list-container">
          <DxList :data-source="prodsPerLocation" height="300">
            <template #item="{ data: item }">
              <div>
                <div class="conteo">
                  <div class="cuentasku">{{ `SKU: ${item.SKU}` }}</div>
                  <div class="cuentacant">{{ item.DESCRIP }}</div>
                  <div class="cuentacant">
                    {{ `Cantidad: ${item.CANT1}` }}
                  </div>
                </div>
                <div class="dt-container">
                  <div class="bultos">{{ item.BULTOS }}</div>
                  <div class="caption">bultos</div>
                </div>
              </div>
            </template>
          </DxList>
        </div>
        <v-divider />
        <v-card-actions>
          <v-btn
            text
            block
            color="primary"
            @click="showProdsPerLocarion = false"
          >
            Aceptar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="showCount" max-width="400">
      <v-card min-height="250">
        <v-toolbar color="secondary" dark>
          <v-toolbar-title>Conteo en proceso</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn icon @click="askClearList = true">
            <v-icon>mdi-delete-sweep-outline</v-icon>
          </v-btn>
        </v-toolbar>
        <div class="list-container">
          <DxList
            :data-source="listDataSource"
            height="300"
            :grouped="true"
            :allow-item-deleting="true"
            item-delete-mode="swipe"
          >
            <template #item="{ data: item }">
              <div>
                <div class="conteo">
                  <div class="cuentasku">{{ `SKU: ${item.SKU}` }}</div>
                  <div class="cuentacant">{{ `Bultos: ${item.PACKAGE}` }}</div>
                  <div class="cuentacant">
                    {{ `Cantidad: ${item.PACKING} / ${item.UNI}` }}
                  </div>
                </div>
                <div class="dt-container">
                  <div class="dt">{{ item.TIME }}</div>
                </div>
              </div>
            </template>
            <template #group="{ data: item }">
              <div>{{ item.key }}</div>
            </template>
          </DxList>
        </div>
        <v-divider />
        <v-card-actions>
          <v-btn text color="green darken-1" @click="showCount = false">
            Enviar
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn text color="red darken-1" @click="showCount = false">
            Cerrar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="askClearList" max-width="300">
      <v-card>
        <v-card-title class="text-h5"> Limpiar lista de conteo </v-card-title>
        <v-card-text>{{ msgClearList }}</v-card-text>
        <v-card-actions>
          <v-btn color="green darken-1" text @click.stop="clearList">
            Aceptar
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn color="red darken-1" text @click="askClearList = false">
            Cancelar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-snackbar v-model="snackbar" timeout="5000">
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
import ArrayStore from 'devextreme/data/array_store'
import DataSource from 'devextreme/data/data_source'
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

const getTime = () => {
  const curDT = new Date()
  const date = `${curDT.getFullYear()}-${
    curDT.getMonth() + 1
  }-${curDT.getDate()}`
  const time = `${curDT.getHours()}:${curDT.getMinutes()}:${curDT.getSeconds()}`
  return `${date} ${time}`
}

export default {
  components: {
    DxList,
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
      curIndex: -1,
      countDisabled: true,
      countPerPackage: true,
      showPackageCount: false,
      showConfig: false,
      showCount: false,
      showProdsPerLocarion: false,
      askClearList: false,
      packageCount: 0, // Cuenta de bultos
      packingCount: 0, // Cuenta de empaques
      uniCount: 0, // Cuenta de unidades
      packingPerPackage: 1,
      listProdsCounted: [],
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
      loadingView: false,
      rules: {
        required: (v) => !!v || 'Requerido',
      },
    }
  },
  computed: {
    curUBIX() {
      let ubix = 'UBIX'

      if (this.prodsPerLocation) {
        if (this.prodsPerLocation.length > 0) {
          ubix = this.prodsPerLocation[0].UBIX
        }
      }

      return ubix
    },
    curCount: {
      get() {
        const cE = this.packingCount
        const cU = this.uniCount
        return `${cE} / ${cU}`
      },
      set(newVal) {
        const newCount = newVal.split('/')
        const packingC = Number(newCount[0].trim())
        const uniC = Number(newCount[1].trim())

        this.packingCount = isNaN(packingC) ? 0 : packingC
        this.uniCount = isNaN(uniC) ? 0 : uniC
      },
    },
    listDataSource() {
      const aStore = new ArrayStore({
        data: this.listProdsCounted,
        key: 'SKU',
      })

      return new DataSource({ store: aStore, group: 'UBIX', sort: 'TIME' })
    },
    msgClearList() {
      let msg =
        'Pulse ACEPTAR si realmente desea borrar la lista de conteo en curso'
      if (this.listProdsCounted.length === 0) {
        msg = 'LA LISTA ESTÁ VACIA'
      }
      return msg
    },
  },
  watch: {
    packageCount(newVal) {
      if (this.curIndex >= 0) {
        if (this.countPerPackage) {
          this.listProdsCounted[this.curIndex].PACKAGE = isNaN(newVal)
            ? 0
            : newVal
          this.packingCount = this.packageCount * this.packingPerPackage
          this.listProdsCounted[this.curIndex].PACKING = this.packingCount
          this.listProdsCounted[this.curIndex].TIME = getTime()
        }
      }
    },
    packingCount(newVal) {
      if (this.curIndex >= 0) {
        if (!this.countPerPackage) {
          this.listProdsCounted[this.curIndex].PACKING = newVal
          this.listProdsCounted[this.curIndex].TIME = getTime()
        }
      }
    },
    uniCount(newVal) {
      if (this.curIndex >= 0) {
        this.listProdsCounted[this.curIndex].UNI = newVal
        this.listProdsCounted[this.curIndex].TIME = getTime()
      }
    },
    ubicacionID(newVal) {
      if (!newVal) {
        this.prodsPerLocation = []
        this.countDisabled = true
      }
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
                // const prod = {
                //   sku: '*****',
                //   barcode: '0000000000000',
                //   descrip: 'NO DISPONIBLE',
                //   um: 'UNI',
                //   precio: '0',
                //   disponible: 'NON',
                //   reservado: '0 / 0',
                //   stock: '0 / 0',
                //   foto: '/no_image.png',
                // }
                this.product = Object.assign({}, product)
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
          this.loadingView = true
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

            let indx = -1

            if (this.listProdsCounted.length > 0) {
              indx = this.listProdsCounted.findIndex((obj) => obj.SKU === p.SKU)

              if (indx >= 0) {
                this.curIndex = indx
                let packageC = this.listProdsCounted[indx].PACKAGE
                let packingC = this.listProdsCounted[indx].PACKING
                let uniC = this.listProdsCounted[indx].UNI
                this.packingPerPackage = this.listProdsCounted[indx].CANTXBULTO

                if (!this.cE) {
                  uniC++
                } else if (this.countPerPackage) {
                  packageC++
                  packingC += this.packingPerPackage
                } else {
                  packingC++
                }

                if (this.countPerPackage) this.packageCount = packageC
                this.packingCount = packingC
                this.uniCount = uniC

                if (this.countPerPackage) {
                  this.listProdsCounted[indx].PACKAGE = this.packageCount
                }
                this.listProdsCounted[indx].PACKING = this.packingCount
                this.listProdsCounted[indx].UNI = this.uniCount
                this.listProdsCounted[indx].TIME = getTime()
              }
            }

            // Add product to list
            if (indx < 0) {
              let packageC = 0
              let packingC = 0
              let uniC = 0
              this.packingPerPackage = p.CANTXBULTO

              const pc = {
                SKU: p.SKU,
                PACKAGE: 0,
                PACKING: 0,
                UNI: 0,
                CANTXBULTO: this.packingPerPackage,
                UBIX: p.UBIX,
                UBIXBC: p.UBIXBC,
                TIME: getTime(),
              }

              indx = this.listProdsCounted.push(pc) - 1
              this.curIndex = indx

              if (!this.cE) {
                uniC++
              } else if (this.countPerPackage) {
                packageC++
                packingC += this.packingPerPackage
              } else {
                packingC++
              }

              if (this.countPerPackage) this.packageCount = packageC
              this.packingCount = packingC
              this.uniCount = uniC

              if (this.countPerPackage) {
                this.listProdsCounted[indx].PACKAGE = this.packageCount
              }
              this.listProdsCounted[indx].PACKING = this.packingCount
              this.listProdsCounted[indx].UNI = this.uniCount
              // this.listProdsCounted[indx].TIME = getTime()
            }
          } else {
            this.curIndex = -1
            this.product = Object.assign({}, product)
            this.msgReloc = `El producto ${this.productID} no debe estar en esta ubicación`
            this.msgColor = 'red'
            this.snackbar = true
          }

          this.loadingView = false

          this.productID = ''
          this.$nextTick(() => this.$refs.txtProdID.focus())
        }
      }
    },
    async loadProdsPerLocation() {
      if (this.ubicacionID) {
        const keyType = this.useBC1 ? 'BC' : 'SKU'
        this.loadingView = true
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
                this.curIndex = -1
                this.packageCount = 0
                this.packingCount = 0
                this.uniCount = 0
                this.product = Object.assign({}, product)
                this.msgReloc = 'Ubicación no encontrada'
                this.msgColor = 'red'
                this.snackbar = true
              }
            }
            this.loadingView = false
          })
      }
    },
    countPackage(opc) {
      if (opc === 'plus') {
        this.packageCount++
        this.packingCount += this.packingPerPackage
      }

      if (opc === 'minus') {
        if (this.packageCount > 0) {
          this.packageCount--
          this.packingCount -= this.packingPerPackage
          if (this.packingCount < 0) this.packingCount = 0
        }
      }
    },
    countProds(opc) {
      if (opc === 'plus') {
        if (this.xpos1 <= this.xpos2) {
          if (this.countPerPackage) {
            this.packingCount += this.packingPerPackage
          } else {
            this.packingCount++
          }
        } else {
          this.uniCount++
        }
      }

      if (opc === 'minus') {
        if (this.xpos1 <= this.xpos2) {
          if (this.packingCount > 1) {
            if (this.countPerPackage) {
              this.packingCount -= this.packingPerPackage
            } else {
              this.packingCount--
            }
          }
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
    },
    clearForm(opc = 0) {
      this.product = Object.assign({}, product)
      this.curIndex = -1
      this.productID = ''
      this.packageCount = 0
      this.packingCount = 0
      this.uniCount = 0
      if (opc === 1) this.ubicacionID = ''
    },
    clearList() {
      this.listProdsCounted = []
      this.clearForm()
      this.askClearList = false
    },
  },
}
</script>

<style scoped>
.centered-input >>> input {
  text-align: center;
  font-size: 1.5rem;
}
.list-container {
  min-height: 200px;
  max-height: 300px;
  height: auto;
}
.conteo {
  float: left;
}
.conteo .cuentasku {
  font-weight: bold;
}
.cuentasku {
  font-size: 18px;
  font-weight: bold;
}
.cuentacant {
  font-size: 18px;
  opacity: 0.7;
}
.dt-container {
  float: right;
  padding-top: 13px;
}
.dt-container > div {
  display: inline-block;
}
.dt-container .dt {
  font-size: 14px;
}
.dt-container .bultos {
  font-size: 18px;
}
.dt-container .caption {
  font-size: 11px;
  line-height: 12px;
  padding-left: 6px;
  opacity: 0.7;
}
.ubix {
  padding-top: 10px;
  font-weight: bold;
  font-size: 20px;
  color: rgb(136, 7, 33);
}
</style>
