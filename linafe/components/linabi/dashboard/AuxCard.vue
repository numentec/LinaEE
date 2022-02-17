/* eslint-disable no-console */
<template>
  <v-card
    class="mx-auto my-4"
    style="height: 100%"
    :loading="loadingView"
    :color="cardColor"
    dark
  >
    <v-card-title> {{ cardTitle }} </v-card-title>
    <v-card-subtitle> {{ curPeriodText }} </v-card-subtitle>
    <v-divider />
    <v-card-actions>
      <v-menu
        ref="dMenu"
        v-model="dateMenu"
        :close-on-content-click="false"
        :return-value.sync="curPeriod"
        transition="scale-transition"
        offset-x
        offset-y
        min-width="auto"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" color="white" v-on="on">
            <v-icon>mdi-calendar-refresh-outline</v-icon>
          </v-btn>
        </template>
        <v-date-picker
          v-model="curPeriod"
          range
          no-title
          scrollable
          locale="es-pa"
          :color="`${cardColor} lighten-1`"
        >
          <v-spacer></v-spacer>
          <v-btn text color="primary" @click="dateMenu = false">
            Cancelar
          </v-btn>
          <v-btn text color="primary" @click="updatePeriod"> Aceptar </v-btn>
        </v-date-picker>
      </v-menu>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex'
const startDate = new Date(new Date().getFullYear(), 0, 1)
  .toISOString()
  .substring(0, 10)
const endDate = new Date().toISOString().substring(0, 10)

export default {
  name: 'AuxCard',

  props: {
    cardTitle: {
      type: String,
      default: 'Dashboard element',
    },
    cardColor: {
      type: String,
      default: 'yellow',
    },
  },

  async fetch() {},

  data() {
    return {
      loadingView: false,
      perms: this.$auth.user.perms,
      dateMenu: false,
      curPeriod: [startDate, endDate],
    }
  },
  computed: {
    ...mapGetters('sistema', ['getCurCia']),
    curPeriodText() {
      return `Default period ${this.curPeriod.join(' ~ ')}`
    },
  },
  activated() {
    this.loadingView = false
  },
  methods: {
    updatePeriod() {
      this.$refs.dMenu.save(this.curPeriod)
    },
  },
}
</script>

<style scoped></style>
