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
      <v-form>
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
                  v-show="
                    config.find((obj) => obj.configkey == 'filter15')
                      .configval1 == '1'
                  "
                  class="px-2"
                >
                  <v-autocomplete
                    v-model="p15"
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
                  <v-expansion-panel>
                    <v-expansion-panel-header class="grey--text">
                      Maestro
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                      <template
                        v-if="config.find((obj) => obj.configkey == 'filter01')"
                      >
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
                      <template
                        v-if="config.find((obj) => obj.configkey == 'filter02')"
                      >
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
                      <template
                        v-if="config.find((obj) => obj.configkey == 'filter03')"
                      >
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
                  <v-expansion-panel v-show="showExP1">
                    <v-expansion-panel-header class="grey--text">
                      <v-row no-gutters>
                        <v-col cols="4">
                          <span><v-icon>mdi-filter-variant-plus</v-icon></span>
                        </v-col>
                        <v-col cols="8">
                          <span></span>
                        </v-col>
                      </v-row>
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                      <template
                        v-if="config.find((obj) => obj.configkey == 'filter04')"
                      >
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
                      <template
                        v-if="config.find((obj) => obj.configkey == 'filter05')"
                      >
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
                      <template
                        v-if="config.find((obj) => obj.configkey == 'filter06')"
                      >
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
                  <v-expansion-panel v-show="showExP2">
                    <v-expansion-panel-header class="grey--text">
                      <v-row no-gutters>
                        <v-col cols="4">
                          <span><v-icon>mdi-filter-variant-plus</v-icon></span>
                        </v-col>
                        <v-col cols="8">
                          <span></span>
                        </v-col>
                      </v-row>
                    </v-expansion-panel-header>
                    <v-expansion-panel-content>
                      <template
                        v-if="config.find((obj) => obj.configkey == 'filter07')"
                      >
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
                      <template
                        v-if="config.find((obj) => obj.configkey == 'filter08')"
                      >
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
                      <template
                        v-if="config.find((obj) => obj.configkey == 'filter09')"
                      >
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
                  <v-expansion-panel>
                    <v-expansion-panel-header class="grey--text">
                      Periodo
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

export default {
  name: 'BaseFilters',
  props: {
    dialog: Boolean,
    numvista: {
      type: Number,
      default: 0,
    },
    config: {
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
      verify: '',
      rules: {
        required: (value) => !!value || 'Requerido.',
      },
    }
  },
  computed: {
    showExP1() {
      let f04, f05, f06

      const objf04 = this.config.find((obj) => obj.configkey === 'filter04')
      if (objf04) {
        f04 = objf04.configval1 === '1'
      }
      const objf05 = this.config.find((obj) => obj.configkey === 'filter05')
      if (objf05) {
        f05 = objf05.configval1 === '1'
      }
      const objf06 = this.config.find((obj) => obj.configkey === 'filter06')
      if (objf06) {
        f06 = objf06.configval1 === '1'
      }
      return f04 || f05 || f06
    },
    showExP2() {
      let f07, f08, f09

      const objf07 = this.config.find((obj) => obj.configkey === 'filter07')
      if (objf07) {
        f07 = objf07.configval1 === '1'
      }
      const objf08 = this.config.find((obj) => obj.configkey === 'filter08')
      if (objf08) {
        f08 = objf08.configval1 === '1'
      }
      const objf09 = this.config.find((obj) => obj.configkey === 'filter09')
      if (objf09) {
        f09 = objf09.configval1 === '1'
      }
      return f07 || f08 || f09
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
      this.$refs.basefilters_form.reset()
    },
    closeDialog(refresh) {
      this.$store.dispatch(this.curstore + '/setDates', {
        p12: this.dateIni,
        p13: this.dateEnd,
      })
      this.$emit('closeDialog', refresh)
    },
    periodDisabled() {
      this.pD = !this.pD
    },
  },
}
</script>

<style lang="scss" scoped></style>
