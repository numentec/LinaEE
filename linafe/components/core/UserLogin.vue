<template>
  <client-only>
    <div>
      <v-alert
        ref="errAlert"
        v-model="showAlert"
        type="error"
        text
        outlined
        border="left"
        dismissible
        dense
        icon="mdi-account-alert"
        max-width="800"
        class="mx-auto text-center"
      >
        {{ `${error.message} (codigo: ${error.statusCode})` }}
      </v-alert>
      <v-card max-width="400" class="mx-auto mt-16">
        <v-overlay :absolute="true" :value="overlay">
          <v-progress-circular indeterminate size="50" width="5">
          </v-progress-circular>
        </v-overlay>
        <LinaLogo logosize="xstr" class="text-center logo_stack" />
        <v-card-text>
          <v-form
            id="login_form"
            ref="login_form"
            v-model="valid"
            lazy-validation
            class="mt-0"
            @submit.prevent="userLogin"
          >
            <v-container class="px-4 mt-n12">
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
                    v-show="showdb"
                    v-model="database"
                    prepend-icon="mdi-database-lock-outline"
                    label="Base de Datos"
                  ></v-select>
                </v-col>
              </v-row>
            </v-container>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn
            type="submit"
            form="login_form"
            rounded
            large
            block
            :disabled="!valid"
            color="success"
          >
            Aceptar
          </v-btn>
        </v-card-actions>
      </v-card>
    </div>
  </client-only>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'UserLogin',
  components: {
    LinaLogo: () => import('~/components/core/LinaLogo.vue'),
  },

  data: () => ({
    valid: true,
    login: {
      username: '',
      password: '',
    },
    database: '',
    verify: '',
    show1: false,
    showAlert: false,
    showdb: false,
    overlay: false,
    rules: {
      required: (value) => !!value || 'Requerido.',
      min: (v) => (v && v.length >= 8) || 'Min 8 caracteres',
    },
  }),
  computed: {
    ...mapState('sistema', ['error']),
  },
  watch: {
    error(newVal) {
      const errcode = this.error.statusCode
      this.overlay = false
      if (errcode !== 0) {
        this.showAlert = true
        const top = this.$refs.errAlert.offsetTop
        window.scrollTo(0, top)
        // this.$refs.errAlert.scrollTop = 0
      }
    },
  },
  methods: {
    ...mapActions('sistema', ['setError']),
    reset() {
      this.$refs.login_form.reset()
    },

    resetValidation() {
      this.$refs.login_form.resetValidation()
    },

    async userLogin() {
      if (this.$refs.login_form.validate()) {
        this.overlay = true
        await this.$store.dispatch('sistema/userLogin', this.login).then(() => {
          this.overlay = false
          this.$router.push('/')
        })
      }
    },
  },
}
</script>

<style lang="sass" scoped>
.logo_stack
    position: relative
    top: -88px
    transition: .3s ease
    z-index: 1
</style>
