<template>
  <v-dialog :value="value" max-width="450" persistent>
    <v-card>
      <v-card-title>Email order # {{ orderId }}</v-card-title>
      <v-card-text>
        <v-form ref="form" @submit.prevent="send">
          <v-text-field
            v-model="selSendTo"
            label="Send to"
            prepend-inner-icon="mdi-email-outline"
            hint="Separate multiple addresses with commas"
            :rules="[rules.required, rules.emails]"
            :disabled="sending"
            outlined
            dense
          />
        </v-form>
        <div class="text-subtitle-2 mb-2">Attachments</div>
        <v-btn-toggle v-model="selAttachments" mandatory color="secondary">
          <v-btn
            v-for="a in attachmentOptions"
            :key="a.value"
            :value="a.value"
            small
          >
            <v-icon left small>{{ a.icon }}</v-icon>
            {{ a.text }}
          </v-btn>
        </v-btn-toggle>
        <v-switch
          v-model="selIncludeImages"
          inset
          color="secondary"
          label="Include product images"
          hide-details
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text :disabled="sending" @click="skip">{{ skipText }}</v-btn>
        <v-btn color="secondary" :loading="sending" @click="send">
          <v-icon left>mdi-email-fast-outline</v-icon>
          Send
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapActions } from 'vuex'
import { EMAIL_ATTACHMENT_OPTIONS } from '@/utils/orderEmail'

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

// Destinatarios separados por coma o punto y coma
function splitEmails(value) {
  return (value || '')
    .split(/[,;]/)
    .map((e) => e.trim())
    .filter(Boolean)
}

export default {
  name: 'SendOrderEmailDialog',
  props: {
    value: { type: Boolean, default: false },
    orderId: { type: [Number, String], default: null },
    attachments: { type: String, default: 'pdf' },
    includeImages: { type: Boolean, default: false },
    sendTo: { type: String, default: '' },
    skipText: { type: String, default: 'Do not send' },
  },

  data() {
    return {
      sending: false,
      selAttachments: this.attachments,
      selIncludeImages: this.includeImages,
      selSendTo: this.sendTo,
      attachmentOptions: EMAIL_ATTACHMENT_OPTIONS,
      rules: {
        required: (v) => splitEmails(v).length > 0 || 'Enter an email address',
        emails: (v) =>
          splitEmails(v).every((e) => EMAIL_RE.test(e)) ||
          'Invalid email address',
      },
    }
  },

  watch: {
    // Al abrir, parte de la configuración de SaleApp
    value(open) {
      if (open) {
        this.selAttachments = this.attachments
        this.selIncludeImages = this.includeImages
        this.selSendTo = this.sendTo
        this.$nextTick(() => this.$refs.form?.resetValidation())
      }
    },
  },

  methods: {
    ...mapActions('saleapp/orders', ['sendOrderEmail']),

    async send() {
      if (!this.$refs.form.validate()) return

      this.sending = true
      try {
        await this.sendOrderEmail({
          orderid: this.orderId,
          attachments: this.selAttachments,
          includeImages: this.selIncludeImages,
          sendto: splitEmails(this.selSendTo).join(', '),
        })
        this.close('sent')
      } catch (error) {
        this.close('error', error)
      } finally {
        this.sending = false
      }
    },

    skip() {
      this.close('skipped')
    },

    close(event, payload) {
      this.$emit('input', false)
      this.$emit(event, payload)
    },
  },
}
</script>
