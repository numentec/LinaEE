<template>
  <v-app dark>
    <v-navigation-drawer
      v-model="drawer"
      permanent
      :mini-variant.sync="miniVariant"
      :expand-on-hover="miniVar"
      clipped
      fixed
      app
      dark
      class="primary darken-4"
    >
      <v-list shaped>
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          :to="item.to"
          router
          exact
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <template v-slot:append>
        <div class="pa-2">
          <v-btn v-if="miniVariant" icon class="secondary darken-2">
            <v-icon>mdi-logout-variant</v-icon>
          </v-btn>
          <v-btn v-else rounded block class="secondary darken-2">
            Logout
            <v-icon>mdi-logout-variant</v-icon>
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>
    <v-app-bar :clipped-left="true" fixed app color="primary" dense dark>
      <v-btn icon @click.stop="miniVar = !miniVar">
        <v-icon>
          {{ `${miniVariant ? 'mdi-menu' : 'mdi-backburger'}` }}
        </v-icon>
      </v-btn>
      <v-toolbar-title v-text="title" />
      <v-spacer />
      <v-avatar color="accent" size="35">
        <v-icon dark>mdi-account-circle</v-icon>
      </v-avatar>
    </v-app-bar>
    <v-main>
      <v-container>
        <nuxt />
      </v-container>
    </v-main>
    <v-footer fixed app>
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      clipped: false,
      drawer: false,
      fixed: false,
      items: [
        {
          icon: 'mdi-apps',
          title: 'Welcome',
          to: '/',
        },
        {
          icon: 'mdi-chart-bubble',
          title: 'Inspire',
          to: '/inspire',
        },
      ],
      miniVariant: true,
      miniVar: true,
      right: true,
      rightDrawer: false,
      title: 'LinaEE',
    }
  },
}
</script>
