<template>
  <v-app id="webbase">
    <v-app-bar app color="primary darken-1" flat dark>
      <v-container class="py-0 fill-height">
        <v-avatar
          :color="
            $vuetify.breakpoint.smAndDown ? 'accent lighten-2' : 'transparent'
          "
          size="32"
        >
          <v-icon v-show="$vuetify.breakpoint.smAndDown" dark
            >mdi-account-circle</v-icon
          >
        </v-avatar>

        <v-btn v-for="link in links" :key="link.title" text :to="link.path">
          {{ link.title }}
        </v-btn>
        <v-btn text to="/lina" target="_blank">LinaEE</v-btn>
        <v-spacer></v-spacer>
      </v-container>
      <v-avatar
        class="hidden-sm-and-down"
        color="pink accent-3 shrink"
        size="32"
      >
        <v-icon dark>mdi-account-circle</v-icon>
      </v-avatar>
    </v-app-bar>

    <v-main class="grey lighten-3">
      <v-container>
        <nuxt />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  data: () => ({
    links: [
      { title: 'Inicio', path: '/' },
      { title: 'Tienda', path: '/webstore' },
      { title: 'Directorio', path: '/directory' },
    ],
  }),
}
</script>

<style lang="scss" scoped></style>
