<template>
  <v-app dark>
    <CoreAppBar />
    <component :is="useDrawer" />
    <v-main>
      <v-container>
        <nuxt keep-alive :keep-alive-props="{ exclude: ['modal'] }" />
      </v-container>
    </v-main>
    <v-bottom-navigation :value="mobileNav" color="primary" grow fixed app>
      <v-btn @click="goHome">
        <span>Inicio</span>

        <v-icon>mdi-home</v-icon>
      </v-btn>

      <v-btn @click="qTools">
        <span>Quick Tools</span>

        <v-icon>mdi-tools</v-icon>
      </v-btn>

      <v-btn @click="goFav">
        <span>Favoritos</span>

        <v-icon color="yellow darken-2">mdi-star</v-icon>
      </v-btn>
    </v-bottom-navigation>
    <DxActionSheet
      v-model="isActionSheetVisible"
      :data-source="dataSource"
      :visible="isActionSheetVisible"
      :show-title="false"
      :show-cancel-button="true"
      cancel-text="Cancelar"
      title="Quick tools"
      @cancelClick="isActionSheetVisible = false"
      @itemClick="loadTool($event.itemData)"
    />
    <!-- <v-footer v-else color="asgrey lighten-3" fixed app>
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer> -->
  </v-app>
</template>

<script>
import DxActionSheet from 'devextreme-vue/action-sheet'
const CoreDrawer = () => import('../components/core/Drawer')
const CoreDrawerMobile = () => import('../components/core/DrawerMobile')

export default {
  name: 'LinaHome',
  components: {
    CoreAppBar: () => import('../components/core/AppBar'),
    DxActionSheet,
  },
  data() {
    return {
      mobileNav: 0,
      bar: true,
      dataSource: [
        {
          text: 'Producto - Consultar',
          onClick: () => {
            this.$router.push({ path: '/ventas/tools/qryprod' })
          },
        },
        {
          text: 'Producto - Ubicaciones',
          onClick: () => {
            this.$router.push({ path: '/wms/tools/qryprod' })
          },
        },
        {
          text: 'Reubicar',
          onClick: () => {
            this.$router.push({ path: '/wms/tools/relocate' })
          },
        },
      ],
      isActionSheetVisible: false,
    }
  },
  computed: {
    useDrawer() {
      if (this.$vuetify.breakpoint.mobile) {
        return CoreDrawerMobile
      } else {
        return CoreDrawer
      }
    },
  },
  mounted() {
    this.$root.$on('home', this.goHome)
    this.$root.$on('qtools', this.qTools)
    this.$root.$on('fav', this.goFav)
  },
  methods: {
    loadTool(name) {
      this.isActionSheetVisible = false
    },
    goHome() {
      this.$router.push({ path: '/' })
      this.mobileNav = 0
    },
    qTools() {
      this.isActionSheetVisible = true
      this.mobileNav = 1
    },
    goFav() {
      this.$router.push({ path: '/linabi/favoritos/' })
      this.mobileNav = 2
    },
  },
}
</script>

<style lang="sass">
.v-list-item
  padding: 10px 20px
  margin: 0 .3125rem
  margin-bottom: 0px !important
  min-height: 40px !important
  border-radius: 2px
  .v-list-item__title
    font-weight: 400
</style>
