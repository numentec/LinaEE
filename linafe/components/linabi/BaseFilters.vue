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
            <div v-show="config.find((obj) => obj.id == 14).configval1 == '1'">
              <v-radio-group v-model="filters_to_apply.p14" row class="my-0">
                <v-radio key="1" label="Todos" value="1"></v-radio>
                <v-radio key="2" label="Disponible" value="2"></v-radio>
                <v-radio key="3" label="Futuro" value="3"></v-radio>
              </v-radio-group>
              <v-divider></v-divider>
            </div>
            <div v-show="config.find((obj) => obj.id == 1).configval1 == '1'">
              <v-text-field
                v-model="filters_to_apply.p01"
                :label="config.find((obj) => obj.id == 1).configval2"
              ></v-text-field>
            </div>
            <div v-show="config.find((obj) => obj.id == 2).configval1 == '1'">
              <v-text-field
                v-model="filters_to_apply.p02"
                :label="config.find((obj) => obj.id == 2).configval2"
                dense
              ></v-text-field>
            </div>
            <div v-show="config.find((obj) => obj.id == 3).configval1 == '1'">
              <v-text-field
                v-model="filters_to_apply.p03"
                :label="config.find((obj) => obj.id == 3).configval2"
                dense
              ></v-text-field>
            </div>
            <div v-show="config.find((obj) => obj.id == 4).configval1 == '1'">
              <v-text-field
                v-model="filters_to_apply.p04"
                :label="config.find((obj) => obj.id == 4).configval2"
                dense
              ></v-text-field>
            </div>
            <div v-show="config.find((obj) => obj.id == 5).configval1 == '1'">
              <v-text-field
                v-model="filters_to_apply.p05"
                :label="config.find((obj) => obj.id == 5).configval2"
                dense
              ></v-text-field>
            </div>
            <v-expand-transition>
              <div v-show="morefilters">
                <div
                  v-show="config.find((obj) => obj.id == 6).configval1 == '1'"
                >
                  <v-text-field
                    v-model="filters_to_apply.p06"
                    :label="config.find((obj) => obj.id == 6).configval2"
                    dense
                  ></v-text-field>
                </div>
                <div
                  v-show="config.find((obj) => obj.id == 7).configval1 == '1'"
                >
                  <v-text-field
                    v-model="filters_to_apply.p07"
                    :label="config.find((obj) => obj.id == 7).configval2"
                    dense
                  ></v-text-field>
                </div>
                <div
                  v-show="config.find((obj) => obj.id == 8).configval1 == '1'"
                >
                  <v-text-field
                    v-model="filters_to_apply.p08"
                    :label="config.find((obj) => obj.id == 8).configval2"
                    dense
                  ></v-text-field>
                </div>
                <div
                  v-show="config.find((obj) => obj.id == 9).configval1 == '1'"
                >
                  <v-text-field
                    v-model="filters_to_apply.p09"
                    :label="config.find((obj) => obj.id == 9).configval2"
                    dense
                  ></v-text-field>
                </div>
                <div
                  v-show="config.find((obj) => obj.id == 10).configval1 == '1'"
                >
                  <v-text-field
                    v-model="filters_to_apply.p10"
                    :label="config.find((obj) => obj.id == 10).configval2"
                    dense
                  ></v-text-field>
                </div>
                <div
                  v-show="config.find((obj) => obj.id == 11).configval1 == '1'"
                >
                  <v-checkbox
                    v-model="filters_to_apply.p11"
                    :label="config.find((obj) => obj.id == 11).configval2"
                    class="my-0"
                  >
                  </v-checkbox>
                </div>
                <v-row no-gutters>
                  <v-col
                    v-show="
                      config.find((obj) => obj.id == 12).configval1 == '1'
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
                          :disabled="!filters_to_apply.p11"
                          :label="config.find((obj) => obj.id == 12).configval2"
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
                  <v-col
                    v-show="
                      config.find((obj) => obj.id == 13).configval1 == '1'
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
                          :disabled="!filters_to_apply.p11"
                          :label="config.find((obj) => obj.id == 13).configval2"
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
      p11: '',
      p12: '',
      p13: '',
      p14: '1',
      p15: '',
    },
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
  },
  mounted() {},
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
