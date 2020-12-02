<template>
  <v-app dark>
    <CoreAppBar />
    <CoreDrawer />
    <v-main>
      <v-container>
        <nuxt />
      </v-container>
    </v-main>
    <v-footer color="asgrey lighten-3" fixed app>
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
// import { sessionMixin } from '~/mixins/sessionMixin.js'

export default {
  name: 'LinaHome',
  components: {
    CoreAppBar: () => import('../components/core/AppBar'),
    CoreDrawer: () => import('../components/core/Drawer'),
  },
  // mixins: [sessionMixin],
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
