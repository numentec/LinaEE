<template>
  <client-only>
    <v-dialog
      :value="dialog"
      persistent
      max-width="600px"
      min-width="360px"
      @input="$emit('update:dialog', false)"
      @keydown.esc="closeDialog(false)"
    >
      <v-card>
        <v-toolbar color="accent lighten-3" dark>
          <v-toolbar-title>Registrar Usuario</v-toolbar-title>
          <v-spacer />
          <v-btn icon @click="closeDialog(false)">
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
                    prepend-icon="mdi-account-plus-outline"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6" md="6">
                  <v-text-field
                    v-model="user_to_reg.password"
                    :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                    :rules="[rules.required, rules.min]"
                    :type="show1 ? 'text' : 'password'"
                    name="input-10-1"
                    label="Contraseña"
                    hint="Mínimo 8 caracteres"
                    counter
                    prepend-icon="mdi-lock-outline"
                    @click:append="show1 = !show1"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6" md="6">
                  <v-text-field
                    v-model="verify"
                    block
                    :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                    :rules="[rules.required, passwordMatch]"
                    :type="show1 ? 'text' : 'password'"
                    name="input-10-1"
                    label="Confirmar Contraseña"
                    counter
                    prepend-icon="mdi-lock-check-outline"
                    @click:append="show1 = !show1"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-select
                    v-model="selected_groups"
                    :items="groups"
                    item-text="name"
                    item-value="id"
                    prepend-icon="mdi-account-multiple-check-outline"
                    multiple
                    return-object
                    label="Grupos"
                    chips
                    deletable-chips
                  >
                  </v-select>
                </v-col>
                <v-col cols="12" sm="6" md="6">
                  <v-text-field
                    v-model="user_to_reg.first_name"
                    :rules="[rules.required]"
                    label="Nombres"
                    maxlength="20"
                    required
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6" md="6">
                  <v-text-field
                    v-model="user_to_reg.last_name"
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
                    prepend-icon="mdi-at"
                  ></v-text-field>
                </v-col>
                <v-spacer></v-spacer>
                <v-col class="d-flex ml-auto" cols="12" sm="3" xsm="12">
                  <v-btn type="submit" block :disabled="!valid" color="success"
                    >Registrar</v-btn
                  >
                </v-col>
              </v-row>
            </v-form>
          </v-card-text>
        </v-container>
      </v-card>
    </v-dialog>
  </client-only>
</template>

<script>
export default {
  name: 'UserRegister',
  props: {
    dialog: Boolean,
    groups: {
      type: Array,
      required: false,
      default() {
        return []
      },
    },
  },

  data: () => ({
    valid: true,
    user_to_reg: {
      username: '',
      password: '',
      first_name: '',
      last_name: '',
      email: '',
    },
    selected_groups: [],
    // user.groups.add(groupA, groupB)
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
    reset() {
      this.$refs.register_form.reset()
    },
    resetValidation() {
      this.$refs.register_form.resetValidation()
    },
    closeDialog(refresh) {
      this.$emit('closeDialog', refresh)
    },
    async registerUser() {
      if (this.$refs.register_form.validate()) {
        try {
          await this.$store
            .dispatch('sistema/registerUser', this.user_to_reg)
            .then(() => {
              this.reset()
              this.closeDialog(true)
            })
        } catch (err) {
          if (err.response) {
            this.$error({
              statusCode: err.response.status,
              message: err.response.data.message,
            })
          } else {
            this.$error({
              statusCode: 503,
              message: 'No se pudo cargar la lista de usuarios. Intente luego',
            })
          }
        }
      }
    },
  },
}
</script>

<style lang="scss" scoped></style>
