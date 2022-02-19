/* eslint-disable no-console */
<template>
  <v-navigation-drawer
    v-model="localDrawer"
    temporary
    clipped
    fixed
    dark
    class="primary darken-4"
  >
    <v-list shaped>
      <v-list-item nuxt to="/">
        <v-list-item-icon>
          <v-icon>mdi-home</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title class="title">Inico</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-group
        v-for="item in modulos_disponibles"
        v-show="perms[item.perm]"
        :key="item.title"
        :prepend-icon="item.icon"
        no-action
      >
        <template v-slot:activator>
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </template>
        <v-list-item
          v-for="subitem in item.items"
          v-show="perms[subitem.perm]"
          :key="subitem.title"
          nuxt
          :to="subitem.to"
          router
          exact
        >
          <v-list-item-content>
            <v-list-item-title v-text="subitem.title" />
          </v-list-item-content>
        </v-list-item>
      </v-list-group>
    </v-list>
    <template v-slot:append>
      <div class="pa-2">
        <v-btn rounded block class="secondary darken-2" @click="userLogout">
          Logout
          <v-icon>mdi-logout-variant</v-icon>
        </v-btn>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script>
import { mapActions } from 'vuex'
import { modulos } from '~/assets/utilities'

export default {
  name: 'CoreDrawerMobile',
  async fetch() {
    await this.$axios.get('modul-actives/').then((response) => {
      const modulosActivos = response.data
      this.modulactiv = modulosActivos
      this.modulos_disponibles = this.modulos.filter((el) => {
        return modulosActivos.find((element) => {
          return element.nombre === el.name
        })
      })
    })
  },
  data() {
    return {
      modulos_disponibles: [],
      modulactiv: [],
      perms: this.$auth.user.perms,
      modulos,
    }
  },

  computed: {
    localDrawer: {
      get() {
        return !this.$store.state.core.is_mini
      },
      set(v) {
        this.$store.dispatch('core/setIsMini', !v)
        this.$store.dispatch('core/setIsExpanded', false)
      },
    },
  },

  mounted() {},

  methods: {
    ...mapActions('sistema', ['userLogout']),
  },
}
</script>
