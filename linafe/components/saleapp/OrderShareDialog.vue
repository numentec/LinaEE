<template>
  <v-dialog :value="value" max-width="560" persistent>
    <v-card>
      <v-card-title>Share order # {{ order.id }}</v-card-title>

      <v-tabs v-model="selTab" grow color="secondary">
        <v-tab href="#email" :disabled="busy">
          <v-icon left small>mdi-email-outline</v-icon> Email
        </v-tab>
        <v-tab href="#link" :disabled="busy">
          <v-icon left small>mdi-link-variant</v-icon> Public link
        </v-tab>
      </v-tabs>
      <v-divider />

      <v-tabs-items v-model="selTab">
        <!-- Envío por correo -->
        <v-tab-item value="email">
          <v-card-text class="pt-5">
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
            <v-btn text :disabled="busy" @click="skip">{{ skipText }}</v-btn>
            <v-btn color="secondary" :loading="sending" @click="send">
              <v-icon left>mdi-email-fast-outline</v-icon>
              Send
            </v-btn>
          </v-card-actions>
        </v-tab-item>

        <!-- Enlace público -->
        <v-tab-item value="link">
          <v-card-text class="pt-5">
            <div class="text-body-2 mb-4">
              Anyone with this link can view the order and download it (PDF,
              Excel and images) without logging in. Customer contact data is not
              shown.
            </div>

            <v-alert v-if="isCancelled" type="warning" dense outlined>
              Cancelled orders cannot be shared.
            </v-alert>

            <template v-else-if="hasLink">
              <v-text-field
                :value="publicLink"
                label="Link"
                readonly
                outlined
                dense
                hide-details
                append-icon="mdi-content-copy"
                @click:append="copyLink"
                @focus="$event.target.select()"
              />
              <div class="d-flex align-center mt-2">
                <v-chip x-small label dark :color="isExpired ? 'red' : 'green'">
                  {{ isExpired ? 'Expired' : 'Active' }}
                </v-chip>
                <span class="text-caption ml-2">
                  {{ isExpired ? 'Expired on' : 'Valid until' }}
                  {{ formatDateTime(link.public_token_expires_at) }}
                </span>
              </div>
            </template>

            <div v-else class="text--secondary">
              This order has no public link.
            </div>
          </v-card-text>
          <v-card-actions>
            <v-btn
              v-if="hasLink"
              text
              color="error"
              :loading="linkBusy === 'revoke'"
              :disabled="busy"
              @click="revoke"
            >
              Revoke
            </v-btn>
            <v-spacer />
            <v-btn text :disabled="busy" @click="skip">Close</v-btn>
            <v-btn
              v-if="!isCancelled"
              text
              color="primary"
              :loading="linkBusy === 'issue'"
              :disabled="busy"
              @click="issue"
            >
              {{ hasLink ? 'Renew' : 'Generate link' }}
            </v-btn>
            <v-btn
              v-if="hasLink && !isCancelled"
              color="primary"
              depressed
              :disabled="isExpired"
              @click="copyLink"
            >
              <v-icon left>mdi-content-copy</v-icon> Copy
            </v-btn>
          </v-card-actions>
        </v-tab-item>
      </v-tabs-items>
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

function linkFromOrder(order) {
  return {
    public_token: order?.public_token || null,
    public_token_expires_at: order?.public_token_expires_at || null,
  }
}

// Diálogo para compartir una orden: envío por correo y enlace público.
// Eventos:
//   sent / error  -> resultado del envío de correo (el diálogo se cierra)
//   skipped       -> se cerró sin enviar correo
//   notify        -> (texto, color) mensajes de la pestaña de enlace
export default {
  name: 'OrderShareDialog',
  props: {
    value: { type: Boolean, default: false },
    order: { type: Object, default: () => ({}) },
    // Pestaña inicial al abrir: 'email' | 'link'
    tab: { type: String, default: 'email' },
    attachments: { type: String, default: 'pdf' },
    includeImages: { type: Boolean, default: false },
    sendTo: { type: String, default: '' },
    skipText: { type: String, default: 'Do not send' },
  },

  data() {
    return {
      selTab: this.tab,
      sending: false,
      linkBusy: '',
      now: Date.now(),
      // Copia local del enlace: la orden puede no estar en el store
      // (p. ej. recién creada en el checkout)
      link: linkFromOrder(this.order),
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

  computed: {
    busy() {
      return this.sending || Boolean(this.linkBusy)
    },
    hasLink() {
      return Boolean(this.link.public_token)
    },
    isCancelled() {
      return this.order.status === 'cancelled'
    },
    isExpired() {
      const expires = this.link.public_token_expires_at
      return Boolean(expires) && new Date(expires).getTime() <= this.now
    },
    publicLink() {
      if (!this.hasLink || !process.client) return ''
      return `${window.location.origin}/portal/shared-order/${this.link.public_token}`
    },
  },

  watch: {
    // Al abrir, parte de la configuración de SaleApp y del estado de la orden
    value(open) {
      if (!open) return
      this.selTab = this.tab
      this.selAttachments = this.attachments
      this.selIncludeImages = this.includeImages
      this.selSendTo = this.sendTo
      this.link = linkFromOrder(this.order)
      this.now = Date.now()
      this.$nextTick(() => this.$refs.form?.resetValidation())
    },
  },

  methods: {
    ...mapActions('saleapp/orders', [
      'sendOrderEmail',
      'issuePublicLink',
      'revokePublicLink',
    ]),

    // ---- Correo ----
    async send() {
      if (!this.$refs.form.validate()) return

      this.sending = true
      try {
        await this.sendOrderEmail({
          orderid: this.order.id,
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

    // ---- Enlace público ----
    async issue() {
      const renew = this.hasLink
      const ok = await this.runLink('issue', () =>
        this.issuePublicLink(this.order.id)
      )
      if (!ok) return
      this.$emit(
        'notify',
        renew ? 'Public link renewed' : 'Public link generated',
        'success'
      )
    },

    async revoke() {
      const ok = await this.runLink('revoke', () =>
        this.revokePublicLink(this.order.id)
      )
      if (!ok) return
      this.$emit('notify', 'Public link revoked', 'success')
    },

    // Ejecuta la acción y actualiza la copia local del enlace;
    // devuelve false (y avisa) si falla
    async runLink(kind, fn) {
      this.linkBusy = kind
      try {
        this.link = linkFromOrder(await fn())
        this.now = Date.now()
        return true
      } catch (error) {
        const detail = error?.response?.data?.error || error.message
        this.$emit('notify', `Public link error: ${detail}`, 'error')
        return false
      } finally {
        this.linkBusy = ''
      }
    },

    async copyLink() {
      try {
        await navigator.clipboard.writeText(this.publicLink)
        this.$emit('notify', 'Link copied to clipboard', 'success')
      } catch (error) {
        this.$emit('notify', 'Could not copy the link', 'error')
      }
    },

    formatDateTime(value) {
      if (!value) return '—'
      return new Date(value).toLocaleString([], {
        dateStyle: 'medium',
        timeStyle: 'short',
      })
    },
  },
}
</script>
