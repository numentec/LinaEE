<template>
  <client-only>
    <v-dialog
      eager
      :value="dialog"
      persistent
      max-width="600px"
      min-width="360px"
      @input="$emit('update:dialog', false)"
      @keydown.esc="closeDialog(false)"
    >
      <v-form
        ref="bf_form"
        v-model="valid"
        lazy-validation
        @submit.prevent="closeDialog(true)"
      >
        <v-card>
          <v-toolbar color="accent darken-3" dark>
            <v-menu v-model="menuClear" :nudge-width="150" offset-y>
              <template v-slot:activator="{ on, attrs }">
                <v-btn dark icon v-bind="attrs" v-on="on">
                  <v-icon>mdi-dots-vertical</v-icon>
                </v-btn>
              </template>
              <v-list>
                <v-list-item link>
                  <v-list-item-icon>
                    <v-icon>mdi-text-box-remove-outline</v-icon>
                  </v-list-item-icon>
                  <v-list-item-title @click="reset">
                    Limpiar datos
                  </v-list-item-title>
                </v-list-item>
                <v-list-item link>
                  <v-list-item-icon>
                    <v-icon>mdi-autorenew</v-icon>
                  </v-list-item-icon>
                  <v-list-item-title @click="resetValidation"
                    >Reiniciar validación</v-list-item-title
                  >
                </v-list-item>
              </v-list>
            </v-menu>
            <v-toolbar-title>Filtros Iniciales</v-toolbar-title>
            <v-spacer />
            <v-btn icon @click="closeDialog(false)">
              <v-icon>mdi-window-close</v-icon>
            </v-btn>
          </v-toolbar>
          <v-container>
            <v-card-text>
              <template v-if="cfl['filter15']">
                <div v-if="cfl['filter15'].configval1 == '1'" class="px-2">
                  <v-autocomplete
                    v-model="fl.p15"
                    :rules="choiceRules(cfl['filter15'].configval5)"
                    :items="items"
                    item-text="descrip"
                    item-value="key"
                    :label="cfl['filter15'].configval2"
                    clearable
                    dense
                  >
                  </v-autocomplete>
                </div>
              </template>
              <template v-if="cfl['filter14']">
                <div v-show="cfl['filter14'].configval1 == '1'" class="px-2">
                  <v-radio-group v-model="fl.p14" row class="my-0">
                    <v-radio key="1" label="Todos" value="1"></v-radio>
                    <v-radio key="2" label="Disponible" value="2"></v-radio>
                    <v-radio key="3" label="Futuro" value="3"></v-radio>
                  </v-radio-group>
                  <v-divider></v-divider>
                </div>
              </template>
              <v-row justify="center">
                <v-expansion-panels accordion flat mandatory>
                  <v-expansion-panel v-show="showExP1.panel">
                    <v-expansion-panel-header class="grey--text">
                      <span>
                        <v-icon class="mr-2"> mdi-filter-outline </v-icon>
                        Maestro
                      </span>
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                      <template v-if="showExP1.f01">
                        <div v-show="cfl['filter01'].configval1 == '1'">
                          <v-text-field
                            v-model="fl.p01"
                            :rules="choiceRules(cfl['filter01'].configval5)"
                            :label="cfl['filter01'].configval2"
                            clearable
                            dense
                          ></v-text-field>
                        </div>
                      </template>
                      <template v-if="showExP1.f02">
                        <div v-show="cfl['filter02'].configval1 == '1'">
                          <v-autocomplete
                            v-if="cfl['filter02'].configval3 == '1'"
                            v-model="fl.p02"
                            :rules="choiceRules(cfl['filter02'].configval5)"
                            :label="cfl['filter02'].configval2"
                            :items="
                              $store.getters[
                                'linabi/common/' + cfl['filter02'].configval4
                              ]
                            "
                            item-text="NOMBRE"
                            item-value="ID"
                            multiple
                            chips
                            :counter="countChips"
                            deletable-chips
                            clearable
                            dense
                          ></v-autocomplete>
                          <v-text-field
                            v-else
                            v-model="fl.p02"
                            :rules="choiceRules(cfl['filter02'].configval5)"
                            :label="cfl['filter02'].configval2"
                            clearable
                            dense
                          ></v-text-field>
                        </div>
                      </template>
                      <template v-if="showExP1.f03">
                        <div v-show="cfl['filter03'].configval1 == '1'">
                          <v-autocomplete
                            v-if="cfl['filter03'].configval3 == '1'"
                            v-model="fl.p03"
                            :rules="choiceRules(cfl['filter03'].configval5)"
                            :label="cfl['filter03'].configval2"
                            :items="
                              $store.getters[
                                'linabi/common/' + cfl['filter03'].configval4
                              ]
                            "
                            item-text="NOMBRE"
                            item-value="ID"
                            multiple
                            chips
                            :counter="countChips"
                            deletable-chips
                            clearable
                            dense
                          ></v-autocomplete>
                          <v-text-field
                            v-else
                            v-model="fl.p03"
                            :rules="choiceRules(cfl['filter03'].configval5)"
                            :label="cfl['filter03'].configval2"
                            clearable
                            dense
                          ></v-text-field>
                        </div>
                      </template>
                    </v-expansion-panel-content>
                  </v-expansion-panel>
                  <v-expansion-panel v-show="showExP2.panel">
                    <v-expansion-panel-header class="grey--text">
                      <v-row no-gutters>
                        <v-col cols="4">
                          <span>
                            <v-icon class="mr-2">
                              mdi-filter-variant-plus
                            </v-icon>
                            Filtro 1
                          </span>
                        </v-col>
                        <v-col cols="8">
                          <span></span>
                        </v-col>
                      </v-row>
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                      <template v-if="showExP2.f04">
                        <div v-show="cfl['filter04'].configval1 == '1'">
                          <v-autocomplete
                            v-if="cfl['filter04'].configval3 == '1'"
                            v-model="fl.p04"
                            :rules="choiceRules(cfl['filter04'].configval5)"
                            :label="cfl['filter04'].configval2"
                            :items="
                              $store.getters[
                                'linabi/common/' + cfl['filter04'].configval4
                              ]
                            "
                            item-text="NOMBRE"
                            item-value="ID"
                            multiple
                            chips
                            :counter="3"
                            deletable-chips
                            clearable
                            dense
                          ></v-autocomplete>
                          <v-text-field
                            v-else
                            v-model="fl.p04"
                            :rules="choiceRules(cfl['filter04'].configval5)"
                            :label="cfl['filter04'].configval2"
                            clearable
                            dense
                          ></v-text-field>
                        </div>
                      </template>
                      <template v-if="showExP2.f05">
                        <div v-if="cfl['filter05'].configval1 == '1'">
                          <v-autocomplete
                            v-if="cfl['filter05'].configval3 == '1'"
                            v-model="fl.p05"
                            :rules="choiceRules(cfl['filter05'].configval5)"
                            :label="cfl['filter05'].configval2"
                            :items="
                              $store.getters[
                                'linabi/common/' + cfl['filter05'].configval4
                              ]
                            "
                            item-text="NOMBRE"
                            item-value="ID"
                            multiple
                            chips
                            :counter="3"
                            deletable-chips
                            clearable
                            dense
                          ></v-autocomplete>
                          <v-text-field
                            v-else
                            v-model="fl.p05"
                            :rules="choiceRules(cfl['filter05'].configval5)"
                            :label="cfl['filter05'].configval2"
                            clearable
                            dense
                          ></v-text-field>
                        </div>
                      </template>
                      <template v-if="showExP2.f06">
                        <div v-show="cfl['filter06'].configval1 == '1'">
                          <v-autocomplete
                            v-if="cfl['filter06'].configval3 == '1'"
                            v-model="fl.p06"
                            :rules="choiceRules(cfl['filter06'].configval5)"
                            :label="cfl['filter06'].configval2"
                            :items="
                              $store.getters[
                                'linabi/common/' + cfl['filter06'].configval4
                              ]
                            "
                            item-text="NOMBRE"
                            item-value="ID"
                            multiple
                            chips
                            :counter="3"
                            deletable-chips
                            clearable
                            dense
                          ></v-autocomplete>
                          <v-text-field
                            v-else
                            v-model="fl.p06"
                            :rules="choiceRules(cfl['filter06'].configval5)"
                            :label="cfl['filter06'].configval2"
                            clearable
                            dense
                          ></v-text-field>
                        </div>
                      </template>
                    </v-expansion-panel-content>
                  </v-expansion-panel>
                  <v-expansion-panel v-show="showExP3.panel">
                    <v-expansion-panel-header class="grey--text">
                      <v-row no-gutters>
                        <v-col cols="4">
                          <span>
                            <v-icon class="mr-2">
                              mdi-filter-variant-plus
                            </v-icon>
                            Filtro 2
                          </span>
                        </v-col>
                        <v-col cols="8"></v-col>
                      </v-row>
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                      <template v-if="showExP3.f07">
                        <div v-show="cfl['filter07'].configval1 == '1'">
                          <v-autocomplete
                            v-if="cfl['filter07'].configval3 == '1'"
                            v-model="fl.p07"
                            :rules="choiceRules(cfl['filter07'].configval5)"
                            :label="cfl['filter07'].configval2"
                            :items="
                              $store.getters[
                                'linabi/common/' + cfl['filter07'].configval4
                              ]
                            "
                            item-text="NOMBRE"
                            item-value="ID"
                            clearable
                            dense
                          ></v-autocomplete>
                          <v-text-field
                            v-else
                            v-model="fl.p07"
                            :rules="choiceRules(cfl['filter07'].configval5)"
                            :label="cfl['filter07'].configval2"
                            clearable
                            dense
                          ></v-text-field>
                        </div>
                      </template>
                      <template v-if="showExP3.f08">
                        <div v-show="cfl['filter08'].configval1 == '1'">
                          <v-autocomplete
                            v-if="cfl['filter08'].configval3 == '1'"
                            v-model="fl.p08"
                            :rules="choiceRules(cfl['filter08'].configval5)"
                            :label="cfl['filter08'].configval2"
                            :items="
                              $store.getters[
                                'linabi/common/' + cfl['filter08'].configval4
                              ]
                            "
                            item-text="NOMBRE"
                            item-value="ID"
                            clearable
                            dense
                          ></v-autocomplete>
                          <v-text-field
                            v-else
                            v-model="fl.p08"
                            :rules="choiceRules(cfl['filter08'].configval5)"
                            :label="cfl['filter08'].configval2"
                            clearable
                            dense
                          ></v-text-field>
                        </div>
                      </template>
                      <template v-if="showExP3.f09">
                        <div v-show="cfl['filter09'].configval1 == '1'">
                          <v-autocomplete
                            v-if="cfl['filter09'].configval3 == '1'"
                            v-model="fl.p09"
                            :rules="choiceRules(cfl['filter09'].configval5)"
                            :label="cfl['filter09'].configval2"
                            :items="
                              $store.getters[
                                'linabi/common/' + cfl['filter09'].configval4
                              ]
                            "
                            item-text="NOMBRE"
                            item-value="ID"
                            clearable
                            dense
                          ></v-autocomplete>
                          <v-text-field
                            v-else
                            v-model="fl.p09"
                            :rules="choiceRules(cfl['filter09'].configval5)"
                            :label="cfl['filter09'].configval2"
                            clearable
                            dense
                          ></v-text-field>
                        </div>
                      </template>
                    </v-expansion-panel-content>
                  </v-expansion-panel>
                  <v-expansion-panel v-show="showExP4.panel">
                    <v-expansion-panel-header class="grey--text">
                      <span>
                        <v-icon class="mr-2">mdi-calendar-range</v-icon>
                        Periodo
                      </span>
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                      <template v-if="cfl['filter10']">
                        <div v-show="cfl['filter10'].configval1 == '1'">
                          <v-text-field
                            v-model="fl.p10"
                            :rules="choiceRules(cfl['filter10'].configval5)"
                            :label="cfl['filter10'].configval2"
                            clearable
                            dense
                          ></v-text-field>
                        </div>
                      </template>
                      <template v-if="cfl['filter11']">
                        <div v-show="cfl['filter11'].configval1 == '1'">
                          <v-checkbox
                            ref="activePeriod"
                            v-model="fl.p11"
                            :true-value="1"
                            :false-value="0"
                            :label="cfl['filter11'].configval2"
                            class="my-0"
                            @change="periodDisabled"
                          >
                          </v-checkbox>
                        </div>
                      </template>
                      <v-row no-gutters>
                        <template v-if="cfl['filter12']">
                          <v-col
                            v-show="cfl['filter12'].configval1 == '1'"
                            cols="6"
                          >
                            <v-menu
                              v-model="menuDate1"
                              :close-on-content-click="false"
                              :nudge-right="40"
                              transition="scale-transition"
                              offset-y
                              min-width="auto"
                            >
                              <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                  v-model="fl.p12"
                                  :disabled="pD"
                                  :label="cfl['filter12'].configval2"
                                  prepend-icon="mdi-calendar"
                                  clearable
                                  dense
                                  readonly
                                  v-bind="attrs"
                                  v-on="on"
                                ></v-text-field>
                              </template>
                              <v-date-picker
                                v-model="fl.p12"
                                reactive
                                @input="menuDate1 = false"
                              ></v-date-picker>
                            </v-menu>
                          </v-col>
                        </template>
                        <template v-if="cfl['filter13']">
                          <v-col
                            v-show="cfl['filter13'].configval1 == '1'"
                            cols="6"
                          >
                            <v-menu
                              v-model="menuDate2"
                              :close-on-content-click="false"
                              :nudge-right="40"
                              transition="scale-transition"
                              offset-y
                              min-width="auto"
                            >
                              <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                  v-model="fl.p13"
                                  :disabled="pD"
                                  :label="cfl['filter13'].configval2"
                                  prepend-icon="mdi-calendar"
                                  clearable
                                  dense
                                  readonly
                                  v-bind="attrs"
                                  v-on="on"
                                ></v-text-field>
                              </template>
                              <v-date-picker
                                v-model="fl.p13"
                                @input="menuDate2 = false"
                              ></v-date-picker>
                            </v-menu>
                          </v-col>
                        </template>
                      </v-row>
                    </v-expansion-panel-content>
                  </v-expansion-panel>
                </v-expansion-panels>
              </v-row>
            </v-card-text>
            <v-divider></v-divider>
            <v-card-actions>
              <v-btn block color="success darken-1" type="submit">
                Aplicar
              </v-btn>
            </v-card-actions>
          </v-container>
        </v-card>
      </v-form>
    </v-dialog>
  </client-only>
</template>

<script>
import { mapGetters } from 'vuex'
const countChips = 7

const rules = {
  required: true || 'Requerido.',
  isEmpty: true || 'Proporcione al menos un parámetro más',
  maxchips: true || 'Max selection 7',
  checkPeriod: true || 'Proporcione un periodo correcto',
}

function objIsEmpty(obj) {
  let isEmpty = true

  if (obj) {
    if (Array.isArray(obj)) {
      if (obj.length > 0) {
        isEmpty = false
      }
    }
    if (typeof obj === 'string') {
      if (obj.trim !== '') {
        isEmpty = false
      }
    }
  }

  return isEmpty
}

function clearProps(obj) {
  Object.keys(obj).forEach((key) => {
    if (obj[key]) {
      if (Array.isArray(obj[key])) {
        if (obj[key].length === 0) {
          delete obj[key]
        }
      }
      if (typeof obj[key] === 'string') {
        if (obj[key].trim === '') {
          delete obj[key]
        }
      }
    }
  })

  return obj
}

export default {
  name: 'BaseFilters',
  props: {
    dialog: Boolean,
    curView: {
      type: Object,
      default: () => {
        return {
          num: 0,
          checkelperms: true,
        }
      },
    },
    config: {
      type: Array,
      default: () => [{}],
    },
    perms: {
      type: Array,
      default: () => [{}],
    },
    curstore: {
      type: String,
      default: '',
    },
  },

  data() {
    this.$options.computed = {
      ...this.$options.computed,
      ...mapGetters(['loggedInUser']),
      ...mapGetters(this.curstore, ['getFilters']),
    }
    return {
      valid: true,
      items: [
        { key: 'COT', descrip: 'Cotizaciones' },
        { key: 'PEDCOT', descrip: 'Pedidos Cotizados' },
        { key: 'PEDCONF', descrip: 'Pedidos Confirmados' },
        { key: 'FAC', descrip: 'Facturas' },
      ],
      menuClear: false,
      menuDate1: false,
      menuDate2: false,
      pD: false,
      fl: {},
      verify: '',
      countChips,
      rules,
    }
  },
  computed: {
    showExP1() {
      let f01, f02, f03

      const objf01 = this.config.find((obj) => obj.configkey === 'filter01')
      if (objf01) {
        f01 = objf01.configval1 === '1'
        if (f01) {
          if (!this.loggedInUser.is_superuser && this.curView.checkelperms) {
            const permf01 = this.perms.find(
              (obj) => obj.configkey === 'filter01'
            )
            if (permf01) {
              f01 = permf01.acceso
            } else {
              f01 = false
            }
          }
        }
      }
      const objf02 = this.config.find((obj) => obj.configkey === 'filter02')
      if (objf02) {
        f02 = objf02.configval1 === '1'
        if (f02) {
          if (!this.loggedInUser.is_superuser && this.curView.checkelperms) {
            const permf02 = this.perms.find(
              (obj) => obj.configkey === 'filter02'
            )
            if (permf02) {
              f02 = permf02.acceso
            } else {
              f02 = false
            }
          }
        }
      }
      const objf03 = this.config.find((obj) => obj.configkey === 'filter03')
      if (objf03) {
        f03 = objf03.configval1 === '1'
        if (f03) {
          if (!this.loggedInUser.is_superuser && this.curView.checkelperms) {
            const permf03 = this.perms.find(
              (obj) => obj.configkey === 'filter03'
            )
            if (permf03) {
              f03 = permf03.acceso
            } else {
              f03 = false
            }
          }
        }
      }
      return {
        panel: f01 || f02 || f03,
        f01,
        f02,
        f03,
      }
    },
    showExP2() {
      let f04, f05, f06

      const objf04 = this.config.find((obj) => obj.configkey === 'filter04')
      if (objf04) {
        f04 = objf04.configval1 === '1'
        if (f04) {
          if (!this.loggedInUser.is_superuser && this.curView.checkelperms) {
            const permf04 = this.perms.find(
              (obj) => obj.configkey === 'filter04'
            )
            if (permf04) {
              f04 = permf04.acceso
            } else {
              f04 = false
            }
          }
        }
      }
      const objf05 = this.config.find((obj) => obj.configkey === 'filter05')
      if (objf05) {
        f05 = objf05.configval1 === '1'
        if (f05) {
          if (!this.loggedInUser.is_superuser && this.curView.checkelperms) {
            const permf05 = this.perms.find(
              (obj) => obj.configkey === 'filter05'
            )
            if (permf05) {
              f05 = permf05.acceso
            } else {
              f05 = false
            }
          }
        }
      }
      const objf06 = this.config.find((obj) => obj.configkey === 'filter06')
      if (objf06) {
        f06 = objf06.configval1 === '1'
        if (f06) {
          if (!this.loggedInUser.is_superuser && this.curView.checkelperms) {
            const permf06 = this.perms.find(
              (obj) => obj.configkey === 'filter06'
            )
            if (permf06) {
              f06 = permf06.acceso
            } else {
              f06 = false
            }
          }
        }
      }
      return {
        panel: f04 || f05 || f06,
        f04,
        f05,
        f06,
      }
    },
    showExP3() {
      let f07 = false
      let f08 = false
      let f09 = false

      const objf07 = this.config.find((obj) => obj.configkey === 'filter07')
      if (objf07) {
        f07 = objf07.configval1 === '1'
        if (f07) {
          if (!this.loggedInUser.is_superuser && this.curView.checkelperms) {
            const permf07 = this.perms.find(
              (obj) => obj.configkey === 'filter07'
            )
            if (permf07) {
              f07 = permf07.acceso
            } else {
              f07 = false
            }
          }
        }
      }
      const objf08 = this.config.find((obj) => obj.configkey === 'filter08')
      if (objf08) {
        f08 = objf08.configval1 === '1'
        if (f08) {
          if (!this.loggedInUser.is_superuser && this.curView.checkelperms) {
            const permf08 = this.perms.find(
              (obj) => obj.configkey === 'filter08'
            )
            if (permf08) {
              f08 = permf08.acceso
            } else {
              f08 = false
            }
          }
        }
      }
      const objf09 = this.config.find((obj) => obj.configkey === 'filter09')
      if (objf09) {
        f09 = objf09.configval1 === '1'
        if (f09) {
          if (!this.loggedInUser.is_superuser && this.curView.checkelperms) {
            const permf09 = this.perms.find(
              (obj) => obj.configkey === 'filter09'
            )
            if (permf09) {
              f09 = permf09.acceso
            } else {
              f09 = false
            }
          }
        }
      }
      return {
        panel: f07 || f08 || f09,
        f07,
        f08,
        f09,
      }
    },
    showExP4() {
      let f11 = false

      const objf11 = this.config.find((obj) => obj.configkey === 'filter11')
      if (objf11) {
        f11 = objf11.configval1 === '1'
        if (f11) {
          if (!this.loggedInUser.is_superuser && this.curView.checkelperms) {
            const permf11 = this.perms.find(
              (obj) => obj.configkey === 'filter11'
            )
            if (permf11) {
              f11 = permf11.acceso
            } else {
              f11 = false
            }
          }
        }
      }

      return { panel: f11 }
    },
    cfl() {
      // Object filter configuration
      const conf = this.config.reduce((obj, item) => {
        obj[item.configkey] = item
        return obj
      }, {})
      return conf
    },
  },
  watch: {
    // when dialog shown or hidden
    shown() {
      this.rules = rules
      // this.$refs.form.reset()
    },
  },
  created() {
    const objfilter14 = this.cfl.filter14
    if (objfilter14) {
      this.fl.p14 = objfilter14.configval3
    }

    const objfilter11 = this.cfl.filter11
    if (objfilter11) {
      const valf11 = objfilter11.configval3
      if (valf11 === '1') {
        this.fl.p11 = 1
        this.pD = false
      } else {
        this.fl.p11 = 0
        this.pD = true
      }
    }

    if (!this.listed) {
      this.$store.dispatch('linabi/common/setLists')
    }
  },
  mounted() {
    if (Object.keys(this.getFilters).length > 0) {
      Object.assign(this.fl, this.getFilters)
    }
  },
  methods: {
    reset() {
      this.$refs.bf_form.reset()
    },
    resetValidation() {
      this.$refs.bf_form.resetValidation()
    },
    choiceRules(indexes) {
      const indxs = Array.from(indexes).map(Number)

      const arrayRules = [
        this.rules.required,
        this.rules.isEmpty,
        this.rules.maxchips,
        this.rules.checkPeriod,
      ]

      const selectedRules = arrayRules.filter((e, i) => indxs.includes(i))

      return selectedRules
    },
    closeDialog(refresh) {
      if (refresh) {
        this.rules = {
          required: (v) => !!v || 'Requerido.',
          isEmpty: () =>
            this.checkEmpty() || 'Proporcione al menos un parámetro más',
          maxchips: (v) =>
            (v ? v.length <= countChips : true) || 'Max selection 7',
          checkPeriod: (v) =>
            ((v ? v.length > 0 : false) ? this.checkPeriod(v) : true) ||
            'Proporcione un periodo válido',
        }
        this.$nextTick(() => {
          if (this.$refs.bf_form.validate()) {
            const clearfl = clearProps(this.fl)
            // const objfl = JSON.parse(JSON.stringify(clearfl))
            this.$store.dispatch(this.curstore + '/setFilters', clearfl)
            this.$emit('closeDialog', refresh)
          }
        })
      } else {
        this.$emit('closeDialog', refresh)
      }
    },
    periodDisabled() {
      this.pD = !this.pD
    },
    checkEmpty() {
      let isEmpty = true

      if (this.showExP1) {
        if (this.showExP1.panel) {
          if (this.showExP1.f01) {
            if (!objIsEmpty(this.fl.p01)) {
              isEmpty = false
            }
          }
          if (this.showExP1.f02) {
            if (!objIsEmpty(this.fl.p02)) {
              isEmpty = false
            }
          }
          if (this.showExP1.f03) {
            if (!objIsEmpty(this.fl.p03)) {
              isEmpty = false
            }
          }
        }
      }

      if (this.showExP2) {
        if (this.showExP2.panel) {
          if (this.showExP2.f04) {
            if (!objIsEmpty(this.fl.p04)) {
              isEmpty = false
            }
          }
          if (this.showExP2.f05) {
            if (!objIsEmpty(this.fl.p05)) {
              isEmpty = false
            }
          }
          if (this.showExP2.f06) {
            if (!objIsEmpty(this.fl.p06)) {
              isEmpty = false
            }
          }
        }
      }

      if (this.showExP3) {
        if (this.showExP3.panel) {
          if (this.showExP3.f07) {
            if (!objIsEmpty(this.fl.p07)) {
              isEmpty = false
            }
          }
          if (this.showExP3.f08) {
            if (!objIsEmpty(this.fl.p08)) {
              isEmpty = false
            }
          }
          if (this.showExP3.f09) {
            if (!objIsEmpty(this.fl.p09)) {
              isEmpty = false
            }
          }
        }
      }

      if (this.showExP4) {
        if (this.showExP4.panel) {
          if (!objIsEmpty(this.fl.p12) && !objIsEmpty(this.fl.p13)) {
            isEmpty = false
          }
        }
      }

      return !isEmpty
    },
    checkPeriod(v) {
      let hasPeriod = true
      if (this.showExP4) {
        if (this.showExP4.panel) {
          if (this.fl.p11) {
            if (objIsEmpty(this.fl.p12) || objIsEmpty(this.fl.p13)) {
              hasPeriod = false
            }
          }
        }
      }
      return hasPeriod
    },
  },
}
</script>

<style lang="scss" scoped></style>
