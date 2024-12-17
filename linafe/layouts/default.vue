<template>
  <v-app dark>
    <CoreAppBar />
    <component :is="useDrawer" />
    <v-main>
      <v-container>
        <nuxt keep-alive :keep-alive-props="{ exclude: ['modal'] }" />
      </v-container>
    </v-main>
    <v-bottom-navigation
      v-show="getShowBottomNav"
      :value="mobileNav"
      color="primary"
      grow
      fixed
      app
    >
      <v-btn @click="goHome">
        <span>Inicio</span>

        <v-icon>mdi-home</v-icon>
      </v-btn>

      <v-btn v-if="allowedTools.length > 0" @click="qTools">
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
        <template v-for="(item, i) in dataSource">
          <v-btn
            v-if="allowedTools.includes(i)"
            :key="i"
            text
            color="primary"
            :class="{ 'mt-4': i > allowedTools[0] }"
            block
            @click="loadTool(i)"
          >
            {{ item.text }}
          </v-btn>
        </template>
      </v-sheet>
    </v-bottom-sheet>
  </v-app>
</template>

<script>
import { mapState, mapGetters } from 'vuex'

const CoreDrawer = () => import('../components/core/Drawer')
const CoreDrawerMobile = () => import('../components/core/DrawerMobile')

export default {
  name: 'LinaHome',
  components: {
    CoreAppBar: () => import('../components/core/AppBar'),
  },
  middleware: 'setcias',
  data() {
    return {
      mobileNav: 0,
      bar: true,
      allowedTools: [0, 1, 2, 3, 4],
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
    ...mapState('sistema', ['curuser']),
    ...mapGetters('sistema', ['getShowBottomNav']),
    ...mapGetters(['loggedInUser']),
    useDrawer() {
      if (this.$vuetify.breakpoint.mobile) {
        return CoreDrawerMobile
      } else {
        return CoreDrawer
      }
    },
  },
  mounted() {
    window.addEventListener('beforeunload', this.test)

    if (!this.curuser.is_superuser) {
      let aT1 = []
      let aT2 = []
      let aT3 = []

      if (
        this.curuser.ugroups.includes('ventas') ||
        this.curuser.ugroups.includes('ventasadmin')
      ) {
        aT1 = [0, 1]
      }
      if (this.curuser.ugroups.includes('bodega')) {
        aT2 = [1, 2, 3, 4]
      }
      if (this.curuser.ugroups.includes('gerencia')) {
        aT3 = [0, 1, 2, 3, 4]
      }

      this.allowedTools = [...aT1, ...aT2, ...aT3]
    }
    // this.$root.$on('home', this.goHome)
    // this.$root.$on('qtools', this.qTools)
    // this.$root.$on('fav', this.goFav)
  },
  beforeDestroy() {
    window.removeEventListener('beforeunload', this.test)
  },
  methods: {
    loadTool(indx) {
      this.dataSource[indx].onClick()
      this.isActionSheetVisible = false
    },
    goHome() {
      this.$router.push({ path: this.loggedInUser.homelink })
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
    async test() {
      await this.$axios.post('logout/', { force: '1' })
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
