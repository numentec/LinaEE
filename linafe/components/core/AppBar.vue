<template>
  <v-app-bar id="app-bar" color="primary" clipped-left fixed app dense dark>
    <v-btn icon @click="setMiniState(!is_mini)">
      <v-icon>
        {{ `${is_expanded ? 'mdi-backburger' : 'mdi-menu'}` }}
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
        <AppBarItem>
          <v-list-item-title>Perfil</v-list-item-title>
        </AppBarItem>
        <AppBarItem>
          <v-list-item-title>Cerrar Sesión</v-list-item-title>
        </AppBarItem>
      </v-list>
    </v-menu>
  </v-app-bar>
</template>

<script>
// Components
import { VHover, VListItem } from 'vuetify/lib'
import { mapState, mapActions } from 'vuex'
export default {
  name: 'CoreAppBar',

  components: {
    AppBarItem: {
      render(h) {
        return h(VHover, {
          scopedSlots: {
            default: ({ hover }) => {
              return h(
                VListItem,
                {
                  attrs: this.$attrs,
                  class: {
                    'black--text': !hover,
                    'white--text secondary elevation-12': hover,
                  },
                  props: {
                    activeClass: '',
                    dark: hover,
                    link: true,
                    ...this.$attrs,
                  },
                },
                this.$slots.default
              )
            },
          },
        })
      },
    },
  },

  data() {
    return {
      title: 'LinaEE',
    }
  },

  computed: {
    ...mapState('core', {
      drawer: (state) => state.drawer,
      is_mini: (state) => state.is_mini,
      is_expanded: (state) => state.is_expanded,
    }),
  },

  methods: {
    ...mapActions('core', ['SetDrawer', 'setIsMini', 'setIsExpanded']),
    setMiniState(mini) {
      this.setIsMini(mini)
      this.setIsExpanded(!mini)
    },
  },
}
</script>
