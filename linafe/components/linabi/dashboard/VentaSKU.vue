/* eslint-disable no-console */
<template>
  <v-card
    class="mx-auto my-4"
    style="height: 100%"
    :loading="loadingView"
    color="cyan"
    dark
  >
    <v-app-bar flat dense dark color="cyan">
      <v-toolbar-title class="text-h6 white--text pl-0">
        Ventas por SKU
      </v-toolbar-title>
      <v-card-subtitle>{{ curPeriodText }}</v-card-subtitle>
      <v-spacer></v-spacer>
      <v-menu
        ref="menuConf"
        v-model="menuConfig"
        :close-on-content-click="false"
        transition="scale-transition"
        min-width="auto"
        left
        offset-y
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" v-on="on">
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>
        <v-list nav>
          <v-list-item link @click="goView">
            <v-list-item-icon>
              <v-icon>mdi-open-in-new</v-icon>
            </v-list-item-icon>
            <v-list-item-title> Ir a detalle </v-list-item-title>
          </v-list-item>
          <v-list-group prepend-icon="mdi-export" no-action>
            <template v-slot:activator>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>Exportar</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </template>
            <v-list-item link>
              <v-list-item-content>
                <v-list-item-title @click.stop="exportGrid(1)">
                  Excel
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item link>
              <v-list-item-content>
                <v-list-item-title @click.stop="exportGrid(2)">
                  PDF
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list-group>
          <v-list-item>
            <v-list-item-action>
              <v-switch v-model="selQry"></v-switch>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>SKUs de menor venta</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>
    <v-divider />
    <v-card-text>
      <DxDataGrid
        :data-source="dataSource"
        :remote-operations="false"
        :allow-column-reordering="true"
        :row-alternation-enabled="true"
        :show-borders="true"
        :focused-row-enabled="true"
        :column-auto-width="true"
        :allow-column-resizing="true"
        column-resizing-mode="widget"
        :show-column-lines="true"
        :show-row-lines="false"
        :hover-state-enabled="true"
      >
        <DxColumn data-field="SKU" data-type="string" />
        <DxColumn
          data-field="DESCRIP"
          data-type="string"
          caption="Descripción"
        />
        <DxColumn data-field="UM" data-type="string" />
        <template v-for="i in [1, 2, 3, 4]">
          <DxColumn
            :key="i"
            :data-field="`T${i}V`"
            data-type="number"
            format="#,##0.00"
            alignment="right"
            :caption="`T${i}`"
          />
        </template>
        <DxColumn
          data-field="TOT"
          data-type="number"
          format="#,##0.00"
          alignment="right"
          caption="Total"
        />
        <DxPager
          :allowed-page-sizes="[5, 10, 20]"
          :show-page-size-selector="true"
        />
        <DxPaging :page-size="psize" />
      </DxDataGrid>
    </v-card-text>

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
          color="blue lighten-1"
        >
          <v-spacer></v-spacer>
          <v-btn text color="primary" @click="dateMenu = false">
            Cancelar
          </v-btn>
          <v-btn text color="primary" @click="updatePeriod"> Aceptar </v-btn>
        </v-date-picker>
      </v-menu>
      <v-spacer></v-spacer>
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon color="white" v-bind="attrs" v-on="on" @click="goView">
            <v-icon>mdi-open-in-new</v-icon>
          </v-btn>
        </template>
        <span>Ir a detalle</span>
      </v-tooltip>
    </v-card-actions>
    <v-overlay :absolute="true" :value="$fetchState.pending">
      <v-progress-circular indeterminate size="64"></v-progress-circular>
    </v-overlay>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex'
import {
  DxDataGrid,
  DxColumn,
  DxPager,
  DxPaging,
} from 'devextreme-vue/data-grid'
import DataSource from 'devextreme/data/data_source'

const startDate = new Date(new Date().getFullYear(), 0, 1)
  .toISOString()
  .substring(0, 10)
const endDate = new Date().toISOString().substring(0, 10)

export default {
  name: 'VentaSKU',

  components: {
    DxDataGrid,
    DxColumn,
    DxPager,
    DxPaging,
  },
  props: {},

  async fetch() {
    if (this.curPeriod.length === 1) {
      this.curPeriod.push(this.curPeriod[0])
      this.$refs.dMenu.save(this.curPeriod)
    }

    const curparams = {
      p01: this.selQry ? 12 : 11,
      p02: this.getCurCia.extrel,
      p03: this.curPeriod[0],
      p04: this.curPeriod[1],
      p05: 100,
    }

    this.loadingView = true

    await this.$axios
      .get('linabi/extbidashboard/', {
        params: curparams,
      })
      .then((response) => {
        // this.dataSource = response.data

        this.dataSource = new DataSource({
          store: {
            type: 'array',
            key: 'SKU',
            data: response.data,
          },
        })

        this.loadingView = false
      })
  },

  data() {
    return {
      selQry: false,
      loadingView: false,
      perms: this.$auth.user.perms,
      dataSource: null,
      umbral: 0,
      curPeriod: [startDate, endDate],
      dateMenu: false,
      menuConfig: false,
      psize: 10,
      path: '/linabi/dashboardqueries/skusales/',
    }
  },
  computed: {
    ...mapGetters('sistema', ['getCurCia']),
    curPeriodText() {
      return this.curPeriod.join(' ~ ')
    },
    setTitle() {
      const title = {
        text: 'Ventas por mes',
        subtitle: {
          text: this.curPeriodText,
          font: {
            color: 'gray',
            opacity: 0.9,
          },
        },
      }

      return title
    },
  },
  activated() {
    this.loadingView = false
  },
  methods: {
    refreshData() {
      this.$fetch()
    },
    updatePeriod() {
      this.$refs.dMenu.save(this.curPeriod)
      this.refreshData()
    },
    exportGrid(opc) {
      this.menuConfig = false
    },
    goView() {
      const curPeriod = this.curPeriod
      this.$emit('goView', {
        argField: 'SKU',
        curPeriod,
        path: '/linabi/dashboardqueries/skusales/',
      })
      // this.$router.push('/linabi/dashboardqueries/skusales/')
    },
  },
}
</script>

<style scoped>
.tooltip-header {
  margin-bottom: 5px;
  font-size: 16px;
  font-weight: 500;
  padding-bottom: 5px;
  border-bottom: 1px solid #c5c5c5;
}

.tooltip-body {
  width: 170px;
}

.tooltip-body .series-name {
  font-weight: normal;
  opacity: 0.6;
  display: inline-block;
  line-height: 1.5;
  padding-right: 10px;
  width: 126px;
}

.tooltip-body .value-text {
  display: inline-block;
  line-height: 1.5;
  width: 30px;
}
</style>
