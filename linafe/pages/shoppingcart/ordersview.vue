<template>
  <v-container>
    <div class="floating-header">
      <v-row>
        <v-toolbar flat color="rgba(225, 250, 250, 0.5)">
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                class="mt-0 mb-2 ml-0"
                icon
                v-bind="attrs"
                color="cyan lighten-1"
                v-on="on"
                @click="$router.back()"
              >
                <v-icon>mdi-chevron-left</v-icon>
              </v-btn>
            </template>
            <span>Back to previous view</span>
          </v-tooltip>
          <v-spacer></v-spacer>
          <v-btn icon small @click="() => setCurrentIndex(0)">
            <v-icon>mdi-page-first</v-icon>
          </v-btn>
          <v-text-field
            :value="`${curIndex + 1} / ${ordersCount}`"
            readonly
            filled
            rounded
            dense
            class="centered-input mt-6"
            style="max-width: 200px"
            prepend-inner-icon="mdi-chevron-left"
            append-icon="mdi-chevron-right"
            @click:prepend-inner="() => goLeft()"
            @click:append="() => goRight()"
          ></v-text-field>
          <v-btn icon small @click="() => setCurrentIndex(ordersCount - 1)">
            <v-icon>mdi-page-last</v-icon>
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn
            v-show="!isMobile"
            class="ma-2"
            icon
            color="cyan lighten-1"
            @click="viewMode = !viewMode"
          >
            <v-icon v-if="viewMode">mdi-format-list-text</v-icon>
            <v-icon v-else>mdi-view-grid</v-icon>
          </v-btn>
          <v-menu offset-y>
            <template v-slot:activator="{ on, attrs }">
              <v-btn icon color="cyan lighten-1" v-bind="attrs" v-on="on">
                <v-icon>mdi-dots-vertical</v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item @click="goToProducts">
                <v-list-item-title>Go to Cart</v-list-item-title>
              </v-list-item>
              <v-list-item @click="snackbar = true">
                <v-list-item-title>
                  {{ viewMode ? 'List view' : 'Grid view' }}
                </v-list-item-title>
              </v-list-item>
              <v-list-item @click="snackbar = true">
                <v-list-item-title>Option 3</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-toolbar>
      </v-row>
    </div>
    <v-row>
      <v-col cols="12" md="8">
        <v-card>
          <v-toolbar dense flat rounded>
            <v-card-title>{{ `Order # ${curOrder.id}` }}</v-card-title>
            <v-spacer></v-spacer>

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
            <OrderSummary
              v-show="showSummary"
              :cur-order="curOrder"
              :outlined="true"
              @go-to-products="goToProducts"
            />
          </v-expand-transition>
          <v-card-text>
            <v-row v-for="(item, index) in curOrder.items" :key="item.id">
              <v-col cols="12">
                <v-row dense><OrderCard :item="{ ...item, index }" /></v-row>
                <v-row dense><v-divider class="mb-0"></v-divider></v-row>
              </v-col>
            </v-row>
            <v-alert
              v-if="ordersCount.length === 0"
              border="bottom"
              colored-border
              type="warning"
            >
              <strong>There are not orders</strong>.
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <OrderSummary :cur-order="curOrder" @go-to-products="goToProducts" />
      </v-col>
    </v-row>
    <v-snackbar v-model="snackbar" timeout="3000">
      {{ snackbarText }}
      <template v-slot:action="{ attrs }">
        <v-btn
          color="secondary"
          text
          v-bind="attrs"
          @click.stop="snackbar = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import OrderCard from '@/components/shoppingcart/OrderCard.vue'
import OrderSummary from '@/components/shoppingcart/OrderSummary.vue'

export default {
  name: 'OrdersView',
  components: {
    OrderCard,
    OrderSummary,
  },

  async asyncData({ store, error }) {
    try {
      await store.dispatch('shoppingcart/orders/fetchOrders')
    } catch (err) {
      if (err.response) {
        error({
          statusCode: err.response.status,
          message: err.response.data.detail,
        })
      } else {
        error({
          statusCode: 503,
          message: 'Error fetching orders',
        })
      }
    }
  },

  data() {
    return {
      viewMode: true, // true for grid and false for list
      snackbar: false,
      snackbarText: 'No implementado',
      loading: false,
      showSummary: false,
    }
  },
  computed: {
    ...mapGetters('shoppingcart/orders', {
      curOrder: 'getCurrentOrder',
      curIndex: 'getCurrentIndex',
      curID: 'getCurrentID',
      lastID: 'getLastCreatedID',
      dataLoading: 'getLoadingStatus',
      ordersCount: 'getOrdersCount',
      getIndexByOrderID: 'getIndexByOrderID',
      getJustCreated: 'getJustCreated',
    }),
    ...mapGetters('sistema', ['getCurCia']),
    isMobile() {
      return this.$vuetify.breakpoint.mobile
    },
  },

  activated() {
    if (this.getJustCreated) {
      this.setJustCreated()
      if (this.lastID !== 0) {
        setTimeout(() => {
          this.setCurrentIndex(this.getIndexByOrderID(this.lastID))
        }, 1000)
      }
    }
  },

  methods: {
    ...mapActions('shoppingcart/orders', [
      'setCurrentIndex',
      'fetchOrders',
      'setJustCreated',
    ]),
    async goToProducts() {
      this.loading = true
      await this.$router.push('/shoppingcart/categories/products')
      this.loading = false
    },
    goLeft() {
      if (this.curIndex === 0) {
        return
      }
      this.setCurrentIndex(this.curIndex - 1)
    },
    goRight() {
      if (this.curIndex === this.ordersCount - 1) {
        return
      }
      this.setCurrentIndex(this.curIndex + 1)
    },
  },
}
</script>

<style scoped>
.floating-header {
  position: -webkit-sticky; /* Safari */
  position: sticky;
  top: 45px; /* Ajusta este valor según la altura de tu app-bar */
  z-index: 3; /* Asegúrate de que esté por encima de otros elementos pero por debajo del Drawer */
  background-color: white;
}
.centered-input >>> input {
  text-align: center;
}
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
