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
    <component :is="drawerListComponent" />
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

export default {
  name: 'CoreDrawerMobile',
  props: {
    drawerListComponent: {
      type: [Object, Function], // Accepts a component as an object or function
      required: true, // It's required
    },
  },
  data() {
    return {}
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
