<template>
  <v-app id="portal">
    <v-app-bar color="primary" clipped-left fixed app dark>
      <v-toolbar-title>LinaEE Demo Portal</v-toolbar-title>
      <v-spacer />
      <v-badge
        v-show="getCartItemCount > 0"
        :content="getCartProductCount > 999 ? '999+' : getCartProductCount"
        class="mr-6"
        color="red"
        offset-y="25"
        overlap
      >
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn icon dark v-bind="attrs" v-on="on" @click="goToCart">
              <v-icon dark>mdi-cart-outline</v-icon>
            </v-btn>
          </template>
          <span>Go to cart</span>
        </v-tooltip>
      </v-badge>
      <v-card-actions>
        <v-btn rounded small color="success" @click="$router.push('/login')">
          <v-icon left> mdi-account-key </v-icon>
          Login
        </v-btn>
      </v-card-actions>
      <v-btn icon @click="$router.push('/login')">
        <v-icon>mdi-dots-vertical</v-icon>
      </v-btn>
    </v-app-bar>
    <v-main class="grey lighten-3">
      <v-container>
        <nuxt />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'PortalLayout',
  data: () => ({}),

  computed: {
    ...mapGetters('shoppingcart/cart', [
      'getCartItemCount',
      'getCartProductCount',
    ]),
  },

  methods: {
    goToCart() {
      this.$router.push('/shoppingcart/cart')
    },
  },
}
</script>

<style lang="scss" scoped></style>
