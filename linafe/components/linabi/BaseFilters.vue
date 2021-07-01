/* eslint-disable no-console */
<template>
  <client-only>
    <v-dialog
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
            <v-toolbar-title>Filtros Iniciales</v-toolbar-title>
            <v-spacer />
            <v-btn icon @click="closeDialog(false)">
              <v-icon>mdi-window-close</v-icon>
            </v-btn>
          </v-toolbar>
          <v-container>
            <v-card-text>
              <template
                v-if="config.find((obj) => obj.configkey == 'filter15')"
              >
                <div
                  v-if="
                    config.find((obj) => obj.configkey == 'filter15')
                      .configval1 == '1'
                  "
                  class="px-2"
                >
                  <v-autocomplete
                    v-model="p15"
                    :rules="[rules.required]"
                    :items="items"
                    item-text="descrip"
                    item-value="key"
                    :label="
                      config.find((obj) => obj.configkey == 'filter15')
                        .configval2
                    "
                    clearable
                    dense
                  >
                  </v-autocomplete>
                </div>
              </template>
              <template
                v-if="config.find((obj) => obj.configkey == 'filter14')"
              >
                <div
                  v-show="
                    config.find((obj) => obj.configkey == 'filter14')
                      .configval1 == '1'
                  "
                  class="px-2"
                >
                  <v-radio-group v-model="p14" row class="my-0">
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
                        <div
                          v-show="
                            config.find((obj) => obj.configkey == 'filter01')
                              .configval1 == '1'
                          "
                        >
                          <v-text-field
                            v-model="p01"
                            :label="
                              config.find((obj) => obj.configkey == 'filter01')
                                .configval2
                            "
                            clearable
                            dense
                          ></v-text-field>
                        </div>
                      </template>
                      <template v-if="showExP1.f02">
                        <div
                          v-show="
                            config.find((obj) => obj.configkey == 'filter02')
                              .configval1 == '1'
                          "
                        >
                          <v-autocomplete
                            v-if="
                              config.find((obj) => obj.configkey == 'filter02')
                                .configval3 == '1'
                            "
                            v-model="p02"
                            :label="
                              config.find((obj) => obj.configkey == 'filter02')
                                .configval2
                            "
                            :items="
                              $store.getters[
                                'linabi/common/' +
                                  config.find(
                                    (obj) => obj.configkey == 'filter02'
                                  ).configval4
                              ]
                            "
                            item-text="NOMBRE"
                            item-value="ID"
                            multiple
                            chips
                            deletable-chips
                            clearable
                            dense
                          ></v-autocomplete>
                          <v-text-field
                            v-else
                            v-model="p02"
                            :label="
                              config.find((obj) => obj.configkey == 'filter02')
                                .configval2
                            "
                            clearable
                            dense
                          ></v-text-field>
                        </div>
                      </template>
                      <template v-if="showExP1.f03">
                        <div
                          v-show="
                            config.find((obj) => obj.configkey == 'filter03')
                              .configval1 == '1'
                          "
                        >
                          <v-autocomplete
                            v-if="
                              config.find((obj) => obj.configkey == 'filter03')
                                .configval3 == '1'
                            "
                            v-model="p03"
                            :label="
                              config.find((obj) => obj.configkey == 'filter03')
                                .configval2
                            "
                            :items="
                              $store.getters[
                                'linabi/common/' +
                                  config.find(
                                    (obj) => obj.configkey == 'filter03'
                                  ).configval4
                              ]
                            "
                            item-text="NOMBRE"
                            item-value="ID"
                            multiple
                            chips
                            deletable-chips
                            clearable
                            dense
                          ></v-autocomplete>
                          <v-text-field
                            v-else
                            v-model="p03"
                            :label="
                              config.find((obj) => obj.configkey == 'filter03')
                                .configval2
                            "
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
                        <div
                          v-show="
                            config.find((obj) => obj.configkey == 'filter04')
                              .configval1 == '1'
                          "
                        >
                          <v-autocomplete
                            v-if="
                              config.find((obj) => obj.configkey == 'filter04')
                                .configval3 == '1'
                            "
                            v-model="p04"
                            :label="
                              config.find((obj) => obj.configkey == 'filter04')
                                .configval2
                            "
                            :items="
                              $store.getters[
                                'linabi/common/' +
                                  config.find(
                                    (obj) => obj.configkey == 'filter04'
                                  ).configval4
                              ]
                            "
                            item-text="NOMBRE"
                            item-value="ID"
                            multiple
                            chips
                            deletable-chips
                            clearable
                            dense
                          ></v-autocomplete>
                          <v-text-field
                            v-else
                            v-model="p04"
                            :label="
                              config.find((obj) => obj.configkey == 'filter04')
                                .configval2
                            "
                            clearable
                            dense
                          ></v-text-field>
                        </div>
                      </template>
                      <template v-if="showExP2.f05">
                        <div
                          v-if="
                            config.find((obj) => obj.configkey == 'filter05')
                              .configval1 == '1'
                          "
                        >
                          <v-autocomplete
                            v-if="
                              config.find((obj) => obj.configkey == 'filter05')
                                .configval3 == '1'
                            "
                            v-model="p05"
                            :label="
                              config.find((obj) => obj.configkey == 'filter05')
                                .configval2
                            "
                            :items="
                              $store.getters[
                                'linabi/common/' +
                                  config.find(
                                    (obj) => obj.configkey == 'filter05'
                                  ).configval4
                              ]
                            "
                            item-text="NOMBRE"
                            item-value="ID"
                            multiple
                            chips
                            deletable-chips
                            clearable
                            dense
                          ></v-autocomplete>
                          <v-text-field
                            v-else
                            v-model="p05"
                            :label="
                              config.find((obj) => obj.configkey == 'filter05')
                                .configval2
                            "
                            clearable
                            dense
                          ></v-text-field>
                        </div>
                      </template>
                      <template v-if="showExP2.f06">
                        <div
                          v-show="
                            config.find((obj) => obj.configkey == 'filter06')
                              .configval1 == '1'
                          "
                        >
                          <v-autocomplete
                            v-if="
                              config.find((obj) => obj.configkey == 'filter06')
                                .configval3 == '1'
                            "
                            v-model="p06"
                            :label="
                              config.find((obj) => obj.configkey == 'filter06')
                                .configval2
                            "
                            :items="
                              $store.getters[
                                'linabi/common/' +
                                  config.find(
                                    (obj) => obj.configkey == 'filter06'
                                  ).configval4
                              ]
                            "
                            item-text="NOMBRE"
                            item-value="ID"
                            multiple
                            chips
                            deletable-chips
                            clearable
                            dense
                          ></v-autocomplete>
                          <v-text-field
                            v-else
                            v-model="p06"
                            :label="
                              config.find((obj) => obj.configkey == 'filter06')
                                .configval2
                            "
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
                        <div
                          v-show="
                            config.find((obj) => obj.configkey == 'filter07')
                              .configval1 == '1'
                          "
                        >
                          <v-autocomplete
                            v-if="
                              config.find((obj) => obj.configkey == 'filter07')
                                .configval3 == '1'
                            "
                            v-model="p07"
                            :label="
                              config.find((obj) => obj.configkey == 'filter07')
                                .configval2
                            "
                            :items="
                              $store.getters[
                                'linabi/common/' +
                                  config.find(
                                    (obj) => obj.configkey == 'filter07'
                                  ).configval4
                              ]
                            "
                            item-text="NOMBRE"
                            item-value="ID"
                            clearable
                            dense
                          ></v-autocomplete>
                          <v-text-field
                            v-else
                            v-model="p07"
                            :label="
                              config.find((obj) => obj.configkey == 'filter07')
                                .configval2
                            "
                            clearable
                            dense
                          ></v-text-field>
                        </div>
                      </template>
                      <template v-if="showExP3.f08">
                        <div
                          v-show="
                            config.find((obj) => obj.configkey == 'filter08')
                              .configval1 == '1'
                          "
                        >
                          <v-autocomplete
                            v-if="
                              config.find((obj) => obj.configkey == 'filter08')
                                .configval3 == '1'
                            "
                            v-model="p08"
                            :label="
                              config.find((obj) => obj.configkey == 'filter08')
                                .configval2
                            "
                            :items="
                              $store.getters[
                                'linabi/common/' +
                                  config.find(
                                    (obj) => obj.configkey == 'filter08'
                                  ).configval4
                              ]
                            "
                            item-text="NOMBRE"
                            item-value="ID"
                            clearable
                            dense
                          ></v-autocomplete>
                          <v-text-field
                            v-else
                            v-model="p08"
                            :label="
                              config.find((obj) => obj.configkey == 'filter08')
                                .configval2
                            "
                            clearable
                            dense
                          ></v-text-field>
                        </div>
                      </template>
                      <template v-if="showExP3.f09">
                        <div
                          v-show="
                            config.find((obj) => obj.configkey == 'filter09')
                              .configval1 == '1'
                          "
                        >
                          <v-autocomplete
                            v-if="
                              config.find((obj) => obj.configkey == 'filter09')
                                .configval3 == '1'
                            "
                            v-model="p09"
                            :label="
                              config.find((obj) => obj.configkey == 'filter09')
                                .configval2
                            "
                            :items="
                              $store.getters[
                                'linabi/common/' +
                                  config.find(
                                    (obj) => obj.configkey == 'filter09'
                                  ).configval4
                              ]
                            "
                            item-text="NOMBRE"
                            item-value="ID"
                            clearable
                            dense
                          ></v-autocomplete>
                          <v-text-field
                            v-else
                            v-model="p09"
                            :label="
                              config.find((obj) => obj.configkey == 'filter09')
                                .configval2
                            "
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
                      <template
                        v-if="config.find((obj) => obj.configkey == 'filter10')"
                      >
                        <div
                          v-show="
                            config.find((obj) => obj.configkey == 'filter10')
                              .configval1 == '1'
                          "
                        >
                          <v-text-field
                            v-model="p10"
                            :label="
                              config.find((obj) => obj.configkey == 'filter10')
                                .configval2
                            "
                            clearable
                            dense
                          ></v-text-field>
                        </div>
                      </template>
                      <template
                        v-if="config.find((obj) => obj.configkey == 'filter11')"
                      >
                        <div
                          v-show="
                            config.find((obj) => obj.configkey == 'filter11')
                              .configval1 == '1'
                          "
                        >
                          <v-checkbox
                            ref="activePeriod"
                            v-model="p11"
                            :true-value="1"
                            :false-value="0"
                            :label="
                              config.find((obj) => obj.configkey == 'filter11')
                                .configval2
                            "
                            class="my-0"
                            @change="periodDisabled"
                          >
                          </v-checkbox>
                        </div>
                      </template>
                      <v-row no-gutters>
                        <template
                          v-if="
                            config.find((obj) => obj.configkey == 'filter12')
                          "
                        >
                          <v-col
                            v-show="
                              config.find((obj) => obj.configkey == 'filter12')
                                .configval1 == '1'
                            "
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
                                  v-model="dateIni"
                                  :disabled="pD"
                                  :label="
                                    config.find(
                                      (obj) => obj.configkey == 'filter12'
                                    ).configval2
                                  "
                                  prepend-icon="mdi-calendar"
                                  clearable
                                  dense
                                  readonly
                                  v-bind="attrs"
                                  v-on="on"
                                ></v-text-field>
                              </template>
                              <v-date-picker
                                v-model="dateIni"
                                reactive
                                @input="menuDate1 = false"
                              ></v-date-picker>
                            </v-menu>
                          </v-col>
                        </template>
                        <template
                          v-if="
                            config.find((obj) => obj.configkey == 'filter13')
                          "
                        >
                          <v-col
                            v-show="
                              config.find((obj) => obj.configkey == 'filter13')
                                .configval1 == '1'
                            "
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
                                  v-model="dateEnd"
                                  :disabled="pD"
                                  :label="
                                    config.find(
                                      (obj) => obj.configkey == 'filter13'
                                    ).configval2
                                  "
                                  prepend-icon="mdi-calendar"
                                  clearable
                                  dense
                                  readonly
                                  v-bind="attrs"
                                  v-on="on"
                                ></v-text-field>
                              </template>
                              <v-date-picker
                                v-model="dateEnd"
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
              <v-btn
                block
                :disabled="!valid"
                color="success darken-1"
                type="submit"
                @click="closeDialog(true)"
              >
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
import { mapFields } from 'vuex-map-fields'
import { mapGetters } from 'vuex'

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
      ...mapFields(this.curstore, [
        'filters.p01',
        'filters.p02',
        'filters.p03',
        'filters.p04',
        'filters.p05',
        'filters.p06',
        'filters.p07',
        'filters.p08',
        'filters.p09',
        'filters.p10',
        'filters.p11',
        'filters.p12',
        'filters.p13',
        'filters.p14',
        'filters.p15',
      ]),
    }
    return {
      valid: true,
      items: [
        { key: 'COT', descrip: 'Cotizaciones' },
        { key: 'PEDCOT', descrip: 'Pedidos Cotizados' },
        { key: 'PEDCONF', descrip: 'Pedidos Confirmados' },
        { key: 'FAC', descrip: 'Facturas' },
      ],
      menuDate1: false,
      menuDate2: false,
      pD: false,
      dateIni: this.p12,
      dateEnd: this.p13,
      pp01: this.p01,
      pp02: this.p02,
      pp03: this.p03,
      pp04: this.p04,
      pp05: this.p05,
      pp06: this.p06,
      pp07: this.p07,
      pp08: this.p08,
      pp09: this.p09,
      verify: '',
      rules: {
        required: (value) => !!value || 'Requerido.',
        isEmpty: () =>
          this.checkEmpty() || 'Proporcione a menos un parámetro más',
      },
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
  },
  created() {
    const objfilter14 = this.config.find((obj) => obj.configkey === 'filter14')
    if (objfilter14) {
      this.p14 = objfilter14.configval3
    }

    const objfilter11 = this.config.find((obj) => obj.configkey === 'filter11')
    if (objfilter11) {
      const valf11 = objfilter11.configval3
      if (valf11 === '1') {
        this.p11 = 1
        this.pD = false
      } else {
        this.p11 = 0
        this.pD = true
      }
    }

    if (!this.listed) {
      this.$store.dispatch('linabi/common/setLists')
    }
  },
  methods: {
    reset() {
      this.$refs.bf_form.reset()
    },
    resetValidation() {
      this.$refs.bf_form.resetValidation()
    },
    closeDialog(refresh) {
      if (refresh) {
        if (this.$refs.bf_form.validate()) {
          this.$store.dispatch(this.curstore + '/setDates', {
            p12: this.dateIni,
            p13: this.dateEnd,
          })
          this.$emit('closeDialog', refresh)
        }
      } else {
        this.$emit('closeDialog', refresh)
      }
    },
    periodDisabled() {
      this.pD = !this.pD
    },
    checkEmpty() {
      let isEmpty = true
      const visibleFilters = []

      if (this.showExP1) {
        if (this.showExP1.panel) {
          if (this.showExP1.f01) {
            visibleFilters.push(this.p01)
          }
          if (this.showExP1.f02) {
            visibleFilters.push(this.p02)
          }
          if (this.showExP1.f03) {
            visibleFilters.push(this.p03)
          }
        }
      }

      if (this.showExP2) {
        if (this.showExP2.panel) {
          if (this.showExP2.f04) {
            visibleFilters.push(this.p04)
          }
          if (this.showExP2.f05) {
            visibleFilters.push(this.p05)
          }
          if (this.showExP2.f06) {
            visibleFilters.push(this.p06)
          }
        }
      }

      if (this.showExP3) {
        if (this.showExP3.panel) {
          if (this.showExP3.f07) {
            visibleFilters.push(this.p07)
          }
          if (this.showExP3.f08) {
            visibleFilters.push(this.p08)
          }
          if (this.showExP3.f09) {
            visibleFilters.push(this.p09)
          }
        }
      }

      if (this.showExP4) {
        if (this.showExP4.panel) {
          visibleFilters.push(this.dateIni)
          visibleFilters.push(this.dateEnd)
        }
      }

      console.log('VALOR VISIBLEFILTERS', visibleFilters)

      visibleFilters.forEach((obj) => {
        if (obj) {
          isEmpty = false
        }
      })

      return !isEmpty
    },
  },
}
</script>

<style lang="scss" scoped></style>
