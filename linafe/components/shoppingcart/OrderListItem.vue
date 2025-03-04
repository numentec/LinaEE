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
      <v-list-item-title>
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
      <v-btn icon @click.stop="$emit('resend-mail')">
        <v-icon>mdi-email-outline</v-icon>
      </v-btn>
    </v-list-item-action>
  </v-list-item>
</template>

<script>
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
  },

  activated() {
    this.loadingView = false
  },

  methods: {
    resendMail() {
      this.loadingView = true
      this.$emit('resend-mail', this.order.id)
    },
  },
}
</script>

<style scoped></style>
