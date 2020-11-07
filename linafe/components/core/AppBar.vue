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
        <AppBarItem to="/sistema/usuarios">
          <v-list-item-title>Perfil</v-list-item-title>
        </AppBarItem>
        <AppBarItem>
          <v-list-item-title @click.stop="userLogout">
            Cerrar Sesión
          </v-list-item-title>
        </AppBarItem>
      </v-list>
    </v-menu>
  </v-app-bar>
</template>

<script>
// Components
import { mapState, mapActions } from 'vuex'
import { VHover, VListItem } from 'vuetify/lib'
import { authComputed } from '~/store/core.js'

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
    ...mapState('core', ['drawer', 'is_mini', 'is_expanded']),
    ...authComputed,
  },

  methods: {
    ...mapActions('core', ['SetDrawer', 'setIsMini', 'setIsExpanded']),
    ...mapActions('sistema', ['userLogout']),
    setMiniState(mini) {
      this.setIsMini(mini)
      this.setIsExpanded(!mini)
    },
    testAlert() {
      alert(
        'Llamando api de login por ' + this.username + ' / ' + this.password
      )
    },
  },
}
</script>
