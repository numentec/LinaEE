<template>
  <div>
    <v-card class="px-0">
      <v-card-title>
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn icon v-bind="attrs" v-on="on" @click="$router.back()">
              <v-icon large color="primary">mdi-chevron-left</v-icon>
            </v-btn>
          </template>
          <span>Volver a vista anterior</span>
        </v-tooltip>
        <span>Reubicar producto</span>
        <v-spacer></v-spacer>
        <v-menu bottom left>
          <template v-slot:activator="{ on, attrs }">
            <v-btn icon v-bind="attrs" color="primary" v-on="on">
              <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item link>
              <v-list-item-title>Historial</v-list-item-title>
            </v-list-item>
            <v-list-item link @click.stop="showConfig = true">
              <v-list-item-title>Configuración</v-list-item-title>
            </v-list-item>
            <v-list-item link @click="cancelStepper">
              <v-list-item-title>Cancelar</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-card-title>
      <v-stepper v-model="curStep" alt-labels flat tile>
        <v-stepper-header class="hidden-sm-and-down px-1">
          <v-stepper-step
            :complete="curStep > 1"
            :step="1"
            :editable="editSteps.s1"
          >
            Producto
          </v-stepper-step>

          <v-stepper-step
            :complete="curStep > 2"
            :step="2"
            :editable="editSteps.s2"
          >
            Origen
          </v-stepper-step>

          <v-stepper-step
            :complete="curStep > 3"
            :step="3"
            :editable="editSteps.s3"
          >
            Cantidad
          </v-stepper-step>

          <v-stepper-step :step="4" :editable="editSteps.s4">
            Destino
          </v-stepper-step>
        </v-stepper-header>

        <v-stepper-items>
          <v-stepper-content step="1" class="pa-0">
            <v-card class="px-4" min-height="200px" flat tile>
              <v-switch v-model="useBC1" label="Use Barcode"></v-switch>
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    ref="txtProdID"
                    v-model="productID"
                    :rules="[rules.required]"
                    :append-outer-icon="'mdi-send'"
                    clearable
                    :placeholder="
                      useBC1 ? 'Barcode de Producto' : 'SKU de Producto'
                    "
                    type="text"
                    @keydown.enter="findLocations"
                    @click:append-outer="findLocations"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-card>
          </v-stepper-content>

          <v-stepper-content step="2" class="px-0">
            <v-card class="px-4" min-height="200px" flat tile>
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    ref="txtOrigen"
                    v-model="origen"
                    :rules="[rules.required]"
                    :append-outer-icon="'mdi-send'"
                    clearable
                    placeholder="Ubicación de origen"
                    type="text"
                    persistent-hint
                    @keydown.enter="setOrigen"
                    @click:append-outer="setOrigen"
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-row justify="center" align="center" no-gutters>
                <div class="text-h6" v-text="`SKU: ${curSKU} (${curUM})`"></div>
              </v-row>
              <v-divider></v-divider>
              <v-row>
                <div class="mb-2">
                  <DxList
                    ref="locationsList"
                    :data-source="dataSource"
                    selection-mode="single"
                    :selected-item-keys="selectedKeys"
                    :hover-state-enabled="true"
                    :height="150"
                    no-data-text="No se encontró"
                    @selection-changed="onSelectionChanged"
                    @item-click="onItemClick"
                  >
                    <template #item="{ data: item }">
                      <v-card flat tile class="mx-auto">
                        <v-row justify="center" align="center" no-gutter>
                          <div class="ubix-container">
                            <div class="ubix">{{ item.UBIX }}</div>
                          </div>
                        </v-row>
                        <v-row justify="center" align="center" no-gutter>
                          <div class="ubix-container">
                            <div class="ubixbc">{{ `${item.UBIXBC}` }}</div>
                          </div>
                        </v-row>
                        <v-row justify="center" align="center">
                          <div class="stock-container">
                            <div class="stock">
                              {{
                                `${item.CANT3}  (Bultos: ${item.BULTOS_DISPONIBLE})`
                              }}
                            </div>
                          </div>
                        </v-row>
                        <v-divider></v-divider>
                      </v-card>
                    </template>
                  </DxList>
                </div>
              </v-row>
            </v-card>
          </v-stepper-content>

          <v-stepper-content step="3" class="px-0">
            <v-card class="px-4" min-height="200px" flat tile>
              <v-row>
                <v-col v-if="showEmpaques" cols="12" md="6">
                  <v-text-field
                    ref="txtEmpaques"
                    v-model.number="cantidad.empaq"
                    :rules="[rules.isNumber]"
                    clearable
                    placeholder="Empaques"
                    label="Empaques"
                    type="text"
                    @focus="$event.target.select()"
                    @keydown.enter="setCantidad"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" :md="showEmpaques ? 6 : 12">
                  <v-text-field
                    ref="txtUnidades"
                    v-model.number="cantidad.uni"
                    :rules="[rules.isNumber]"
                    :append-outer-icon="'mdi-send'"
                    clearable
                    placeholder="Unidades"
                    label="Unidades"
                    type="text"
                    @focus="$event.target.select()"
                    @keydown.enter="setCantidad"
                    @click:append-outer="setCantidad"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-card>
          </v-stepper-content>

          <v-stepper-content step="4" class="px-0">
            <v-card class="px-4" min-height="200px" flat tile>
              <v-switch v-model="useBC2" label="Use Barcode"></v-switch>
              <v-row no-gutters>
                <v-col cols="12">
                  <v-text-field
                    ref="txtDestino"
                    v-model="destino"
                    :rules="[rules.required]"
                    :append-outer-icon="'mdi-send'"
                    clearable
                    :placeholder="useBC2 ? 'Destino (Barcode)' : 'Destino (ID)'"
                    type="text"
                    @keydown.enter="validDestino"
                    @click:append-outer="validDestino"
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-row no-gutters>
                <v-col cols="12" class="d-flex justify-center shrink">
                  <v-card-title
                    ref="lblDestino"
                    class="red--text text--darken-4"
                  >
                    {{ destinoDescrip }}
                  </v-card-title>
                </v-col>
              </v-row>
              <v-row no-gutters>
                <v-col cols="12">
                  <v-card-actions>
                    <v-btn
                      :key="btnkey"
                      color="primary"
                      :disabled="!relocate"
                      block
                      @click.once="execRelocation"
                    >
                      Reubicar
                    </v-btn>
                  </v-card-actions>
                </v-col>
              </v-row>
            </v-card>
          </v-stepper-content>
        </v-stepper-items>
      </v-stepper>
      <v-card-actions>
        <v-btn color="primary" @click="cancelStepper">
          <v-icon v-show="$vuetify.breakpoint.mobile"> mdi-cancel </v-icon>
          <span v-show="!$vuetify.breakpoint.mobile">Cancel</span>
        </v-btn>
        <v-spacer />
        <MobileSteps
          v-show="$vuetify.breakpoint.mobile"
          :cur-step="curStep"
          :enabled-step="editSteps"
          @clickStep="(v) => (curStep = v)"
        />
      </v-card-actions>
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
          <v-row no-gutters>
            <v-text-field
              v-model="preUBIX"
              label="Prefijo de ubicación destino"
              hint="Prefijo que se repite en cada consulta"
              persistent-hint
            ></v-text-field>
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
import { mapGetters } from 'vuex'
import DxList from 'devextreme-vue/list'
import DataSource from 'devextreme/data/data_source'
import MobileSteps from '~/components/utilities/MobileSteps'

export default {
  components: {
    DxList,
    MobileSteps,
  },
  data() {
    return {
      curStep: 1,
      useBC1: false,
      useBC2: true,
      productID: '',
      origen: '',
      destino: '',
      destinoDescrip: '',
      relocate: false,
      dataSource: null,
      curSKU: '###',
      curUM: 'UNI',
      selectedKeys: [],
      selectedLoc: {},
      cantSelectedLoc: { empaq: 0, uni: 0 },
      cantidad: { empaq: 0, uni: 0 },
      showEmpaques: false,
      editSteps: { s1: true, s2: false, s3: false, s4: false },
      showConfig: false,
      countPerPackage: true,
      preUBIX: '',
      btnkey: 1,
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
  computed: {
    ...mapGetters('sistema', ['getCurCia']),
  },
  watch: {
    destino(newVal) {
      if (!newVal) {
        this.relocate = false
        this.destinoDescrip = ''
      }
    },
  },
  mounted() {
    this.$nextTick(() => this.$refs.txtProdID.focus())
  },
  methods: {
    async findLocations() {
      if (this.productID) {
        const keyType = this.useBC1 ? 'BC' : 'SKU'

        this.dataSource = null

        await this.$axios
          .get('wms/qrystockext/', {
            params: { p01: this.productID, p02: keyType, p03: '01', p04: 'D' },
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
                  filter: [['DISP', '>', 0], 'and', ['LINALLOW', '=', 'A']],
                })
                this.curSKU = response.data[0].SKU
                this.curUM = response.data[0].UM

                this.dataSource = ds

                this.editSteps.s1 = true
                this.editSteps.s2 = true
                this.editSteps.s3 = false
                this.editSteps.s4 = false

                this.curStep = 2
                this.$nextTick(() => this.$refs.txtOrigen.focus())
              } else {
                this.curSKU = '###'
                this.curUM = 'UNI'
                this.cantidad.empaq = 0
                this.cantidad.uni = 0

                this.editSteps.s1 = true
                this.editSteps.s2 = false
                this.editSteps.s3 = false
                this.editSteps.s4 = false

                this.msgReloc = 'No disponible para reubicar'
                this.msgColor = 'yellow'
                this.snackbar = true
              }
            }
          })
      }
    },
    onSelectionChanged(e) {
      const loc = e.addedItems[0]
      if (loc) {
        this.selectedLoc = JSON.parse(JSON.stringify(loc))
        this.origen = this.selectedLoc.UBIXBC

        if (this.selectedLoc.SEPARADOR) {
          const i = this.selectedLoc.CANT3.indexOf(this.selectedLoc.SEPARADOR)

          this.cantSelectedLoc.empaq = Number(
            this.selectedLoc.CANT3.substring(0, i - 1).trim()
          )
          this.cantSelectedLoc.uni = Number(
            this.selectedLoc.CANT3.substring(i + 1).trim()
          )

          this.showEmpaques = true
        } else {
          this.cantSelectedLoc.empaq = 0
          this.cantSelectedLoc.uni = Number(this.selectedLoc.CANT3.trim())
          this.showEmpaques = false
        }

        this.cantidad = { ...this.cantSelectedLoc }

        if (this.cantidad.empaq + this.cantidad.uni > 0) {
          // this.editSteps.s1 = true
          // this.editSteps.s2 = true
          this.editSteps.s3 = true
          this.editSteps.s4 = false
          this.curStep = 3
          if (this.showEmpaques) {
            this.$nextTick(() => this.$refs.txtEmpaques.focus())
          } else {
            this.$nextTick(() => this.$refs.txtUnidades.focus())
          }
        }
      } else {
        this.selectedKeys = []
        this.editSteps.s3 = false
        this.editSteps.s4 = false
      }
    },
    onItemClick(e) {
      if (e.itemData.UBIXBC === this.origen) {
        if (this.cantidad.empaq + this.cantidad.uni > 0) {
          this.editSteps.s3 = true
          this.editSteps.s4 = false
          this.curStep = 3
          if (this.showEmpaques) {
            this.$nextTick(() => this.$refs.txtEmpaques.focus())
          } else {
            this.$nextTick(() => this.$refs.txtUnidades.focus())
          }
        }
      }
    },
    setOrigen() {
      if (this.origen) {
        if (!this.selectedKeys.includes(this.origen)) {
          if (this.dataSource._items.length > 0) {
            const isInList = this.dataSource._items.find(
              (obj) => obj.UBIXBC === this.origen || obj.UBIX === this.origen
            )

            if (isInList) {
              this.selectedKeys = [...[], this.origen]
            } else {
              this.msgReloc = 'Ubicación incorrecta'
              this.msgColor = 'red'
              this.snackbar = true
            }
          }
        }
      } else {
        this.msgReloc = 'Proporcione ubicación de origen'
        this.msgColor = 'red'
        this.snackbar = true
      }
    },
    setCantidad() {
      this.cantidad.empaq = Number(this.cantidad.empaq)
      this.cantidad.uni = Number(this.cantidad.uni)

      if (this.cantidad.empaq + this.cantidad.uni > 0) {
        const e = this.cantSelectedLoc.empaq
        const u = this.cantSelectedLoc.uni
        const empaq = Number(this.cantidad.empaq)
        const uni = Number(this.cantidad.uni)
        if (empaq + uni > 0) {
          if (empaq <= e && uni <= u) {
            this.editSteps.s4 = true
            this.curStep = 4
            this.$nextTick(() => this.$refs.txtDestino.focus())
          } else {
            let msgR = `Excede disponible: ${u}`
            if (this.selectedLoc.SEPARADOR) {
              const sep = this.selectedLoc.SEPARADOR
              msgR = `Excede disponible: ${e} ${sep} ${u}`
            }
            this.msgReloc = msgR
            this.msgColor = 'red'
            this.snackbar = true
          }
        }
      } else {
        this.msgReloc = 'Proporcione cantidades válidas'
        this.msgColor = 'red'
        this.snackbar = true
      }
    },
    async validDestino() {
      this.relocate = false
      if (this.destino) {
        const vdestino = this.destino.toUpperCase()
        if (
          vdestino.includes(this.selectedLoc.UBIX) ||
          vdestino.includes(this.selectedLoc.UBIXBC)
        ) {
          this.destinoDescrip = ''
          this.msgReloc = 'Ubicaciones de origen y destino sobrepuestas'
          this.msgColor = 'red'
          this.snackbar = true
          return true
        }

        const e = this.cantidad.empaq
        const u = this.cantidad.uni

        let cantidad = u

        if (this.selectedLoc.SEPARADOR) {
          const sep = this.selectedLoc.SEPARADOR
          cantidad = `${e} ${sep} ${u}`
        }

        await this.$axios
          .get('wms/relocatext/', {
            params: {
              p01: 'VALIDUBIX',
              p02: 'O',
              p03: this.preUBIX + this.destino.trim(),
              p04: cantidad,
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
                  this.relocate = true
                  this.msgReloc = 'UBICACION VALIDA'
                  this.destinoDescrip = msgerr
                } else {
                  this.relocate = false
                  this.destinoDescrip = ''
                }

                this.msgColor = numerr.startsWith('EOK') ? 'green' : 'red'
                this.snackbar = true
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
    async execRelocation() {
      const e = this.cantidad.empaq
      const u = this.cantidad.uni

      let cantidad = u

      if (this.selectedLoc.SEPARADOR) {
        const sep = this.selectedLoc.SEPARADOR
        cantidad = `${e} ${sep} ${u}`
      }

      if (this.destino) {
        await this.$axios
          .get('wms/relocatext/', {
            params: {
              p01: this.selectedLoc.SKU,
              p02: this.origen,
              p03: this.preUBIX + this.destino.trim(),
              p04: cantidad,
            },
          })
          .then((response) => {
            if (response.data) {
              if (response.data.length > 0) {
                const numerr = response.data[0].status.substring(0, 5)
                const msgerr = response.data[0].status.substring(6)
                this.msgReloc = msgerr
                this.msgColor = numerr.startsWith('EOK') ? 'green' : 'red'
                this.snackbar = true
              } else {
                this.msgReloc = 'SIN RESPUESTA DE LA BASE DE DATOS'
                this.msgColor = 'yellow'
                this.snackbar = true
              }
              this.cancelStepper()
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

      this.relocate = false
      this.btnkey++
    },
    cancelStepper() {
      // this.useBC1 = true
      // this.useBC2 = true
      this.productID = ''
      this.origen = ''
      this.destino = ''
      this.dataSource = null
      this.curSKU = '###'
      this.curUM = 'UNI'
      this.selectedKeys = []
      this.selectedLoc = {}
      this.cantSelectedLoc = { empaq: 0, uni: 0 }
      this.cantidad = { empaq: 0, uni: 0 }
      this.showEmpaques = false
      this.editSteps = { s1: true, s2: false, s3: false, s4: false }
      this.curStep = 1
      this.$nextTick(() => this.$refs.txtProdID.focus())
    },
  },
}
</script>

<style scoped>
.scroll {
  overflow-y: scroll;
}

.ubix-container {
  float: left;
  padding-top: 3px;
}

.ubix-container .ubix {
  font-weight: bold;
  font-size: 15px;
  color: rgb(136, 7, 33);
}

.ubix-container .ubixbc {
  font-size: 12px;
}

.stock-container {
  float: right;
  padding-top: 2px;
}

.stock-container > div {
  display: inline-block;
}

.stock-container .stock {
  font-size: 20px;
}

.stock-container .caption {
  font-size: 11px;
  line-height: 12px;
  padding-left: 6px;
  opacity: 0.7;
}
</style>
