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
              <v-list-item link @click="clearForm">
                <v-list-item-title>Limpiar</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-card-title>
        <v-card-text>
          <v-row dense>
            <!-- <v-col cols="3">
              <v-switch v-model="useBC1" label="BC" class="mx-2" />
            </v-col> -->
            <v-col cols="12">
              <v-text-field
                ref="txtMarbeteID"
                v-model="marbeteID"
                :rules="[rules.required]"
                :append-outer-icon="'mdi-send'"
                clearable
                label="Marbete"
                placeholder="Marbete"
                type="text"
                class="mx-2"
                @keydown.enter="loadMarbete"
                @click:append-outer="loadMarbete"
                @click:clear="clearForm"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <!-- <v-col cols="4" class="d-flex justify-center shrink">
              <ImgForGrid
                :img-file="curMarbete.FOTO"
                :swidth="100"
                :lwidth="200"
              />
            </v-col> -->
            <v-col cols>
              <v-row justify="start" align="center" dense>
                <v-card-title class="my-0 py-0 px-2">
                  {{ curMarbete.MARBETE }}
                </v-card-title>
              </v-row>
              <v-row justify="start" align="center" dense>
                <v-card-text class="my-0 pt-0 px-2">
                  <div class="text-subtitle-1">
                    {{ `SKU: ${curMarbete.SKU}` }}
                  </div>
                </v-card-text>
              </v-row>
              <v-row justify="start" align="center" dense>
                <v-card-text class="my-0 pt-0 px-2">
                  <div class="text-subtitle-1">
                    {{ curMarbete.DESCRIP }}
                  </div>
                </v-card-text>
              </v-row>
              <v-row justify="start" align="center" dense>
                <v-card-text class="my-0 py-0 px-2">
                  {{ curMarbete.BARCODE }}
                </v-card-text>
              </v-row>
              <v-row justify="start" align="center" dense>
                <v-card-title class="my-0 py-0 px-2">
                  {{ curMarbete.UBIX }}
                </v-card-title>
              </v-row>
              <v-row justify="start" align="center">
                <v-chip color="light-blue" text-color="white" class="mx-2">
                  {{ `Empaque: ${curMarbete.EMPAQUE}` }}
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
                x-small
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
                x-small
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
                x-small
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
                :label="`${curMarbete.UM} (Excepción)`"
                :placeholder="`${curMarbete.UM} (Excepción)`"
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
                x-small
                color="primary"
                :disabled="countDisabled"
                @click="countProds('minus')"
              >
                <v-icon>mdi-minus</v-icon>
              </v-btn>
            </v-col>
          </v-row>
          <v-divider></v-divider>
          <v-row justify="space-around" align="center" dense>
            <v-col cols="12" class="d-flex justify-center shrink">
              <v-btn
                class="ma-2"
                color="primary"
                :disabled="countDisabled"
                block
                rounded
                @click="clearForm"
              >
                {{ `Tot: ${curCount}` }}
                <v-icon right dark>mdi-check</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
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
              height="200"
              :grouped="true"
              :allow-item-deleting="true"
              item-delete-mode="slideItem"
            >
              <template #item="{ data: item }">
                <div>
                  <div class="conteo">
                    <div class="cuentasku">{{ `MAR: ${item.MARBETE}` }}</div>
                    <div class="cuentacant">{{ item.SKU }}</div>
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
import { locale, loadMessages } from 'devextreme/localization'
// import ImgForGrid from '~/components/utilities/ImgForGrid'

loadMessages({
  // Replace "en" with the target locale of the dictionary
  es: {
    'dxListEditDecorator-delete': 'Borrar',
    'dxListEditDecorator-more': 'Más',
  },
})

locale(navigator.language)

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

const marbete = {
  MARBETE: 0,
  SKU: '*****',
  BARCODE: '0000000000000',
  CODIGO: '0',
  DESCRIP: 'PRODUCT',
  UM: 'UNI', // Descripción de unidad de medida
  UMBC: '1', // Barcode o código de UM
  MULTIPLO: 1, // Múltiplo de UM
  EMPAQUE: '1',
  UBIX: 'UBIX',
  UBIXBC: 'UBIXBC',
  PACKAGEC: 0,
  PACKINGC: 0,
  PACKINGTOTC: 0,
  UNI: 0,
  PPP: 1, // Packings Per Package
  CTIME: getTime(),
  NUMINV: 0,
  FOTO: '/no_image.png',
  SEPARADOR: '/',
}

export default {
  components: {
    DxList,
    // ImgForGrid,
  },

  data() {
    return {
      useBC1: true,
      curMarbete: Object.assign({}, marbete),
      marbeteID: '',
      curIndex: -1,
      countDisabled: true,
      showConfig: false,
      showCount: false,
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
      selectedItem: 0,
      loadingView: false,
      rules: {
        required: (v) => !!v || 'Requerido',
        positiveNumber: (v) => v >= 0 || 'La cantidad no puede ser negativa',
      },
    }
  },
  computed: {
    ...mapGetters('sistema', ['getCurCia']),
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
        key: 'MARBETE',
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
    marbeteID(newVal) {
      if (!newVal) {
        this.clearForm()
      }
    },
  },
  mounted() {
    this.$nextTick(() => this.$refs.txtMarbeteID.focus())
  },
  methods: {
    async loadMarbete() {
      if (this.marbeteID) {
        const keyType = this.useBC1 ? 'BC' : 'ID'
        this.loadingView = true
        await this.$axios
          .get('wms/extmarbete/', {
            params: {
              p01: this.marbeteID,
              p02: keyType,
              p03: this.getCurCia.extrel,
            },
          })
          .then((response) => {
            if (response.data) {
              const data = response.data

              this.curMarbete = Object.assign({}, data[0])

              const cM = this.curMarbete.MARBETE

              let indx = -1

              if (this.listProdsCounted.length > 0) {
                indx = this.listProdsCounted.findIndex(
                  (obj) => obj.MARBETE === cM
                )

                if (indx >= 0) {
                  this.curIndex = indx
                  this.packageCount = this.listProdsCounted[indx].PACKAGEC
                  this.packingCount = this.listProdsCounted[indx].PACKINGC
                  this.uniCount = this.listProdsCounted[indx].UNI
                  this.packingPerPackage = this.listProdsCounted[indx].PPP
                }
              }

              // Add marbete to list
              if (indx < 0) {
                if (this.curIndex >= 0) {
                  const ptot =
                    this.packageCount + this.packingCount + this.uniCount

                  if (ptot === 0) {
                    this.listProdsCounted.splice(this.curIndex, 1)
                  }
                }

                indx = this.listProdsCounted.push(this.curMarbete) - 1
                this.curIndex = indx

                this.packingPerPackage = this.curMarbete.PPP
                this.packageCount = 0
                this.packingCount = 0
                this.uniCount = 0
              }

              this.countDisabled = false
            } else {
              this.countDisabled = true
              this.curIndex = -1
              this.curMarbete = Object.assign({}, marbete)
              this.packageCount = 0
              this.packingCount = 0
              this.uniCount = 0

              this.msgReloc = 'Error cargando marbete'
              this.msgColor = 'red'
              this.snackbar = true
            }

            this.loadingView = false
          })
          .catch((e) => {
            this.loadingView = false

            this.countDisabled = true
            this.curIndex = -1
            this.curMarbete = Object.assign({}, marbete)
            this.packageCount = 0
            this.packingCount = 0
            this.uniCount = 0

            this.msgReloc = e.response.data.detail
            this.msgColor = 'red'
            this.snackbar = true
          })
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
          cia: this.getCurCia.extrel,
        })
        .then((response) => {
          if (response.data) {
            this.msgReloc = response.data.msg // 'Cuenta enviada con éxito'
            this.msgColor = 'green'
            this.snackbar = true
            this.clearList()
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

      if (this.marbeteID !== '') this.marbeteID = ''
      // this.reset()
      this.resetValidation()

      this.curMarbete = Object.assign({}, marbete)
      // setTimeout(() => {
      this.packageCount = 0
      this.packingCount = 0
      this.uniCount = 0
      //   this.$refs.txtExcepCount.$refs.input.value = '0 / 0'
      // }, 0)
      this.countDisabled = true

      this.$refs.txtMarbeteID.scrollTop = 0
      // document.body.scrollIntoView({ behavior: 'smooth', block: 'start' })
      // window.scrollTo({ top: 0, behavior: 'smooth' })
      this.$nextTick(() => this.$refs.txtMarbeteID.focus())
    },
    clearList() {
      this.listProdsCounted = []
      this.curIndex = -1
      this.clearForm()
      this.askClearList = false
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
  font-size: 1.3rem;
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
  text-align: right;
  padding-top: 30px;
}
.dt-container > div {
  display: inline-block;
}
.dt-container .dt {
  font-size: 12px;
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
