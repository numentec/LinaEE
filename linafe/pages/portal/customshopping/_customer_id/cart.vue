<template>
  <div>
    <v-container>
      <v-row>
        <v-col cols="12" md="12">
          <h1 class="text-center">{{ customerId }} Shopping Cart</h1>
          <p class="text-center">Manage your custom shopping cart here.</p>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="8">
          <v-card>
            <v-overlay :absolute="true" :value="loading">
              <v-progress-circular indeterminate size="50" width="5">
              </v-progress-circular>
            </v-overlay>
            <v-toolbar dense flat rounded>
              <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    class="mt-0 mb-2 mx-2"
                    icon
                    small
                    v-bind="attrs"
                    v-on="on"
                    @click="$router.back()"
                  >
                    <v-icon>mdi-chevron-left</v-icon>
                  </v-btn>
                </template>
                <span>Back to previous view</span>
              </v-tooltip>
              <v-card-title>Shopping Cart</v-card-title>
              <v-spacer></v-spacer>

              <v-btn
                v-show="getCartItems.length > 0"
                icon
                small
                @click.stop="clearCart"
              >
                <v-icon>mdi-cart-remove</v-icon>
              </v-btn>
              <v-btn
                v-show="isMobile"
                icon
                small
                @click.stop="showSummary = !showSummary"
              >
                <v-icon>
                  {{ showSummary ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
                </v-icon>
              </v-btn>
            </v-toolbar>
            <v-divider></v-divider>
            <v-expand-transition>
              <CartOrderSummary
                v-show="showSummary"
                :customers-list="sellersList"
                :loading="loading"
                :outlined="true"
                :is-customer-cart="true"
                @go-to-checkout="goToCheckout"
              />
            </v-expand-transition>
            <v-card-text>
              <v-row v-for="(item, index) in getCartItems" :key="item.id">
                <v-col cols="12">
                  <v-row dense>
                    <CartCard :show-price="false" :item="{ ...item, index }" />
                  </v-row>
                  <v-row dense><v-divider class="mb-0"></v-divider></v-row>
                </v-col>
              </v-row>
              <v-alert
                v-if="getCartItems.length === 0"
                border="bottom"
                colored-border
                type="warning"
              >
                Your shopping cart <strong>is empty</strong>.
              </v-alert>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" md="4">
          <CartOrderSummary
            :customers-list="sellersList"
            :loading="loading"
            :is-customer-cart="true"
            @go-to-checkout="goToCheckout"
          />
        </v-col>
      </v-row>
      <v-snackbar
        v-model="snackbar"
        :timeout="snackbarTimeout"
        :color="snackbarColor"
        dark
        right
        top
        rounded="pill"
        transition="slide-x-reverse-transition"
      >
        {{ snackbarText }}
        <template v-slot:action="{ attrs }">
          <v-btn dark text v-bind="attrs" @click.stop="snackbar = false">
            Close
          </v-btn>
        </template>
      </v-snackbar>
    </v-container>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import CartCard from '@/components/shoppingcart/CartCard.vue'
import CartOrderSummary from '@/components/shoppingcart/CartOrderSummary.vue'

const sellersList = [
  { id: '1', name: 'Seller 1', email: 'seller1@numen.pa' },
  { id: '2', name: 'Seller 2', email: 'seller2@numen.pa' },
  { id: '3', name: 'Seller 3', email: 'seller3@numen.pa' },
]

export default {
  name: 'CartPage',
  layout: 'publicapps',

  components: {
    CartCard,
    CartOrderSummary,
  },

  data() {
    return {
      selectedCustomer: {},
      editEmail: '',
      editTel: '',
      snackbar: false,
      snackbarText: 'No implementado',
      snackbarColor: 'info',
      snackbarTimeout: 3000,
      loading: false,
      dialog: false,
      showSummary: false,
      sellersList,
    }
  },

  computed: {
    ...mapGetters({
      customerId: 'customshopping/customcatalog/getCustomerId',
      catalogToken: 'customshopping/customcatalog/getCustomCatalogToken',
    }),

    ...mapGetters('shoppingcart/cart', [
      'getCartItems',
      'getCartTotalPrice',
      'getCartCustomer',
    ]),

    ...mapGetters('sistema', ['getCurCia']),

    isMobile() {
      return this.$vuetify.breakpoint.smAndDown
    },
    isXSmall() {
      return this.$vuetify.breakpoint.xsOnly
    },
  },

  methods: {
    ...mapActions('shoppingcart/orders', ['createOrder']),
    ...mapActions('shoppingcart/cart', ['clearCart']),
    async goToCheckout() {
      this.snackbar = true
      if (this.getCartItems.length === 0) {
        this.snackbarColor = 'warning'
        this.snackbarText = 'Your shopping cart is empty'
        return
      }

      if (!this.getCartCustomer.id) {
        this.snackbarColor = 'warning'
        this.snackbarText = 'Please select a customer'
        return
      }

      this.snackbarColor = 'info'
      this.snackbarText = 'Creating order...'

      this.loading = true

      try {
        await this.createOrder()
        this.snackbarColor = 'success'
        this.snackbarText = 'Order created successfully'
        this.snackbarTimeout = 5000

        setTimeout(() => {
          this.loading = false
          this.$router.push('/shoppingcart/ordersview')
        }, 2000)
      } catch (error) {
        this.loading = false
        this.snackbarColor = 'error'
        this.snackbarText =
          'Failed to create order: ' +
          (error.response?.data?.message || error.message)
        this.snackbarTimeout = 5000
      }
    },
  },
  head() {
    return {
      title: 'Cart - Linafe Custom Shopping',
      meta: [
        {
          hid: 'description',
          name: 'description',
          content: 'View and manage your custom shopping cart.',
        },
      ],
    }
  },
}
</script>

<style lang="scss" scoped></style>
