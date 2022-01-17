<template>
  <v-form ref="form" v-model="valid" lazy-validation>
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
              <v-list-item link @click="clearForm()">
                <v-list-item-title>Limpiar</v-list-item-title>
              </v-list-item>
              <v-list-item
                link
                :disabled="!lockUbix"
                @click.stop="showProdsPerLocarion = true"
              >
                <v-list-item-content>
                  <v-list-item-title>Ver productos</v-list-item-title>
                  <v-list-item-subtitle>
                    Productos de la ubicación
                  </v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-list-item link>
                <v-list-item-title>Historial</v-list-item-title>
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
              <v-btn
                class="ma-2"
                text
                icon
                large
                color="primary"
                @click="lockUbix = !lockUbix"
              >
                <v-icon v-show="lockUbix">mdi-lock</v-icon>
                <v-icon v-show="!lockUbix"
                  >mdi-lock-open-variant-outline</v-icon
                >
              </v-btn>
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
                @keydown.enter="loadProdsPerLocation"
                @click:append-outer="loadProdsPerLocation"
                @click:clear="clearForm"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row dense>
            <v-col cols="3">
              <v-switch v-model="useBC" class="mx-2" />
            </v-col>
            <v-col cols="9">
              <v-text-field
                ref="txtProdID"
                v-model="productID"
                :append-outer-icon="'mdi-send'"
                clearable
                :placeholder="useBC ? 'Código de Barra' : 'SKU de Producto'"
                :disabled="lockUbix && prodIDDisabled"
                type="text"
                class="mx-2"
                @keydown.enter="findProduct"
                @click:append-outer="findProduct"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col
              v-if="showImg !== 12"
              :cols="12 - showImg"
              class="d-flex justify-center shrink"
            >
              <ImgForGrid
                :img-file="curProd.foto"
                :swidth="100"
                :lwidth="200"
              />
            </v-col>
            <v-col :cols="showImg">
              <v-row justify="start" align="center" dense>
                <v-card-title class="my-0 py-0 px-2">
                  {{ curProd.sku }}
                </v-card-title>
              </v-row>
              <v-row justify="start" align="center" dense>
                <v-card-text class="my-0 pt-0 px-2">
                  <div class="text-subtitle-1">
                    {{ curProd.descrip }}
                  </div>
                </v-card-text>
              </v-row>
              <v-row justify="start" align="center" dense>
                <v-card-text class="my-0 py-0 px-2">
                  {{ curProd.barcode }}
                </v-card-text>
              </v-row>
              <v-row justify="start" align="center">
                <v-chip color="light-blue" text-color="white" class="mx-2">
                  {{ `Empaque: ${curProd.empaque}` }}
                </v-chip>
              </v-row>
            </v-col>
          </v-row>
          <v-divider></v-divider>
          <v-row
            v-show="countPerPackage"
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
                v-model.number="packageCount"
                label="Bultos"
                placeholder="Bultos"
                type="number"
                class="centered-input"
                :rules="[rules.positiveNumber]"
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
                ref="txtExcepCount"
                v-model="excepCount"
                :label="
                  countPerPackage ? `${curProd.um} (Excepción)` : curProd.um
                "
                :placeholder="
                  countPerPackage ? `${curProd.um} (Excepción)` : curProd.um
                "
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
          <v-divider></v-divider>
        </v-card-text>
        <v-card-actions>
          <v-btn
            v-show="countPerPackage"
            color="primary"
            :disabled="countDisabled"
            block
            rounded
            @click="$nextTick(() => $refs.txtProdID.focus())"
          >
            {{ `Tot: ${curCount}` }}
            <v-icon right dark>mdi-check</v-icon>
          </v-btn>
        </v-card-actions>
        <template v-for="(item, i) in stocklist">
          <v-card
            v-if="item.LINALLOW != 'H'"
            :key="i"
            tile
            class="mx-auto mb-2"
          >
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
                v-model="countPerPackage"
                label="Contar por bultos"
              ></v-switch>
            </v-row>
            <!-- <v-row no-gutters>
              <v-switch
                v-model="showPackageCount"
                label="Ver conteo de bultos"
                :disabled="!countPerPackage"
              ></v-switch>
            </v-row> -->
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
              height="250"
              :grouped="true"
              :allow-item-deleting="true"
              item-delete-mode="slideItem"
              @item-deleted="onlistDataSourceDelete"
            >
              <template #item="{ data: item }">
                <div>
                  <div class="conteo">
                    <div class="cuentasku">{{ `SKU: ${item.SKU}` }}</div>
                    <div class="cuentacant">
                      {{ `Bultos: ${item.PACKAGEC}` }}
                    </div>
                    <div class="cuentacant">
                      {{ `Cantidad: ${item.PACKINGTOTC} / ${item.UNI}` }}
                    </div>
                  </div>
                  <div class="dt-container">
                    <div class="dt">{{ cTime(item.CTIME, 0) }}</div>
                    <br />
                    <div class="dt">{{ cTime(item.CTIME, 1) }}</div>
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
            <v-btn
              text
              color="green darken-1"
              :disabled="listProdsCounted.length == 0"
              @click="sendCount"
            >
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
          <v-card-title class="text-h5"> Limpiar lista </v-card-title>
          <v-card-text>{{ msgClearList }}</v-card-text>
          <v-card-actions>
            <v-btn
              color="green darken-1"
              text
              :disabled="listProdsCounted.length == 0"
              @click.stop="clearList"
            >
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
          <v-btn
            :color="msgColor"
            text
            v-bind="attrs"
            @click="snackbar = false"
          >
            Cerrar
          </v-btn>
        </template>
      </v-snackbar>
    </div>
  </v-form>
</template>

<script>
import { mapGetters } from 'vuex'
import DxList from 'devextreme-vue/list'
import ArrayStore from 'devextreme/data/array_store'
import DataSource from 'devextreme/data/data_source'
import ImgForGrid from '~/components/utilities/ImgForGrid'

const getTime = () => {
  const curDT = new Date()
  const Y = curDT.getFullYear()
  const M = (curDT.getMonth() + 1).toString().padStart(2, '0')
  const D = curDT.getDate().toString().padStart(2, '0')
  const date = `${Y}-${M}-${D}`

  const hh = curDT.getHours().toString().padStart(2, '0')
  const mm = curDT.getMinutes().toString().padStart(2, '0')
  const ss = curDT.getSeconds().toString().padStart(2, '0')
  const time = `${hh}:${mm}:${ss}`
  return `${date} ${time}`
}

const curProd = {
  sku: '*****',
  barcode: '0000000000000',
  descrip: 'PRODUCT',
  um: 'UNI',
  empaque: 'UNI',
  ppp: 1,
  // PACKAGEC: 0,
  // PACKINGC: 0,
  // PACKINGTOTC: 0,
  // UNI: 0,
  // CTIME: getTime(),
  precio: '0',
  disponible: 'NON',
  reservado: '0 / 0',
  stock: '0 / 0',
  foto: '/no_image.png',
}

export default {
  components: {
    DxList,
    ImgForGrid,
  },

  data() {
    return {
      useBC1: true,
      useBC: true,
      lockUbix: true,
      productID: '',
      prodIDDisabled: true,
      ubicacionID: '',
      prodsPerLocation: [],
      curIndex: -1,
      countDisabled: true,
      countPerPackage: true,
      showPackageCount: true,
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
      valid: true,
      msgReloc: '',
      msgColor: 'secondary',
      snackbar: false,
      curProd: Object.assign({}, curProd),
      stocklist: [],
      selectedItem: 0,
      showImg: 12,
      loadingView: false,
      rules: {
        required: (v) => !!v || 'Requerido',
        positiveNumber: (v) => v >= 0 || 'La cantidad no puede ser negativa',
      },
    }
  },
  computed: {
    ...mapGetters('sistema', ['getCurCia']),
    curUBIX() {
      let ubix = 'UBIX'

      if (this.prodsPerLocation) {
        if (this.prodsPerLocation.length > 0) {
          ubix = this.prodsPerLocation[0].UBIX
        }
      }

      return ubix
    },
    excepCount: {
      get() {
        // Cuenta de empaques y unidades de excepción
        const pC = this.packingCount
        const uC = this.uniCount
        return `${pC} / ${uC}`
      },
      set(newVal) {
        if (newVal) {
          const newCount = newVal.split('/')

          const pC = newCount[0] ? Number(newCount[0].trim()) : 0
          const uC = newCount[1] ? Number(newCount[1].trim()) : 0

          this.packingCount = isNaN(pC) ? 0 : pC
          this.uniCount = isNaN(uC) ? 0 : uC
        } else {
          this.packingCount = 0
          this.uniCount = 0
        }
      },
    },
    curCount() {
      // Cuenta total de empaques y unidades
      const pC = this.packageCount * this.packingPerPackage + this.packingCount
      const uC = this.uniCount
      return `${pC} / ${uC}`
    },
    listDataSource() {
      const aStore = new ArrayStore({
        data: this.listProdsCounted,
        key: 'SKU',
      })

      return new DataSource({ store: aStore, group: 'UBIX', sort: 'CTIME' })
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
    curCount(newVal) {
      if (this.curIndex >= 0) {
        const newCount = newVal.split('/')
        const pCTot = Number(newCount[0].trim())
        const uniC = Number(newCount[1].trim())

        const curinx = this.curIndex

        this.listProdsCounted[curinx].PACKINGC = this.packingCount
        this.listProdsCounted[curinx].PACKAGEC = this.packageCount
        this.listProdsCounted[curinx].PACKINGTOTC = isNaN(pCTot) ? 0 : pCTot
        this.listProdsCounted[curinx].UNI = isNaN(uniC) ? 0 : uniC
        this.listProdsCounted[curinx].CTIME = getTime()
      }
    },
    ubicacionID(newVal) {
      if (!newVal) {
        this.clearForm()
      }
    },
  },
  mounted() {
    this.$nextTick(() => this.$refs.txtUbicacionID.focus())
  },
  methods: {
    findProduct() {
      if (this.lockUbix) {
        if (this.prodsPerLocation.length > 0) {
          this.loadingView = true
          const xProd = () => {
            if (this.useBC) {
              return this.prodsPerLocation.find(
                (o) => o.BARCODE === this.productID
              )
            } else {
              return this.prodsPerLocation.find(
                (o) => o.SKU.toLowerCase() === this.productID.toLowerCase()
              )
            }
          }

          const p = xProd()

          if (p) {
            this.curProd.sku = p.SKU
            this.curProd.barcode = p.BARCODE
            this.curProd.descrip = p.DESCRIP
            this.curProd.um = p.UM
            this.curProd.empaque = p.EMPAQUE
            this.curProd.ppp = p.PPP
            // this.curProd.PACKAGEC = 0
            // this.curProd.PACKINGC = 0
            // this.curProd.PACKINGTOTC = 0
            this.curProd.disponible = p.CANT1
            this.curProd.precio = 0
            this.curProd.foto = this.$config.fotosURL + p.FOTO

            let indx = -1

            if (this.listProdsCounted.length > 0) {
              indx = this.listProdsCounted.findIndex((obj) => obj.SKU === p.SKU)

              if (indx >= 0) {
                this.curIndex = indx
                let packageC = this.listProdsCounted[indx].PACKAGEC
                let packingC = this.listProdsCounted[indx].PACKINGC
                let uniC = this.listProdsCounted[indx].UNI
                this.packingPerPackage = this.listProdsCounted[indx].PPP

                if (this.countPerPackage) {
                  packageC++
                } else if (this.cE) {
                  packingC++
                } else {
                  uniC++
                }

                this.packageCount = packageC
                this.packingCount = packingC
                this.uniCount = uniC
              }
            }

            // Add product to list
            if (indx < 0) {
              let packageC = 0
              let packingC = 0
              let uniC = 0
              this.packingPerPackage = p.PPP

              const pc = {
                SKU: p.SKU,
                BARCODE: p.BARCODE,
                PACKAGEC: 0,
                PACKINGC: 0,
                PACKINGTOTC: 0,
                DESCRIP: p.DESCRIP,
                UNI: 0,
                EMPAQUE: p.EMPAQUE,
                PPP: this.packingPerPackage,
                UBIX: p.UBIX,
                UBIXBC: p.UBIXBC,
                MARBETE: '0000',
                CTIME: getTime(),
              }

              indx = this.listProdsCounted.push(pc) - 1
              this.curIndex = indx

              if (this.countPerPackage) {
                packageC++
              } else if (this.cE) {
                packingC++
              } else {
                uniC++
              }

              this.packageCount = packageC
              this.packingCount = packingC
              this.uniCount = uniC
            }

            this.countDisabled = false
          } else {
            this.curIndex = -1
            this.curProd = Object.assign({}, curProd)
            this.msgReloc = `El producto ${this.productID} no debe estar en esta ubicación`
            this.msgColor = 'red'
            this.snackbar = true
            this.countDisabled = true
          }

          this.loadingView = false

          this.productID = ''
          this.$nextTick(() => this.$refs.txtProdID.focus())
        }
      } else if (this.listProdsCounted.length > 0) {
        this.loadingView = true
        const prodIndx = () => {
          if (this.useBC) {
            return this.listProdsCounted.findIndex(
              (o) => o.BARCODE === this.productID
            )
          } else {
            return this.listProdsCounted.findIndex(
              (o) => o.SKU.toLowerCase() === this.productID.toLowerCase()
            )
          }
        }

        const indx = prodIndx()

        // Si el producto se encuentra en el conteo actual,
        // se debe cargar desde la lista de conteo en curso
        if (indx >= 0) {
          const px = this.listProdsCounted[indx]
          this.curIndex = indx
          let packageC = px.PACKAGEC
          let packingC = px.PACKINGC
          let uniC = px.UNI
          this.packingPerPackage = px.PPP

          this.curProd.sku = px.SKU
          this.curProd.barcode = px.BARCODE
          this.curProd.descrip = px.DESCRIP
          this.curProd.um = px.UM
          this.curProd.empaque = px.EMPAQUE
          this.curProd.ppp = px.PPP
          this.curProd.disponible = px.CANT1
          this.curProd.precio = 0
          this.curProd.foto = this.$config.fotosURL + px.FOTO

          if (this.countPerPackage) {
            packageC++
          } else if (this.cE) {
            packingC++
          } else {
            uniC++
          }

          this.packageCount = packageC
          this.packingCount = packingC
          this.uniCount = uniC

          this.loadingView = false

          this.countDisabled = false
          this.productID = ''
          this.$nextTick(() => this.$refs.txtProdID.focus())
        } else {
          // Si el producto no se encuentra en el conteo actual,
          // se debe cargar desde la api
          this.loadProd()
        }
      } else {
        this.loadProd()
      }
    },
    async loadProd() {
      this.loadingView = true
      await this.$axios
        .get('wms/prodsperloc/', {
          params: {
            p01: this.ubicacionID,
            p02: this.useBC ? 'BC' : 'SKU',
            p03: this.getCurCia.extrel,
            p04: this.productID,
          },
        })
        .then((response) => {
          if (response.data) {
            if (response.data.length > 0) {
              const px = response.data[0]
              let packageC = 0
              let packingC = 0
              let uniC = 0
              this.packingPerPackage = px.PPP

              const pc = {
                SKU: px.SKU,
                BARCODE: px.BARCODE,
                PACKAGEC: 0,
                PACKINGC: 0,
                PACKINGTOTC: 0,
                DESCRIP: px.DESCRIP,
                UNI: 0,
                EMPAQUE: px.EMPAQUE,
                PPP: this.packingPerPackage,
                UBIX: px.UBIX,
                UBIXBC: px.UBIXBC,
                MARBETE: '0000',
                CTIME: getTime(),
              }

              this.curIndex = this.listProdsCounted.push(pc) - 1

              this.curProd.sku = px.SKU
              this.curProd.barcode = px.BARCODE
              this.curProd.descrip = px.DESCRIP
              this.curProd.um = px.UM
              this.curProd.empaque = px.EMPAQUE
              this.curProd.ppp = px.PPP
              this.curProd.disponible = px.CANT1
              this.curProd.precio = 0
              this.curProd.foto = this.$config.fotosURL + px.FOTO

              if (this.countPerPackage) {
                packageC++
              } else if (this.cE) {
                packingC++
              } else {
                uniC++
              }

              this.packageCount = packageC
              this.packingCount = packingC
              this.uniCount = uniC

              this.countDisabled = false
              this.productID = ''
              this.$nextTick(() => this.$refs.txtProdID.focus())
            } else {
              this.prodsPerLocation = []
              this.countDisabled = true
              this.prodIDDisabled = true
              this.curIndex = -1
              this.packageCount = 0
              this.packingCount = 0
              this.uniCount = 0
              this.curProd = Object.assign({}, curProd)
              this.msgReloc = 'SKU no encontrado'
              this.msgColor = 'red'
              this.snackbar = true
            }
          }
          this.loadingView = false
        })
    },
    async loadProdsPerLocation() {
      if (this.ubicacionID) {
        if (this.lockUbix) {
          this.loadingView = true
          await this.$axios
            .get('wms/prodsperloc/', {
              params: {
                p01: this.ubicacionID,
                p02: 'BC',
                p03: this.getCurCia.extrel,
              },
            })
            .then((response) => {
              if (response.data) {
                if (response.data.length > 0) {
                  this.prodsPerLocation = response.data
                  this.prodIDDisabled = false
                  // this.countDisabled = false
                  this.curProd = Object.assign({}, curProd)
                  this.$nextTick(() => this.$refs.txtProdID.focus())
                  this.msgReloc = 'Ubicación cargada con éxito'
                  this.msgColor = 'green'
                  this.snackbar = true
                } else {
                  this.prodsPerLocation = []
                  this.countDisabled = true
                  this.prodIDDisabled = true
                  this.curIndex = -1
                  this.packageCount = 0
                  this.packingCount = 0
                  this.uniCount = 0
                  this.curProd = Object.assign({}, curProd)
                  this.msgReloc = 'Ubicación no encontrada'
                  this.msgColor = 'red'
                  this.snackbar = true
                }
              }
              this.loadingView = false
            })
        } else {
          this.validDestino()
        }
      }
    },
    countPackage(opc) {
      if (opc === 'plus') {
        this.packageCount++
      }

      if (opc === 'minus') {
        if (this.packageCount > 0) {
          this.packageCount--
        }
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
          if (this.packingCount > 0) {
            this.packingCount--
          }
        } else {
          this.uniCount--
          if (this.uniCount < 0) this.uniCount = 0
        }
      }
    },
    async sendCount() {
      const curlPC = JSON.stringify(this.listProdsCounted)

      this.showCount = false
      this.loadingView = true

      await this.$axios
        .post('wms/extcountedprods/', {
          items: curlPC,
          cia: '01',
        })
        .then((response) => {
          if (response.data) {
            this.msgReloc = response.data.msg // 'Cuenta enviada con éxito'
            this.msgColor = 'green'
            this.snackbar = true
          } else {
            this.msgReloc = 'Error al enviar la cuenta en curso'
            this.msgColor = 'red'
            this.snackbar = true
          }
        })
        .catch((err) => {
          if (err.response) {
            let msgerr = 'X'
            if (err.response.data.non_field_errors) {
              msgerr = err.response.data.non_field_errors[0]
            } else if (err.response.data.detail) {
              msgerr = err.response.data.detail
            } else {
              msgerr = err.response.statusText
            }
            this.$nuxt.context.error({
              statusCode: err.response.status,
              message: msgerr,
            })
          } else if (err.request) {
            this.$nuxt.context.error({
              statusCode: 503,
              message: 'No hubo respuesta del servidor',
            })
          } else {
            this.$nuxt.context.error({
              statusCode: 1000,
              message: err.message,
            })
          }
        })
      this.loadingView = false
    },
    async validDestino() {
      if (this.ubicacionID) {
        await this.$axios
          .get('wms/relocatext/', {
            params: {
              p01: 'VALIDUBIX',
              p02: 'O',
              p03: this.ubicacionID,
              p04: 0,
              p05: this.getCurCia.extrel,
            },
          })
          .then((response) => {
            if (response.data) {
              if (response.data.length > 0) {
                const numerr = response.data[0].status.substring(0, 5)
                const msgerr = response.data[0].status.substring(6)
                this.msgReloc = msgerr

                if (numerr.startsWith('EOK')) {
                  this.msgReloc = 'UBICACION VALIDA'
                } else {
                  this.msgReloc = 'NO SE PUDO VALIDAR LA UBICACION'
                }

                this.msgColor = numerr.startsWith('EOK') ? 'green' : 'yellow'
                this.snackbar = true

                this.$nextTick(() => this.$refs.txtProdID.focus())
              } else {
                this.msgReloc = 'SIN RESPUESTA DE LA BASE DE DATOS'
                this.msgColor = 'yellow'
                this.snackbar = true
              }
            }
          })
          .catch((err) => {
            let stcode = 0
            let msg = ''
            if (err.response) {
              stcode = err.response.status
              msg = err.response.data.message
            } else if (err.request) {
              stcode = 503
              msg = err.response.data.message
            } else {
              stcode = 1010
              msg = err.message
            }

            this.msgReloc = `${stcode} - ${msg}`
            this.msgColor = 'red'
            this.snackbar = true
          })
      } else {
        this.msgReloc = 'Proporcione ubicación destino'
        this.msgColor = 'red'
        this.snackbar = true
      }
    },
    setPos() {
      const txt = this.$refs.txtExcepCount.$refs.input
      const xstr = txt.value
      this.xpos1 = txt.selectionStart
      this.xpos2 = xstr.indexOf('/')
      if (this.xpos1 <= this.xpos2) {
        this.cE = true
      } else {
        this.cE = false
      }
    },
    clearForm() {
      if (this.curIndex >= 0) {
        const ptot = this.packageCount + this.packingCount + this.uniCount
        if (ptot === 0) {
          this.listProdsCounted.splice(this.curIndex, 1)
        }
        this.curIndex = -1
      }

      if (this.ubicacionID !== '') this.ubicacionID = ''
      this.prodsPerLocation = []

      this.resetValidation()
      this.prodIDDisabled = true

      this.curProd = Object.assign({}, curProd)

      this.packageCount = 0
      this.packingCount = 0
      this.uniCount = 0

      this.countDisabled = true

      this.$refs.txtUbicacionID.scrollTop = 0
      this.$nextTick(() => this.$refs.txtUbicacionID.focus())
    },
    clearList() {
      this.listProdsCounted = []
      this.clearForm()
      this.askClearList = false
    },
    onlistDataSourceDelete(e) {
      this.clearForm()
    },
    cTime(item, inx) {
      const timepart = item.split(' ')
      return timepart[inx].trim()
    },
    reset() {
      this.$refs.form.reset()
    },
    resetValidation() {
      this.$refs.form.resetValidation()
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
