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
    <v-bottom-sheet v-model="isActionSheetVisible">
      <v-sheet class="text-center">
        <v-btn
          v-for="(item, i) in dataSource"
          :key="i"
          text
          color="primary"
          :class="{ 'mt-4': i > 0 }"
          block
          @click="loadTool(i)"
        >
          {{ item.text }}
        </v-btn>
      </v-sheet>
    </v-bottom-sheet>
  </v-app>
</template>

<script>
// import DxActionSheet from 'devextreme-vue/action-sheet'
const CoreDrawer = () => import('../components/core/Drawer')
const CoreDrawerMobile = () => import('../components/core/DrawerMobile')

export default {
  name: 'LinaHome',
  components: {
    CoreAppBar: () => import('../components/core/AppBar'),
  },
  data() {
    return {
      mobileNav: 0,
      bar: true,
      dataSource: [
        {
          text: 'Consultar Producto',
          onClick: () => {
            this.$router.push({ path: '/ventas/tools/qryprod' })
          },
        },
        {
          text: 'Ubicaciones de Producto',
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
        {
          text: 'Conteo por SKU',
          onClick: () => {
            this.$router.push({ path: '/wms/tools/countprods' })
          },
        },
        {
          text: 'Conteo por Marbete',
          onClick: () => {
            this.$router.push({ path: '/wms/tools/countmarbete' })
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
    // this.$root.$on('home', this.goHome)
    // this.$root.$on('qtools', this.qTools)
    // this.$root.$on('fav', this.goFav)
  },
  methods: {
    loadTool(indx) {
      this.dataSource[indx].onClick()
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
