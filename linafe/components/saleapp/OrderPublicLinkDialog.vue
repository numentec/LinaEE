<template>
  <v-dialog :value="value" max-width="560" @input="$emit('input', $event)">
    <v-card>
      <v-card-title>Public link · Order # {{ order.id }}</v-card-title>

      <v-card-text>
        <div class="text-body-2 mb-4">
          Anyone with this link can view the order and download it (PDF, Excel
          and images) without logging in. Customer contact data is not shown.
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
              {{ formatDateTime(order.public_token_expires_at) }}
            </span>
          </div>
        </template>

        <div v-else class="text--secondary">This order has no public link.</div>
      </v-card-text>

      <v-card-actions>
        <v-btn
          v-if="hasLink"
          text
          color="error"
          :loading="busy === 'revoke'"
          :disabled="!!busy"
          @click="revoke"
        >
          Revoke
        </v-btn>
        <v-spacer />
        <v-btn text @click="$emit('input', false)">Close</v-btn>
        <v-btn
          v-if="!isCancelled"
          text
          color="primary"
          :loading="busy === 'issue'"
          :disabled="!!busy"
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
    </v-card>
  </v-dialog>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'OrderPublicLinkDialog',
  props: {
    value: { type: Boolean, default: false },
    order: { type: Object, default: () => ({}) },
  },

  data() {
    return {
      busy: '',
      now: Date.now(),
    }
  },

  computed: {
    hasLink() {
      return Boolean(this.order.public_token)
    },
    isCancelled() {
      return this.order.status === 'cancelled'
    },
    isExpired() {
      const expires = this.order.public_token_expires_at
      return Boolean(expires) && new Date(expires).getTime() <= this.now
    },
    publicLink() {
      if (!this.hasLink || !process.client) return ''
      return `${window.location.origin}/portal/shared-order/${this.order.public_token}`
    },
  },

  watch: {
    value(open) {
      if (open) this.now = Date.now()
    },
  },

  methods: {
    ...mapActions('saleapp/orders', ['issuePublicLink', 'revokePublicLink']),

    async issue() {
      const renew = this.hasLink
      const ok = await this.run('issue', () =>
        this.issuePublicLink(this.order.id)
      )
      if (!ok) return
      this.now = Date.now()
      this.$emit(
        'notify',
        renew ? 'Public link renewed' : 'Public link generated',
        'success'
      )
    },

    async revoke() {
      const ok = await this.run('revoke', () =>
        this.revokePublicLink(this.order.id)
      )
      if (!ok) return
      this.$emit('notify', 'Public link revoked', 'success')
    },

    // Ejecuta la acción; devuelve false (y avisa) si falla
    async run(kind, fn) {
      this.busy = kind
      try {
        await fn()
        return true
      } catch (error) {
        const detail = error?.response?.data?.error || error.message
        this.$emit('notify', `Public link error: ${detail}`, 'error')
        return false
      } finally {
        this.busy = ''
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
