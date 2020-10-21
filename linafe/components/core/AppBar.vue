<template>
  <v-app-bar id="app-bar" color="primary" clipped-left fixed app dense dark>
    <v-btn icon @click="setIsMini(!is_mini)">
      <v-icon>
        {{ `${is_mini ? 'mdi-menu' : 'mdi-backburger'}` }}
      </v-icon>
    </v-btn>
    <v-toolbar-title v-text="title" />
    <v-spacer />
    <v-menu offset-y origin="center center" transition="scale-transition">
      <template v-slot:activator="{ on, attrs }">
        <v-avatar color="accent" size="35" v-bind="attrs" v-on="on">
          <v-icon dark>mdi-account-circle</v-icon>
        </v-avatar>
      </template>
      <v-list>
        <v-list-item>
          <v-list-item-title>Perfil</v-list-item-title>
        </v-list-item>
        <v-list-item>
          <v-list-item-title>Cerrar Sesión</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-app-bar>
</template>

<script>
// Components
// import { VHover, VListItem } from 'vuetify/lib'
import { mapState, mapActions } from 'vuex'
export default {
  name: 'CoreAppBar',

  // components: {
  //   AppBarItem: {
  //     render(h) {
  //       return h(VHover, {
  //         scopedSlots: {
  //           default: ({ hover }) => {
  //             return h(
  //               VListItem,
  //               {
  //                 attrs: this.$attrs,
  //                 class: {
  //                   'black--text': !hover,
  //                   'white--text secondary elevation-12': hover,
  //                 },
  //                 props: {
  //                   activeClass: '',
  //                   dark: hover,
  //                   link: true,
  //                   ...this.$attrs,
  //                 },
  //               },
  //               this.$slots.default
  //             )
  //           },
  //         },
  //       })
  //     },
  //   },
  // },

  data() {
    return {
      title: 'LinaEE',
    }
  },

  computed: {
    ...mapState(['drawer', 'mini_variant', 'is_mini']),
  },

  methods: {
    ...mapActions({
      setDrawer: 'SET_DRAWER',
      setMiniVariant: 'setMiniVariant',
      setIsMini: 'setIsMini',
    }),
  },
}
</script>
