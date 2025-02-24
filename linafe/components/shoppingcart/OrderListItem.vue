<template>
  <v-list-item :key="order.id" class="mx-0">
    <!-- <v-list-item-avatar>
                    <v-img
                        :src="`https://picsum.photos/seed/${order.id}/50/50`"
                        alt="Order image"
                    ></v-img>
                    </v-list-item-avatar> -->
    <v-list-item-content>
      <v-list-item-title>
        <vbtn text @click="$emit('order-clicked', order.id)">
          {{ `Order #: ${order.id}` }}
        </vbtn>
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
      <v-btn icon @click="$emit('resend-mail')">
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
    goToView() {
      this.loadingView = true
      this.$emit('card-clicked', {
        key: this.category.type,
        value: this.category.id,
      })
      if (
        this.category.link === null ||
        this.category.link === '' ||
        this.category.link === undefined
      ) {
        this.$router.push('/shoppingcart/categories/departments')
      } else {
        this.$router.push(this.category.link)
      }
    },
    onImgError() {
      this.imgSrc = '/no_image.png'
      this.$emit('no-image')
    },
  },
}
</script>

<style scoped></style>
