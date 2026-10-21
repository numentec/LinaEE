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
            <v-card-title>{{ cartTitle }}</v-card-title>
            <v-tooltip v-if="getCartOrderId" bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  icon
                  small
                  v-bind="attrs"
                  v-on="on"
                  @click.stop="unlinkOrder"
                >
                  <v-icon>mdi-link-variant-off</v-icon>
                </v-btn>
              </template>
              <span>Unlink order (checkout will create a new order)</span>
            </v-tooltip>
            <v-spacer></v-spacer>

            <v-btn
              v-show="getCartItems.length > 0"
              icon
              small
              @click.stop="clearCart()"
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
              :customers-list="customersList"
              :loading="loading"
              :outlined="true"
              @go-to-checkout="goToCheckout"
            />
          </v-expand-transition>
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
        <CartOrderSummary
          :customers-list="customersList"
          :loading="loading"
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
    <SendOrderEmailDialog
      v-model="emailDialog"
      :order-id="emailOrder.id"
      :send-to="emailOrder.sendto || emailOrder.customer_email || ''"
      :attachments="emailConf.attachments"
      :include-images="emailConf.include_images"
      @sent="onEmailSent"
      @skipped="finishCheckout"
      @error="onEmailError"
    />
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import CartCard from '@/components/saleapp/CartCard.vue'
import CartOrderSummary from '@/components/saleapp/CartOrderSummary.vue'
import SendOrderEmailDialog from '@/components/saleapp/SendOrderEmailDialog.vue'

export default {
  name: 'SaleAppCart',
  components: {
    CartCard,
    CartOrderSummary,
    SendOrderEmailDialog,
  },
  async fetch() {
    const curparams = {
      type: 'CLI',
      cia: this.getCurCia.extrel,
    }

    // this.loadingView = true
    await this.$axios
      .get('saleapp/catsbrands/', {
        params: curparams,
      })
      .then((response) => {
        this.$store.dispatch('saleapp/categories/setCustomers', response.data)
        // this.loadingView = false
      })
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
      emailDialog: false,
      emailOrder: {},
      emailConf: { attachments: 'pdf', include_images: false },
    }
  },
  computed: {
    ...mapGetters('saleapp/cart', [
      'getCartItems',
      'getCartTotalPrice',
      'getCartCustomer',
      'getCartOrderId',
    ]),
    ...mapGetters('saleapp/categories', ['getCustomers']),

    cartTitle() {
      return this.getCartOrderId
        ? `Editing order # ${this.getCartOrderId}`
        : 'Shopping Cart'
    },
    ...mapGetters('sistema', ['getCurCia']),

    customersList() {
      return JSON.parse(JSON.stringify(this.getCustomers))
    },

    isMobile() {
      return this.$vuetify.breakpoint.smAndDown
    },
    isXSmall() {
      return this.$vuetify.breakpoint.xsOnly
    },
  },

  // Mensaje enviado por otra vista al navegar al carrito (p.ej. Keep selling)
  activated() {
    const info = this.$route.params?.info
    if (info) {
      this.snackbarColor = 'info'
      this.snackbarText = info
      this.snackbarTimeout = 5000
      this.snackbar = true
    }
  },

  methods: {
    ...mapActions('saleapp/orders', ['createOrder', 'updateOrder']),
    ...mapActions('saleapp/cart', ['clearCart']),
    unlinkOrder() {
      this.$store.commit('saleapp/cart/SET_ORDER_ID', null)
    },
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

      const isUpdate = !!this.getCartOrderId

      this.snackbarColor = 'info'
      this.snackbarText = isUpdate ? 'Updating order...' : 'Creating order...'

      this.loading = true

      try {
        const { order, email } = isUpdate
          ? await this.updateOrder()
          : await this.createOrder()

        this.snackbarColor = 'success'
        this.snackbarText = isUpdate
          ? 'Order updated successfully'
          : 'Order created successfully'
        if (email?.action === 'sent') {
          this.snackbarText += ' and emailed to the customer'
        }
        this.snackbarTimeout = 5000

        // Política "ask": se pregunta antes de enviar el correo
        if (email?.action === 'ask') {
          this.emailOrder = order
          this.emailConf = email
          this.emailDialog = true
          return
        }

        this.finishCheckout()
      } catch (error) {
        this.loading = false
        this.snackbarColor = 'error'
        this.snackbarText =
          `Failed to ${isUpdate ? 'update' : 'create'} order: ` +
          (error.response?.data?.non_field_errors?.[0] ||
            error.response?.data?.message ||
            error.message)
        this.snackbarTimeout = 5000
      }
    },
    finishCheckout() {
      setTimeout(() => {
        this.loading = false
        this.$router.push('/saleapp/ordersview')
      }, 2000)
    },
    onEmailSent() {
      this.snackbarColor = 'success'
      this.snackbarText = `Order # ${this.emailOrder.id} is being emailed`
      this.snackbar = true
      this.finishCheckout()
    },
    onEmailError(error) {
      this.snackbarColor = 'error'
      this.snackbarText =
        'Failed to email order: ' +
        (error?.response?.data?.attachments?.[0] ||
          error?.response?.data?.error ||
          error?.message)
      this.snackbar = true
      this.finishCheckout()
    },
  },
}
</script>

<style scoped></style>
