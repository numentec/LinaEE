<template>
  <div>
    <v-progress-linear v-if="loading" indeterminate color="secondary" />
    <v-alert v-if="!canEdit" type="info" text dense>
      Read only. Changing these settings requires access to the configuration
      module.
    </v-alert>
    <v-form :disabled="loading || !canEdit" @submit.prevent="save">
      <v-row>
        <v-col cols="12">
          <div class="text-subtitle-2 mb-2">
            Send the order by email to the customer
          </div>
          <v-btn-toggle v-model="conf.email_policy" mandatory color="secondary">
            <v-btn
              v-for="p in policies"
              :key="p.value"
              :value="p.value"
              :disabled="loading || !canEdit"
              small
            >
              <v-icon left small>{{ p.icon }}</v-icon>
              {{ p.text }}
            </v-btn>
          </v-btn-toggle>
          <div class="text-caption text--secondary mt-1">
            {{ policyHint }}
          </div>
          <div v-if="errors.email_policy" class="error--text text-caption">
            {{ errors.email_policy[0] }}
          </div>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12" md="6">
          <div class="text-subtitle-2 mb-2">Attachments</div>
          <v-btn-toggle
            v-model="conf.email_attachments"
            mandatory
            color="secondary"
          >
            <v-btn
              v-for="a in attachmentOptions"
              :key="a.value"
              :value="a.value"
              :disabled="loading || !canEdit || isNever"
              small
            >
              <v-icon left small>{{ a.icon }}</v-icon>
              {{ a.text }}
            </v-btn>
          </v-btn-toggle>
          <div v-if="errors.email_attachments" class="error--text text-caption">
            {{ errors.email_attachments[0] }}
          </div>
        </v-col>
        <v-col cols="12" md="6">
          <v-switch
            v-model="conf.email_include_images"
            inset
            color="secondary"
            label="Include product images"
            :disabled="isNever"
            :error-messages="errors.email_include_images"
          />
        </v-col>
      </v-row>

      <v-row v-if="conf.modified_at" dense>
        <v-col cols="12" class="text-caption text--secondary">
          {{ conf.company_name }} · Last modified
          {{ formatDate(conf.modified_at) }}
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12" class="d-flex">
          <v-spacer />
          <v-btn
            color="secondary"
            type="submit"
            :loading="saving"
            :disabled="loading || !canEdit"
          >
            <v-icon left>mdi-content-save</v-icon>
            Save
          </v-btn>
        </v-col>
      </v-row>
    </v-form>

    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="5000">
      {{ snackbar.text }}
      <template v-slot:action="{ attrs }">
        <v-btn text v-bind="attrs" @click="snackbar.show = false">Close</v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { EMAIL_ATTACHMENT_OPTIONS } from '@/utils/orderEmail'

const URL = 'saleapp/settings/'

export default {
  async fetch() {
    try {
      const { data } = await this.$axios.get(URL, { params: this.ciaParams })
      this.conf = data
    } catch (err) {
      this.notify('Could not load SaleApp settings', 'error')
    } finally {
      this.loading = false
    }
  },

  data() {
    return {
      loading: true,
      saving: false,
      conf: {
        email_policy: 'ask',
        email_attachments: 'pdf',
        email_include_images: false,
      },
      errors: {},
      snackbar: { show: false, text: '', color: '' },
      policies: [
        {
          value: 'auto',
          text: 'Automatic',
          icon: 'mdi-email-fast-outline',
          hint: 'The order is emailed as soon as it is created or updated.',
        },
        {
          value: 'ask',
          text: 'Ask',
          icon: 'mdi-email-alert-outline',
          hint: 'After checkout you are asked whether to email the order.',
        },
        {
          value: 'never',
          text: 'Do not send',
          icon: 'mdi-email-off-outline',
          hint: 'Orders are never emailed automatically.',
        },
      ],
      attachmentOptions: EMAIL_ATTACHMENT_OPTIONS,
    }
  },

  computed: {
    ...mapGetters('sistema', ['getCurCia', 'getCurUser']),
    ciaParams() {
      return this.getCurCia?.id ? { cia: this.getCurCia.id } : {}
    },
    canEdit() {
      return !!this.getCurUser?.perms?.['core.acc_config']
    },
    isNever() {
      return this.conf.email_policy === 'never'
    },
    policyHint() {
      const policy = this.policies.find(
        (p) => p.value === this.conf.email_policy
      )
      return policy ? policy.hint : ''
    },
  },

  watch: {
    // Otra compañía seleccionada: carga su configuración
    'getCurCia.id'() {
      this.loading = true
      this.$fetch()
    },
  },

  methods: {
    async save() {
      this.saving = true
      this.errors = {}
      try {
        const { data } = await this.$axios.put(
          URL,
          {
            email_policy: this.conf.email_policy,
            email_attachments: this.conf.email_attachments,
            email_include_images: this.conf.email_include_images,
          },
          { params: this.ciaParams }
        )
        this.conf = data
        this.notify('Settings saved', 'success')
      } catch (err) {
        if (err.response?.status === 403) {
          this.notify('You are not allowed to change these settings', 'error')
        } else {
          this.errors = err.response?.data || {}
          this.notify('Please review the settings', 'error')
        }
      } finally {
        this.saving = false
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
