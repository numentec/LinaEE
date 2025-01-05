<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="8">
        <v-card>
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
                  <v-btn color="green darken-1" text @click="goToCheckout">
                    Checkout
                  </v-btn>
                </v-row>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-snackbar v-model="snackbar" timeout="2000">
      No implementado
      <template v-slot:action="{ attrs }">
        <v-btn
          color="secondary"
          text
          v-bind="attrs"
          @click.stop="snackbar = false"
        >
          Cerrar
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
        }
      }
      this.setCartCustomer(newCustomer)
    },
  },

  methods: {
    ...mapActions('shoppingcart/cart', ['setCartCustomer']),
    goToCheckout() {
      this.snackbar = true
    },
  },
}
</script>

<style scoped>
/* Add any custom styles here */
</style>
