<template>
  <v-dialog
    :value="dialog"
    persistent
    max-width="600px"
    min-width="360px"
    @input="$emit('update:dialog', false)"
    @keydown.esc="closeDialog()"
  >
    <v-card>
      <v-toolbar color="accent lighten-3" dark>
        <v-toolbar-title>Registrar Usuario</v-toolbar-title>
        <v-spacer />
        <v-btn icon @click="closeDialog()">
          <v-icon>mdi-window-close</v-icon>
        </v-btn>
      </v-toolbar>
      <v-container class="px-4">
        <v-card-text>
          <v-form
            ref="register_form"
            v-model="valid"
            lazy-validation
            @submit.prevent="registerUser"
          >
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="user_to_reg.username"
                  :rules="[rules.required]"
                  label="Usuario"
                  maxlength="10"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="6">
                <v-text-field
                  v-model="user_to_reg.firstName"
                  :rules="[rules.required]"
                  label="Nombres"
                  maxlength="20"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="6">
                <v-text-field
                  v-model="user_to_reg.lastName"
                  :rules="[rules.required]"
                  label="Apellidos"
                  maxlength="20"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="user_to_reg.email"
                  :rules="emailRules"
                  label="E-mail"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="user_to_reg.password"
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
                <v-text-field
                  v-model="verify"
                  block
                  :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                  :rules="[rules.required, passwordMatch]"
                  :type="show1 ? 'text' : 'password'"
                  name="input-10-1"
                  label="Confirmar Contraseña"
                  counter
                  @click:append="show1 = !show1"
                ></v-text-field>
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
                  >Register</v-btn
                >
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>
      </v-container>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'UserRegister',
  props: {
    dialog: Boolean,
  },

  data: () => ({
    valid: true,

    user_to_reg: {
      username: '',
      firstName: '',
      lastName: '',
      email: '',
      password: '',
    },
    verify: '',
    emailRules: [
      (v) => !!v || 'Required',
      (v) => /.+@.+\..+/.test(v) || 'E-mail must be valid',
    ],

    show1: false,
    rules: {
      required: (value) => !!value || 'Requerido.',
      min: (v) => (v && v.length >= 8) || 'Min 8 caracteres',
    },
  }),
  computed: {
    passwordMatch() {
      return () =>
        this.user_to_reg.password === this.verify || 'Contraseñas no coinciden'
    },
  },
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
    closeDialog() {
      this.$emit('closeDialog')
    },
    registerUser() {
      this.$store.dispatch('registerUser', {
        user_to_reg: this.user_to_reg,
      })
    },
  },
}
</script>

<style lang="scss" scoped></style>
