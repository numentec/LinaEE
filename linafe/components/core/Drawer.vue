<template>
  <div @mouseover="setIsExpanded(true)" @mouseout="setIsExpanded(!is_mini)">
    <v-navigation-drawer
      v-model="drawer_mode"
      permanent
      :mini-variant="is_mini"
      :expand-on-hover="is_mini"
      clipped
      fixed
      app
      dark
      class="primary darken-4"
    >
      <component :is="drawerListComponent" />
      <template v-slot:append>
        <div v-show="logoutButtonVisible" class="pa-2">
          <v-btn
            v-show="!is_expanded"
            icon
            class="secondary darken-2"
            @click="userLogout"
          >
            <v-icon>mdi-logout-variant</v-icon>
          </v-btn>
          <v-btn
            v-show="is_expanded"
            rounded
            block
            class="secondary darken-2"
            @click="userLogout"
          >
            Logout
            <v-icon>mdi-logout-variant</v-icon>
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'CoreDrawer',
  props: {
    drawerListComponent: {
      type: [Object, Function], // Acepta un componente como objeto o función
      required: true, // Es obligatorio
    },
    showLogout: {
      type: Boolean,
      default: true, // Por defecto, mostrar el botón de logout
    },
  },

  data() {
    return {
      drawer_mode: null,
      logoutButtonVisible: this.showLogout,
    }
  },

  computed: {
    ...mapState('core', ['drawer', 'is_mini', 'is_expanded']),
    // perms() {
    //   return this.curuser.perms
    // },
  },

  mounted() {
    this.setIsExpanded(false)
  },

  methods: {
    ...mapActions('core', ['SetDrawer', 'setIsExpanded']),
    ...mapActions('sistema', ['userLogout']),
  },
}
</script>
