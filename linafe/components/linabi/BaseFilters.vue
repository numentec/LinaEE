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
      <v-card>
        <v-toolbar color="accent lighten-3" dark>
          <v-toolbar-title>Filtros Iniciales</v-toolbar-title>
          <v-spacer />
          <v-btn icon @click="closeDialog(false)">
            <v-icon>mdi-window-close</v-icon>
          </v-btn>
        </v-toolbar>
        <v-container class="px-4">
          <v-card-text>
            <template v-if="config.find((obj) => obj.configkey == 'filter15')">
              <div
                v-show="
                  config.find((obj) => obj.configkey == 'filter15')
                    .configval1 == '1'
                "
              >
                <v-autocomplete
                  v-model="filters_to_apply.p15"
                  :items="items"
                  item-text="descrip"
                  item-value="key"
                  :label="
                    config.find((obj) => obj.configkey == 'filter15').configval2
                  "
                  clearable
                  dense
                >
                </v-autocomplete>
              </div>
            </template>
            <template v-if="config.find((obj) => obj.configkey == 'filter14')">
              <div
                v-show="
                  config.find((obj) => obj.configkey == 'filter14')
                    .configval1 == '1'
                "
              >
                <v-radio-group v-model="filters_to_apply.p14" row class="my-0">
                  <v-radio key="1" label="Todos" value="1"></v-radio>
                  <v-radio key="2" label="Disponible" value="2"></v-radio>
                  <v-radio key="3" label="Futuro" value="3"></v-radio>
                </v-radio-group>
                <v-divider></v-divider>
              </div>
            </template>
            <template v-if="config.find((obj) => obj.configkey == 'filter01')">
              <div
                v-show="
                  config.find((obj) => obj.configkey == 'filter01')
                    .configval1 == '1'
                "
              >
                <v-text-field
                  v-model="filters_to_apply.p01"
                  :label="
                    config.find((obj) => obj.configkey == 'filter01').configval2
                  "
                ></v-text-field>
              </div>
            </template>
            <template v-if="config.find((obj) => obj.configkey == 'filter02')">
              <div
                v-show="
                  config.find((obj) => obj.configkey == 'filter02')
                    .configval1 == '1'
                "
              >
                <v-text-field
                  v-model="filters_to_apply.p02"
                  :label="
                    config.find((obj) => obj.configkey == 'filter02').configval2
                  "
                  dense
                ></v-text-field>
              </div>
            </template>
            <template v-if="config.find((obj) => obj.configkey == 'filter03')">
              <div
                v-show="
                  config.find((obj) => obj.configkey == 'filter03')
                    .configval1 == '1'
                "
              >
                <v-text-field
                  v-model="filters_to_apply.p03"
                  :label="
                    config.find((obj) => obj.configkey == 'filter03').configval2
                  "
                  dense
                ></v-text-field>
              </div>
            </template>
            <template v-if="config.find((obj) => obj.configkey == 'filter04')">
              <div
                v-show="
                  config.find((obj) => obj.configkey == 'filter04')
                    .configval1 == '1'
                "
              >
                <v-text-field
                  v-model="filters_to_apply.p04"
                  :label="
                    config.find((obj) => obj.configkey == 'filter04').configval2
                  "
                  dense
                ></v-text-field>
              </div>
            </template>
            <template v-if="config.find((obj) => obj.configkey == 'filter05')">
              <div
                v-if="
                  config.find((obj) => obj.configkey == 'filter05')
                    .configval1 == '1'
                "
              >
                <v-text-field
                  v-model="filters_to_apply.p05"
                  :label="
                    config.find((obj) => obj.configkey == 'filter05').configval2
                  "
                  dense
                ></v-text-field>
              </div>
            </template>
            <v-expand-transition>
              <div v-show="morefilters">
                <template
                  v-if="config.find((obj) => obj.configkey == 'filter06')"
                >
                  <div
                    v-show="
                      config.find((obj) => obj.configkey == 'filter06')
                        .configval1 == '1'
                    "
                  >
                    <v-text-field
                      v-model="filters_to_apply.p06"
                      :label="
                        config.find((obj) => obj.configkey == 'filter06')
                          .configval2
                      "
                      dense
                    ></v-text-field>
                  </div>
                </template>
                <template
                  v-if="config.find((obj) => obj.configkey == 'filter07')"
                >
                  <div
                    v-show="
                      config.find((obj) => obj.configkey == 'filter07')
                        .configval1 == '1'
                    "
                  >
                    <v-text-field
                      v-model="filters_to_apply.p07"
                      :label="
                        config.find((obj) => obj.configkey == 'filter07')
                          .configval2
                      "
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
                    <v-text-field
                      v-model="filters_to_apply.p08"
                      :label="
                        config.find((obj) => obj.configkey == 'filter08')
                          .configval2
                      "
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
                    <v-text-field
                      v-model="filters_to_apply.p09"
                      :label="
                        config.find((obj) => obj.configkey == 'filter09')
                          .configval2
                      "
                      dense
                    ></v-text-field>
                  </div>
                </template>
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
                      v-model="filters_to_apply.p10"
                      :label="
                        config.find((obj) => obj.configkey == 'filter10')
                          .configval2
                      "
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
                      v-model="filters_to_apply.p11"
                      :label="
                        config.find((obj) => obj.configkey == 'filter11')
                          .configval2
                      "
                      class="my-0"
                    >
                    </v-checkbox>
                  </div>
                </template>

                <v-row no-gutters>
                  <template
                    v-if="config.find((obj) => obj.configkey == 'filter12')"
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
                            v-model="filters_to_apply.p12"
                            :disabled="periodDisabled"
                            :label="
                              config.find((obj) => obj.configkey == 'filter12')
                                .configval2
                            "
                            prepend-icon="mdi-calendar"
                            dense
                            readonly
                            v-bind="attrs"
                            v-on="on"
                          ></v-text-field>
                        </template>
                        <v-date-picker
                          v-model="filters_to_apply.p12"
                          @input="menuDate1 = false"
                        ></v-date-picker>
                      </v-menu>
                    </v-col>
                  </template>
                  <template
                    v-if="config.find((obj) => obj.configkey == 'filter13')"
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
                            v-model="filters_to_apply.p13"
                            :disabled="periodDisabled"
                            :label="
                              config.find((obj) => obj.configkey == 'filter13')
                                .configval2
                            "
                            prepend-icon="mdi-calendar"
                            dense
                            readonly
                            v-bind="attrs"
                            v-on="on"
                          ></v-text-field>
                        </template>
                        <v-date-picker
                          v-model="filters_to_apply.p13"
                          @input="menuDate2 = false"
                        ></v-date-picker>
                      </v-menu>
                    </v-col>
                  </template>
                </v-row>
              </div>
            </v-expand-transition>
          </v-card-text>
          <v-divider></v-divider>
          <v-row no-gutters>
            <v-col cols="12" sm="6" md="8">
              <v-card-actions>
                <v-btn
                  block
                  :disabled="!valid"
                  color="success"
                  @click="setFiltersAndClose"
                >
                  Aplicar
                </v-btn>
              </v-card-actions>
            </v-col>
            <v-col cols="6" md="4">
              <v-card-actions>
                <v-btn text color="grey" @click="morefilters = !morefilters">
                  Otros filtros
                  <v-icon right>{{
                    morefilters ? 'mdi-chevron-up' : 'mdi-chevron-down'
                  }}</v-icon>
                </v-btn>
              </v-card-actions>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </v-dialog>
  </client-only>
</template>

<script>
import { mapState, mapActions } from 'vuex'

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
  },

  data: () => ({
    valid: true,
    filters_to_apply: {
      p01: '',
      p02: '',
      p03: '',
      p04: '',
      p05: '',
      p06: '',
      p07: '',
      p08: '',
      p09: '',
      p10: '',
      p11: false,
      p12: '',
      p13: '',
      p14: '1',
      p15: '',
    },
    items: [
      { key: 'COT', descrip: 'Cotizaciones' },
      { key: 'PEDCOT', descrip: 'Pedidos Cotizados' },
      { key: 'PEDCONF', descrip: 'Pedidos Confirmados' },
      { key: 'FAC', descrip: 'Facturas' },
    ],
    menuDate1: false,
    menuDate2: false,
    morefilters: false,
    verify: '',
    rules: {
      required: (value) => !!value || 'Requerido.',
    },
  }),
  computed: {
    ...mapState('linabi', ['filters']),
    periodDisabled() {
      return !this.filters_to_apply.p11
    },
  },
  mounted() {
    if (this.numvista === 16) {
      this.filters_to_apply.p11 = true
    }
  },
  methods: {
    ...mapActions('linabi', ['setFilters']),
    reset() {
      this.$refs.basefilters_form.reset()
    },
    closeDialog(refresh) {
      this.$emit('closeDialog', refresh)
    },
    setFiltersAndClose() {
      this.setFilters(this.filters_to_apply)
      this.closeDialog(true)
    },
  },
}
</script>

<style lang="scss" scoped></style>
