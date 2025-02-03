<template>
  <v-container>
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
          </v-toolbar>
          <v-divider></v-divider>
          <v-card-text>
            <v-row v-for="(item, index) in getCartItems" :key="item.id">
              <v-col cols="12">
                <v-row dense><CartCard :item="{ ...item, index }" /></v-row>
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
        <v-card>
          <v-toolbar dense flat rounded>
            <v-card-title>Order Summary</v-card-title>
          </v-toolbar>
          <v-divider></v-divider>
          <v-card-text>
            <v-row>
              <v-col cols="12">
                <v-row dense justify="start" align="start" class="ml-4 mb-4">
                  <v-col align="start">
                    <div class="my-0">
                      <v-autocomplete
                        v-model="selected_customer"
                        label="Customer"
                        return-object
                        :items="getCustomers"
                        item-text="name"
                        item-value="id"
                        dense
                        background-color="#eafaff"
                        rounded
                        clearable
                        single-line
                      ></v-autocomplete>
                    </div>
                    <div class="mt-0">
                      {{ getCartCustomer.email }}
                    </div>
                  </v-col>
                </v-row>
                <v-row justify="center" align="center">
                  <h3>Total</h3>
                </v-row>
                <v-row justify="center" align="center">
                  <h3>
                    {{
                      `${getCartTotalPrice.toLocaleString('es-US', {
                        style: 'currency',
                        currency: 'USD',
                      })}`
                    }}
                  </h3>
                </v-row>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12">
                <v-row justify="center" align="center">
                  <v-btn
                    color="green darken-1"
                    text
                    :loading="loading"
                    :disabled="loading"
                    @click="goToCheckout"
                  >
                    Checkout
                    <template v-slot:loader>
                      <span class="custom-loader">
                        <v-icon light>mdi-cached</v-icon>
                      </span>
                    </template>
                  </v-btn>
                </v-row>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-snackbar
      v-model="snackbar"
      :timeout="snackTimeout"
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
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import CartCard from '@/components/shoppingcart/CartCard.vue'

export default {
  name: 'ShoppingCart',
  components: {
    CartCard,
  },
  async fetch() {
    const curparams = {
      p01: 'CLI',
      p02: this.getCurCia.extrel,
    }

    // this.loadingView = true
    await this.$axios
      .get('shoppingcart/catsbrands/', {
        params: curparams,
      })
      .then((response) => {
        this.$store.dispatch(
          'shoppingcart/categories/setCustomers',
          response.data
        )
        // this.loadingView = false
      })
  },
  data() {
    return {
      selected_customer: null,
      snackbar: false,
      snackbarText: 'No implementado',
      snackbarColor: 'info',
      snackTimeout: 3000,
      loading: false,
      overlay: false,
    }
  },
  computed: {
    ...mapGetters('shoppingcart/cart', [
      'getCartItems',
      'getCartTotalPrice',
      'getCartCustomer',
    ]),
    ...mapGetters('shoppingcart/categories', ['getCustomers']),
    ...mapGetters('sistema', ['getCurCia']),
  },

  watch: {
    selected_customer(newCustomer) {
      if (!newCustomer) {
        newCustomer = {
          id: 0,
          name: 'nocli',
          email: 'noemail@numen.pa',
          tel: '',
        }
      }
      this.setCartCustomer(newCustomer)
    },
  },

  methods: {
    ...mapActions('shoppingcart/cart', ['setCartCustomer']),
    ...mapActions('shoppingcart/orders', ['createOrder']),
    async goToCheckout() {
      this.snackbar = true
      if (this.getCartItems.length === 0) {
        this.snackbarColor = 'warning'
        this.snackbarText = 'Your shopping cart is empty'
        return
      }

      if (!this.getCartCustomer) {
        this.snackbarColor = 'warning'
        this.snackbarText = 'Please select a customer'
        return
      }

      this.snackbarColor = 'info'
      this.snackbarText = 'Creating order...'

      this.loading = true

      await this.createOrder()
      this.snackbarColor = 'success'
      this.snackbarText = 'Order created successfully'
      this.snackbarTimeout = 5000

      setTimeout(() => {
        this.loading = false
        this.$router.push('/shoppingcart/ordersview')
      }, 2000)
    },
  },
}
</script>

<style scoped>
.custom-loader {
  animation: loader 1s infinite;
  display: flex;
}
@-moz-keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}
@-webkit-keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}
@-o-keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}
@keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
