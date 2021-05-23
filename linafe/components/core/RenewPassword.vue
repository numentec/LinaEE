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
        <v-toolbar color="accent darken-3" dark>
          <v-toolbar-title>Renovar Contraseña</v-toolbar-title>
          <v-spacer />
          <v-btn icon @click="closeDialog(false)">
            <v-icon>mdi-window-close</v-icon>
          </v-btn>
        </v-toolbar>
        <v-container class="px-4">
          <v-card-text>
            <v-form
              ref="renew_form"
              v-model="valid"
              lazy-validation
              @submit.prevent="renewPass"
            >
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    v-model="pass_renew.old_password"
                    :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                    :rules="[rules.required, rules.min]"
                    :type="show1 ? 'text' : 'password'"
                    name="input-10-1"
                    label="Contraseña actual"
                    hint="Mínimo 8 caracteres"
                    counter
                    prepend-icon="mdi-lock-outline"
                    @click:append="show1 = !show1"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="pass_renew.password1"
                    :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
                    :rules="[rules.required, rules.min]"
                    :type="show2 ? 'text' : 'password'"
                    name="input-10-1"
                    label="Nueva contraseña"
                    hint="Mínimo 8 caracteres"
                    counter
                    prepend-icon="mdi-shield-lock-outline"
                    @click:append="show2 = !show2"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="pass_renew.password2"
                    block
                    :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
                    :rules="[rules.required, passwordMatch]"
                    :type="show2 ? 'text' : 'password'"
                    name="input-10-1"
                    label="Confirmar nueva contraseña"
                    counter
                    prepend-icon="mdi-lock-check-outline"
                    @click:append="show2 = !show2"
                  ></v-text-field>
                </v-col>
                <v-spacer></v-spacer>
                <v-col class="d-flex ml-auto" cols="12" sm="3" xsm="12">
                  <v-btn type="submit" block :disabled="!valid" color="success"
                    >Aceptar</v-btn
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
  name: 'RenewPassword',
  props: {
    dialog: Boolean,
    uid: {
      type: Number,
      default: 0,
      required: true,
    },
  },

  data: () => ({
    valid: true,
    pass_renew: {
      old_password: '',
      password1: '',
      password2: '',
    },
    show1: false,
    show2: false,
    rules: {
      required: (value) => !!value || 'Requerido.',
      min: (v) => (v && v.length >= 8) || 'Min 8 caracteres',
    },
  }),

  computed: {
    passwordMatch() {
      return () =>
        this.pass_renew.password1 === this.pass_renew.password2 ||
        'Contraseñas no coinciden'
    },
  },

  methods: {
    reset() {
      this.$refs.renew_form.reset()
    },
    resetValidation() {
      this.$refs.renew_form.resetValidation()
    },
    closeDialog(refresh) {
      this.$emit('closeDialog', refresh)
    },
    async renewPass() {
      if (this.$refs.renew_form.validate()) {
        const payload = { uid: this.uid, pwd: this.pass_renew }
        try {
          await this.$store.dispatch('sistema/renewPass', payload).then(() => {
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
              message: 'Error renovando contraseña',
            })
          }
        }
      }
    },
  },
}
</script>

<style lang="scss" scoped></style>
