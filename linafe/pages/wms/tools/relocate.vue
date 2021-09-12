<template>
  <div>
    <v-card class="px-0">
      <v-card-title>Reubicar producto</v-card-title>
      <v-stepper v-model="curStep" alt-labels flat>
        <v-stepper-header class="hidden-sm-and-down px-1">
          <v-stepper-step
            :complete="curStep > 1"
            step="1"
            :editable="editSteps.s1"
          >
            Producto
          </v-stepper-step>

          <v-stepper-step
            :complete="curStep > 2"
            step="2"
            :editable="editSteps.s2"
          >
            Origen
          </v-stepper-step>

          <v-stepper-step
            :complete="curStep > 3"
            step="3"
            :editable="editSteps.s3"
          >
            Cantidad
          </v-stepper-step>

          <v-stepper-step step="4" :editable="editSteps.s4">
            Destino
          </v-stepper-step>
        </v-stepper-header>

        <v-stepper-items>
          <v-stepper-content step="1" class="pa-0">
            <v-card class="mb-1 px-4" min-height="200px" flat tile>
              <v-switch v-model="useBC" label="Use Barcode"></v-switch>
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    ref="txtProdID"
                    v-model="productID"
                    :rules="[rules.required]"
                    :append-outer-icon="'mdi-send'"
                    clearable
                    :placeholder="
                      useBC ? 'Barcode de Producto' : 'SKU de Producto'
                    "
                    type="text"
                    @keydown.enter="findLocations"
                    @click:append-outer="findLocations"
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-card-actions>
                <v-btn color="primary" @click="cancelStepper">
                  <v-icon v-show="$vuetify.breakpoint.mobile">
                    mdi-cancel
                  </v-icon>
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
          </v-stepper-content>

          <v-stepper-content step="2" class="px-0">
            <v-card class="mb-1 px-4" min-height="200px" flat tile>
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
                    @keydown.enter="setOrigen"
                    @click:append-outer="setOrigen"
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <div class="mb-2">
                  <DxList
                    ref="locationsList"
                    :data-source="dataSource"
                    :search-enabled="true"
                    :search-editor-options="{ placeholder: 'Buscar' }"
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
              <v-card-actions>
                <v-btn color="primary" @click="cancelStepper">
                  <v-icon v-show="$vuetify.breakpoint.mobile">
                    mdi-cancel
                  </v-icon>
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
          </v-stepper-content>

          <v-stepper-content step="3" class="px-0">
            <v-card class="mb-1 px-4" min-height="200px" flat tile>
              <v-row>
                <v-col v-if="showEmpaques" :cols="6">
                  <v-text-field
                    ref="txtEmpaques"
                    v-model="cantidad.empaq"
                    :rules="[rules.isNumber]"
                    clearable
                    placeholder="Empaques"
                    label="Empaques"
                    type="text"
                    @focus="$event.target.select()"
                    @keydown.enter="setCantidad"
                  ></v-text-field>
                </v-col>
                <v-col :cols="showEmpaques ? 6 : 12">
                  <v-text-field
                    ref="txtUnidades"
                    v-model="cantidad.uni"
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
              <v-card-actions>
                <v-btn color="primary" @click="cancelStepper">
                  <v-icon v-show="$vuetify.breakpoint.mobile">
                    mdi-cancel
                  </v-icon>
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
          </v-stepper-content>

          <v-stepper-content step="4" class="px-0">
            <v-card class="mb-1 px-4" min-height="200px" flat tile>
              <v-switch v-model="useBC" label="Use Barcode"></v-switch>
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    ref="txtDestino"
                    v-model="destino"
                    :rules="[rules.required]"
                    :append-outer-icon="'mdi-send'"
                    clearable
                    :placeholder="useBC ? 'Destino (Barcode)' : 'Destino (ID)'"
                    type="text"
                    @keydown.enter="relocate"
                    @click:append-outer="relocate"
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-card-actions>
                <v-btn color="primary" @click="cancelStepper">
                  <v-icon v-show="$vuetify.breakpoint.mobile">
                    mdi-cancel
                  </v-icon>
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
          </v-stepper-content>
        </v-stepper-items>
      </v-stepper>
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
import MobileSteps from '~/components/utilities/MobileSteps'

export default {
  components: {
    DxList,
    MobileSteps,
  },
  data() {
    return {
      curStep: 1,
      useBC: true,
      productID: '',
      origen: '',
      destino: '',
      dataSource: null,
      selectedKeys: [],
      selectedLoc: {},
      cantSelectedLoc: { empaq: 0, uni: 0 },
      cantidad: { empaq: 0, uni: 0 },
      showEmpaques: false,
      editSteps: { s1: true, s2: false, s3: false, s4: false },
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
    async findLocations() {
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

            this.editSteps.s1 = true
            this.editSteps.s2 = true
            this.editSteps.s3 = false
            this.editSteps.s4 = false

            this.curStep = 2
            this.$nextTick(() => this.$refs.txtOrigen.focus())
          })
      }
    },
    onSelectionChanged(e) {
      const loc = e.addedItems[0]
      if (loc) {
        this.selectedLoc = JSON.parse(JSON.stringify(loc))
        this.origen = this.selectedLoc.UBIXBC

        if (this.selectedLoc.SEPARADOR) {
          const i = this.selectedLoc.CANT1.indexOf(this.selectedLoc.SEPARADOR)

          this.cantSelectedLoc.empaq = Number(
            this.selectedLoc.CANT1.substring(0, i - 1).trim()
          )
          this.cantSelectedLoc.uni = Number(
            this.selectedLoc.CANT1.substring(i + 1).trim()
          )

          this.showEmpaques = true
        } else {
          this.cantSelectedLoc.empaq = 0
          this.cantSelectedLoc.uni = Number(this.selectedLoc.CANT1.trim())
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
      if (!this.selectedKeys.includes(this.origen)) {
        this.selectedKeys = [...[], this.origen]
      }
    },
    setCantidad() {
      const e = this.cantSelectedLoc.empaq
      const u = this.cantSelectedLoc.uni
      const empaq = this.cantidad.empaq
      const uni = this.cantidad.uni
      if (empaq <= e && uni <= u) {
        this.editSteps.s4 = true
        this.curStep = 4
        this.$nextTick(() => this.$refs.txtDestino.focus())
      }
    },
    relocate() {
      this.msgReloc = 'Reubicación exitosa'
      this.msgColor = 'green'
      this.snackbar = true
    },
    cancelStepper() {
      this.useBC = true
      this.productID = ''
      this.origen = ''
      this.destino = ''
      this.dataSource = null
      this.selectedKeys = []
      this.selectedLoc = {}
      this.cantSelectedLoc = { empaq: 0, uni: 0 }
      this.cantidad = { empaq: 0, uni: 0 }
      this.showEmpaques = false
      this.editSteps = { s1: true, s2: false, s3: false, s4: false }
      this.curStep = 1
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
