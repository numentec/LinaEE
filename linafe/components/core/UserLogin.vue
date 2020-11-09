<template>
  <client-only>
    <v-card max-width="400" class="mx-auto pt-2">
      <v-alert v-if="error" type="error" dense>{{ error }}</v-alert>
      <v-card-title class="grey lighten-3">
        <LinaLogo class="text-center" />
      </v-card-title>
      <v-form
        ref="login_form"
        v-model="valid"
        lazy-validation
        @submit.prevent="userLogin"
      >
        <v-card max-width="400" flat>
          <v-card-text>
            <v-container class="px-4">
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    v-model="login.username"
                    prepend-icon="mdi-account"
                    :rules="[rules.required]"
                    label="Usuario"
                    maxlength="10"
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="login.password"
                    prepend-icon="mdi-lock"
                    :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                    :rules="[rules.required, rules.min]"
                    :type="show1 ? 'text' : 'password'"
                    name="pass"
                    label="Contraseña"
                    hint="Mínimo 8 caracteres"
                    counter
                    @click:append="show1 = !show1"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-select
                    v-model="database"
                    prepend-icon="mdi-database-lock-outline"
                    label="Base de Datos"
                  ></v-select>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-btn
              type="submit"
              rounded
              large
              block
              :disabled="!valid"
              color="success"
              @click="validate"
            >
              Aceptar
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-form>
    </v-card>
  </client-only>
</template>

<script>
export default {
  name: 'UserLogin',
  components: {
    LinaLogo: () => import('~/components/core/LinaLogo.vue'),
  },
  props: {},

  data: () => ({
    valid: true,

    login: {
      username: '',
      password: '',
    },
    database: '',
    verify: '',
    error: null,

    show1: false,
    rules: {
      required: (value) => !!value || 'Requerido.',
      min: (v) => (v && v.length >= 8) || 'Min 8 caracteres',
    },
  }),
  computed: {},
  methods: {
    validate() {
      if (this.$refs.login_form.validate()) {
        // submit form to server/API here...
      }
    },

    reset() {
      this.$refs.login_form.reset()
    },

    resetValidation() {
      this.$refs.login_form.resetValidation()
    },

    userLogin() {
      this.$store
        .dispatch('sistema/userLogin', this.login)
        .then(() => {
          this.$router.push('/')
        })
        .catch((err) => {
          this.error = err.response.data.message
        })
    },
  },
}
</script>

<style lang="scss" scoped></style>
