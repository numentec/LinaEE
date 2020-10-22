<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="8" md="6">
      <div class="text-center">
        <LinaLogo />
      </div>
      <v-card>
        <v-card-title class="headline">
          Welcome to Lina Enterprise Edition
        </v-card-title>
        <v-card-text>
          <p>
            Gracias por elegir Lina Edición Empresarial como su ERP. Lina es más
            que un ERP. Explore todas sus funcionalidades.
          </p>
          <hr class="my-3" />
          <a
            href="https://linaee.com/"
            target="_blank"
            rel="noopener noreferrer"
          >
            LinaEE Site
          </a>
          <br />
          <a
            href="https://github.com/nuxt/nuxt.js"
            target="_blank"
            rel="noopener noreferrer"
          >
            LinaEE GitHub
          </a>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="primary" nuxt to="/inspire"> Continue </v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import LinaLogo from '~/components/core/LinaLogo.vue'

export default {
  components: {
    LinaLogo,
  },
}
</script>
