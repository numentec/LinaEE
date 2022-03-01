/* eslint-disable no-console */
<template>
  <v-card class="mx-auto my-4" :loading="loadingView" :color="cardColor" dark>
    <v-card-title> {{ cardTitle }} </v-card-title>
    <v-divider />
    <v-card-title class="text-h4" v-text="dataSource"></v-card-title>
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
        <template v-slot:activator="{ on: menu, attrs }">
          <v-tooltip bottom>
            <template v-slot:activator="{ on: tooltip }">
              <v-btn icon v-bind="attrs" v-on="{ ...tooltip, ...menu }">
                <v-icon>mdi-calendar-refresh-outline</v-icon>
              </v-btn>
            </template>
            <span>Establecer periodo</span>
          </v-tooltip>
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
  name: 'VentasTot',

  props: {
    cardType: {
      type: String,
      default: 'V1',
    },
    cardId: {
      type: String,
      default: 'V1',
    },
    cardTitle: {
      type: String,
      default: 'Ventas del año',
    },
    cardColor: {
      type: String,
      default: 'green',
    },
  },

  async fetch() {
    if (this.curPeriod.length === 1) {
      this.curPeriod.push(this.curPeriod[0])
      this.$refs.dMenu.save(this.curPeriod)
    }

    const curparams = {
      p01: '0',
      p02: this.getCurCia.extrel,
      p03: this.curPeriod[0],
      p04: this.curPeriod[1],
    }

    this.loadingView = true

    await this.$axios
      .get('linabi/extbidashboard/', {
        params: curparams,
      })
      .then((response) => {
        let v = response.data[0][this.cardType]

        if (!v) {
          v = 0
        }

        this.dataSource = v.toLocaleString('en-US', {
          style: 'currency',
          currency: 'USD',
        })

        this.loadingView = false
      })
  },

  data() {
    return {
      loadingView: false,
      perms: this.$auth.user.perms,
      dataSource: '$0',
      dateMenu: false,
      curPeriod: [startDate, endDate],
    }
  },
  computed: {
    ...mapGetters('sistema', ['getCurCia']),
    curPeriodText() {
      // const fini = new Date(this.curPeriod[0] + 'T00:00:00').toLocaleDateString(
      //   'es-es'
      // )
      // const ffin = new Date(this.curPeriod[1] + 'T00:00:00').toLocaleDateString(
      //   'es-es'
      // )

      // return fini + ' ~ ' + ffin
      return this.curPeriod.join(' ~ ')
    },
  },
  activated() {
    this.loadingView = false
  },
  methods: {
    goView() {
      // this.loadingView = true
      // this.$router.push(this.el.link)
    },
    refreshData() {
      this.$fetch()
    },
    updatePeriod() {
      this.$refs.dMenu.save(this.curPeriod)
      this.refreshData()
    },
    formatLabel(pointInfo) {
      return `${pointInfo.valueText} (${pointInfo.percentText})`
    },
  },
}
</script>

<style lang="scss" scoped></style>
