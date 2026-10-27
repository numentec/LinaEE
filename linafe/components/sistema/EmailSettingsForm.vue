<template>
  <div>
    <v-progress-linear v-if="loading" indeterminate color="secondary" />
    <v-form
      ref="form"
      v-model="valid"
      :disabled="loading"
      @submit.prevent="save"
    >
      <v-row>
        <v-col cols="12" md="6">
          <div class="text-subtitle-2 mb-2">Proveedor</div>
          <v-btn-toggle
            v-model="conf.provider"
            mandatory
            color="secondary"
            @change="clearErrors"
          >
            <v-btn v-for="p in providers" :key="p.value" :value="p.value" small>
              <v-icon left small>{{ p.icon }}</v-icon>
              {{ p.text }}
            </v-btn>
          </v-btn-toggle>
        </v-col>
        <v-col cols="12" md="6">
          <v-switch
            v-model="conf.is_active"
            inset
            color="secondary"
            label="Usar esta configuración para el envío de correos"
            :hint="
              conf.is_active
                ? ''
                : 'Desactivada: se usa la configuración del servidor (.env)'
            "
            persistent-hint
          />
        </v-col>
      </v-row>

      <v-alert
        v-if="conf.provider === 'gmail'"
        type="info"
        text
        dense
        class="mt-2"
      >
        Gmail requiere tener activada la verificación en 2 pasos y usar una
        <a
          href="https://myaccount.google.com/apppasswords"
          target="_blank"
          rel="noopener"
          >contraseña de aplicación</a
        >
        (16 caracteres), no la contraseña normal de la cuenta.
      </v-alert>
      <v-alert
        v-if="conf.provider === 'office365'"
        type="info"
        text
        dense
        class="mt-2"
      >
        Microsoft 365 envía mediante Microsoft Graph. En el portal de Entra ID
        (Azure):
        <ol class="mt-1">
          <li>
            Registre una aplicación y copie el <b>Tenant ID</b> y el
            <b>Client ID</b>.
          </li>
          <li>
            En <i>Certificados y secretos</i> cree un <b>Client Secret</b>.
          </li>
          <li>
            En <i>Permisos de API</i> agregue
            <b>Microsoft Graph &rarr; Application &rarr; Mail.Send</b> y otorgue
            el consentimiento de administrador.
          </li>
          <li>
            Recomendado: limite la app al buzón remitente con una
            <i>Application Access Policy</i>.
          </li>
        </ol>
      </v-alert>

      <v-row>
        <v-col cols="12" md="4">
          <v-text-field
            v-model="conf.from_email"
            label="Correo remitente"
            :rules="
              conf.is_active ? [rules.required, rules.email] : [rules.email]
            "
            :error-messages="errors.from_email"
          />
        </v-col>
        <v-col cols="12" md="4">
          <v-text-field
            v-model="conf.from_name"
            label="Nombre del remitente"
            :error-messages="errors.from_name"
          />
        </v-col>
        <v-col cols="12" md="4">
          <v-text-field
            v-model="conf.reply_to"
            label="Responder a (opcional)"
            :rules="[rules.email]"
            :error-messages="errors.reply_to"
          />
        </v-col>
        <v-col cols="12" class="pt-0">
          <v-switch
            v-model="conf.reply_to_user"
            inset
            class="mt-0"
            label="Responder al usuario en sesión"
            hint="Las respuestas se dirigen al correo del usuario que envía. Si no tiene correo, o el envío no lo hace un usuario, se usa Responder a."
            persistent-hint
            :error-messages="errors.reply_to_user"
          />
        </v-col>
      </v-row>

      <v-row v-if="conf.provider === 'smtp'">
        <v-col cols="12" md="5">
          <v-text-field
            v-model="conf.host"
            label="Servidor SMTP"
            placeholder="mail.empresa.com"
            :rules="conf.is_active ? [rules.required] : []"
            :error-messages="errors.host"
          />
        </v-col>
        <v-col cols="12" md="3">
          <v-select
            v-model="conf.security"
            :items="securities"
            label="Seguridad"
            :error-messages="errors.security"
            @change="suggestPort"
          />
        </v-col>
        <v-col cols="6" md="2">
          <v-text-field
            v-model.number="conf.port"
            type="number"
            label="Puerto"
            :error-messages="errors.port"
          />
        </v-col>
        <v-col cols="6" md="2">
          <v-text-field
            v-model.number="conf.timeout"
            type="number"
            label="Timeout (s)"
            :error-messages="errors.timeout"
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field
            v-model="conf.username"
            label="Usuario"
            autocomplete="off"
            hint="Dejar vacío si el servidor no requiere autenticación"
            :error-messages="errors.username"
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field
            v-model="conf.password"
            label="Contraseña"
            type="password"
            autocomplete="new-password"
            :hint="
              conf.has_password
                ? 'Contraseña guardada. Déjela vacía para conservarla'
                : ''
            "
            persistent-hint
            :error-messages="errors.password"
          />
        </v-col>
      </v-row>

      <v-row v-if="conf.provider === 'gmail'">
        <v-col cols="12" md="6">
          <v-text-field
            v-model="conf.password"
            label="Contraseña de aplicación"
            type="password"
            autocomplete="new-password"
            :hint="
              conf.has_password
                ? 'Contraseña guardada. Déjela vacía para conservarla'
                : ''
            "
            persistent-hint
            :rules="
              conf.is_active && !conf.has_password ? [rules.required] : []
            "
            :error-messages="errors.password"
          />
        </v-col>
        <v-col
          cols="12"
          md="6"
          class="d-flex align-center text-caption text--secondary"
        >
          Servidor smtp.gmail.com, puerto 587 (STARTTLS). El usuario es el
          correo remitente.
        </v-col>
      </v-row>

      <v-row v-if="conf.provider === 'office365'">
        <v-col cols="12" md="6">
          <v-text-field
            v-model="conf.ms_tenant_id"
            label="Tenant ID"
            :rules="conf.is_active ? [rules.required] : []"
            :error-messages="errors.ms_tenant_id"
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field
            v-model="conf.ms_client_id"
            label="Client ID"
            :rules="conf.is_active ? [rules.required] : []"
            :error-messages="errors.ms_client_id"
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field
            v-model="conf.ms_client_secret"
            label="Client Secret"
            type="password"
            autocomplete="new-password"
            :hint="
              conf.has_client_secret
                ? 'Secret guardado. Déjelo vacío para conservarlo'
                : ''
            "
            persistent-hint
            :rules="
              conf.is_active && !conf.has_client_secret ? [rules.required] : []
            "
            :error-messages="errors.ms_client_secret"
          />
        </v-col>
        <v-col
          cols="12"
          md="6"
          class="d-flex align-center text-caption text--secondary"
        >
          El correo remitente debe ser un buzón existente del tenant.
        </v-col>
      </v-row>

      <v-row v-if="conf.last_test_at" dense>
        <v-col cols="12">
          <v-icon small :color="conf.last_test_ok ? 'success' : 'error'">
            {{ conf.last_test_ok ? 'mdi-check-circle' : 'mdi-alert-circle' }}
          </v-icon>
          <span class="text-caption">
            Última prueba {{ formatDate(conf.last_test_at) }}:
            {{ conf.last_test_message }}
          </span>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12" class="d-flex">
          <v-spacer />
          <v-btn
            text
            color="secondary"
            :disabled="loading || !conf.is_active"
            @click="openTest"
          >
            <v-icon left>mdi-email-fast-outline</v-icon>
            Enviar prueba
          </v-btn>
          <v-btn
            color="secondary"
            type="submit"
            :loading="saving"
            :disabled="loading"
          >
            <v-icon left>mdi-content-save</v-icon>
            Guardar
          </v-btn>
        </v-col>
      </v-row>
    </v-form>

    <v-dialog v-model="testDialog" max-width="450">
      <v-card>
        <v-card-title>Enviar correo de prueba</v-card-title>
        <v-card-text>
          <p class="text-caption">Se usa la configuración guardada.</p>
          <v-text-field
            v-model="testTo"
            label="Destinatario"
            :rules="[rules.required, rules.email]"
            autofocus
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="testDialog = false">Cancelar</v-btn>
          <v-btn
            color="secondary"
            :loading="testing"
            :disabled="!testTo"
            @click="sendTest"
            >Enviar</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="5000">
      {{ snackbar.text }}
      <template v-slot:action="{ attrs }">
        <v-btn text v-bind="attrs" @click="snackbar.show = false">Cerrar</v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
const URL = 'settings/email/'
const DEFAULT_PORTS = { starttls: 587, ssl: 465, none: 25 }

export default {
  async fetch() {
    try {
      const { data } = await this.$axios.get(URL)
      this.setConf(data)
    } catch (err) {
      this.notify('No se pudo cargar la configuración de correo', 'error')
    } finally {
      this.loading = false
    }
  },

  data() {
    return {
      loading: true,
      saving: false,
      testing: false,
      valid: true,
      conf: {
        provider: 'smtp',
        security: 'starttls',
        port: 587,
        timeout: 20,
        is_active: false,
        reply_to_user: false,
      },
      errors: {},
      testDialog: false,
      testTo: '',
      snackbar: { show: false, text: '', color: '' },
      providers: [
        { value: 'smtp', text: 'SMTP', icon: 'mdi-email-outline' },
        { value: 'gmail', text: 'Gmail', icon: 'mdi-gmail' },
        {
          value: 'office365',
          text: 'Microsoft 365',
          icon: 'mdi-microsoft-outlook',
        },
      ],
      securities: [
        { value: 'starttls', text: 'STARTTLS' },
        { value: 'ssl', text: 'SSL/TLS' },
        { value: 'none', text: 'Ninguna' },
      ],
      rules: {
        required: (v) => !!v || 'Campo requerido',
        email: (v) =>
          !v || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) || 'Correo no válido',
      },
    }
  },

  methods: {
    setConf(data) {
      this.conf = { ...data, password: '', ms_client_secret: '' }
    },

    clearErrors() {
      this.errors = {}
    },

    suggestPort(security) {
      this.conf.port = DEFAULT_PORTS[security]
    },

    async save() {
      if (!this.$refs.form.validate()) return
      this.saving = true
      this.clearErrors()
      try {
        const { data } = await this.$axios.put(URL, this.conf)
        this.setConf(data)
        this.notify('Configuración guardada', 'success')
      } catch (err) {
        this.errors = (err.response && err.response.data) || {}
        this.notify('Revise los datos de la configuración', 'error')
      } finally {
        this.saving = false
      }
    },

    openTest() {
      this.testTo =
        this.testTo || (this.$auth.user && this.$auth.user.email) || ''
      this.testDialog = true
    },

    async sendTest() {
      this.testing = true
      let result
      try {
        const { data } = await this.$axios.post(URL + 'test/', {
          to: this.testTo,
        })
        result = data
      } catch (err) {
        result = (err.response && err.response.data) || {
          ok: false,
          message: 'Error de conexión',
        }
      } finally {
        this.testing = false
      }
      this.testDialog = false
      this.notify(
        result.message || 'Error enviando la prueba',
        result.ok ? 'success' : 'error'
      )
      if (result.last_test_at) {
        this.conf = {
          ...this.conf,
          last_test_at: result.last_test_at,
          last_test_ok: result.ok,
          last_test_message: result.message,
        }
      }
    },

    notify(text, color) {
      this.snackbar = { show: true, text, color }
    },

    formatDate(value) {
      return new Date(value).toLocaleString()
    },
  },
}
</script>
