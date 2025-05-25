<template>
  <div>
    <v-row justify="end">
      <v-card-actions>
        <v-btn rounded color="success" @click="$router.push('/login')">
          <v-icon left> mdi-account-key </v-icon>
          Login
        </v-btn>
      </v-card-actions>
    </v-row>
    <v-row justify="center" align="center">
      <v-col cols="12">
        <div class="text-center">
          <LinaLogo logosize="mdtr" />
        </div>
        <v-card>
          <v-card-title class="headline"> Welcome to LinaEE </v-card-title>
          <v-card-text>
            <p>Gracias por elegir Lina Edición Empresarial como su ERP.</p>
            <hr class="my-3" />
            <a
              href="https://linaee.com/"
              target="_blank"
              rel="noopener noreferrer"
            >
              LinaEE Site
            </a>
            <!-- <br />
            <a
              href="https://github.com/nuxt/nuxt.js"
              target="_blank"
              rel="noopener noreferrer"
            >
              LinaEE GitHub
            </a> -->
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn
              color="primary"
              @click.stop="showSnackBar('Documentación en desarrollo')"
            >
              Docs
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <v-snackbar v-model="snackbar" timeout="2000">
      {{ snackmsg }}
      <template v-slot:action="{ attrs }">
        <v-btn color="secondary" text v-bind="attrs" @click="snackbar = false">
          Cerrar
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import LinaLogo from '~/components/core/LinaLogo.vue'

export default {
  name: 'Portal',
  layout: 'portal',
  components: {
    LinaLogo,
  },
  data() {
    return {
      snackbar: false,
      snackmsg: '',
    }
  },
  computed: {},
  methods: {
    showSnackBar(msg) {
      this.snackmsg = msg
      this.snackbar = true
    },
  },
  head() {
    return {
      title: 'Portal',
    }
  },
}
</script>

<style lang="scss" scoped></style>
