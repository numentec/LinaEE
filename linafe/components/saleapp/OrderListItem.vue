<template>
  <v-list-item
    :key="order.id"
    class="mx-0"
    @click.stop="$emit('order-clicked', order.id)"
  >
    <!-- <v-list-item-avatar>
                    <v-img
                        :src="`https://picsum.photos/seed/${order.id}/50/50`"
                        alt="Order image"
                    ></v-img>
                    </v-list-item-avatar> -->
    <v-list-item-content>
      <v-list-item-title :class="{ 'text--disabled': isCancelled }">
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-icon
              x-small
              class="mr-1 status-dot"
              :color="statusInfo.color"
              :aria-label="statusInfo.text"
              role="img"
              v-bind="attrs"
              v-on="on"
            >
              mdi-circle
            </v-icon>
          </template>
          <span>{{ statusInfo.text }}</span>
        </v-tooltip>
        {{ `Order #: ${order.id}` }}
      </v-list-item-title>
      <v-list-item-subtitle>
        {{ order.customer_name }}
      </v-list-item-subtitle>
      <v-list-item-subtitle>
        {{
          `Total: $${order.total.toLocaleString('es-US', {
            style: 'currency',
            currency: 'USD',
          })}`
        }}
      </v-list-item-subtitle>
    </v-list-item-content>
    <v-list-item-action>
      <v-list-item-action-text>
        {{ new Date(order.created_at).toISOString().split('T')[0] }}
      </v-list-item-action-text>
      <v-btn icon @click.stop="resendMail">
        <v-icon>mdi-share-variant-outline</v-icon>
      </v-btn>
    </v-list-item-action>
  </v-list-item>
</template>

<script>
import { getOrderStatus } from '@/utils/orderStatus'

export default {
  name: 'OrderListItem',
  props: {
    order: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      loadingView: false,
    }
  },

  computed: {
    isMobile() {
      return this.$vuetify.breakpoint.mobile
    },
    sz() {
      // screen size
      return this.$vuetify.breakpoint.name
    },
    statusInfo() {
      return getOrderStatus(this.order.status)
    },
    isCancelled() {
      return this.order.status === 'cancelled'
    },
  },

  activated() {
    this.loadingView = false
  },

  methods: {
    resendMail() {
      this.$emit('resend-mail', this.order)
    },
  },
}
</script>

<style scoped>
.status-dot {
  vertical-align: middle;
}
</style>
