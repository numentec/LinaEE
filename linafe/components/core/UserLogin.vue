<template>
  <v-card>
    <v-toolbar color="primary lighten-1" dark>
      <v-toolbar-title>Iniciar Sesión</v-toolbar-title>
    </v-toolbar>
    <v-container class="px-4">
      <v-alert v-if="error" type="error" dense>{{ error }}</v-alert>
      <v-card-text>
        <v-form
          ref="register_form"
          v-model="valid"
          lazy-validation
          @submit.prevent="login"
        >
          <v-row>
            <v-col cols="12">
              <v-text-field
                v-model="username"
                prepend-icon="mdi-account"
                :rules="[rules.required]"
                label="Usuario"
                maxlength="10"
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-model="password"
                prepend-icon="mdi-lock"
                :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                :rules="[rules.required, rules.min]"
                :type="show1 ? 'text' : 'password'"
                name="input-10-1"
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
            <v-spacer></v-spacer>
            <v-col class="d-flex ml-auto" cols="12" sm="3" xsm="12">
              <v-btn
                type="submit"
                x-large
                block
                :disabled="!valid"
                color="success"
                @click="validate"
                >Aceptar</v-btn
              >
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-container>
  </v-card>
</template>

<script>
export default {
  name: 'UserLogin',
  props: {},

  data: () => ({
    valid: true,

    username: '',
    password: '',
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
      if (this.$refs.loginForm.validate()) {
        // submit form to server/API here...
      }
    },
    reset() {
      this.$refs.form.reset()
    },
    resetValidation() {
      this.$refs.register_form.resetValidation()
    },
    async login() {
      try {
        await this.$auth.loginWith('local', {
          data: {
            username: this.username,
            password: this.password,
          },
        })

        this.$router.push('/lina')
      } catch (e) {
        this.error = e.response.data.message
      }
    },
  },
}
</script>

<style lang="scss" scoped></style>
