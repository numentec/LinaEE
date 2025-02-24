<template>
  <v-container>
    <div class="floating-header mt-0 mx-0">
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
          <v-btn
            v-if="!isListView"
            icon
            small
            @click="() => setCurrentIndex(0)"
          >
            <v-icon>mdi-page-first</v-icon>
          </v-btn>
          <v-text-field
            v-if="!isListView"
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
          <v-btn
            v-if="!isListView"
            icon
            small
            @click="() => setCurrentIndex(ordersCount - 1)"
          >
            <v-icon>mdi-page-last</v-icon>
          </v-btn>
          <v-text-field
            v-show="isListView"
            v-model="searchOrders"
            solo
            flat
            hide-details
            prepend-inner-icon="mdi-magnify"
            label="Search"
            dense
            rounded
            clearable
          ></v-text-field>
          <v-spacer></v-spacer>
          <v-btn
            v-show="!isMobile"
            class="ma-2"
            icon
            color="cyan lighten-1"
            @click="changeView"
          >
            <v-icon v-if="isListView">mdi-view-grid</v-icon>
            <v-icon v-else>mdi-format-list-text</v-icon>
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
              <v-list-item @click="changeView">
                <v-list-item-title>
                  {{ isListView ? 'Grid view' : 'List view' }}
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
      <v-col cols="12" :md="isListView ? 12 : 8">
        <v-card v-show="!isListView">
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
        <v-list v-show="isListView" nav class="px-0">
          <v-list-item-group v-model="selectedListItem" color="primary">
            <template v-for="order in filteredOrders">
              <OrderListItem
                :key="order.id"
                :order="order"
                @resend-mail="snackbar = true"
                @order-clicked="goToOrder"
              />
            </template>
          </v-list-item-group>
        </v-list>
      </v-col>
      <v-col v-show="!isListView" cols="12" md="4">
        <OrderSummary
          :cur-order="curOrder"
          class="sticky-summary"
          @go-to-products="goToProducts"
        />
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
import OrderListItem from '@/components/shoppingcart/OrderListItem.vue'
import OrderSummary from '@/components/shoppingcart/OrderSummary.vue'

export default {
  name: 'OrdersView',
  components: {
    OrderCard,
    OrderSummary,
    OrderListItem,
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
      isListView: true, // true for list and false for grid
      selectedListItem: 0,
      snackbar: false,
      snackbarText: 'No implementado',
      loading: false,
      showSummary: false,
      searchOrders: '',
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
      orders: 'getOrders',
    }),
    ...mapGetters('sistema', ['getCurCia']),
    isMobile() {
      return this.$vuetify.breakpoint.mobile
    },
    filteredOrders() {
      return this.orders.filter((order) => {
        if (!this.searchOrders) {
          return true
        }
        const searchOrders = this.searchOrders.toLowerCase()
        return (
          order.id.toString().toLowerCase().includes(searchOrders) ||
          order.customer_name.toLowerCase().includes(searchOrders)
        )
      })
    },
  },

  watch: {
    selectedListItem(newIndex, oldIndex) {
      let curIndex = 0

      if (oldIndex) {
        curIndex = oldIndex
      }

      if (newIndex) {
        curIndex = newIndex
      }

      this.setCurrentIndex(curIndex)
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
    setCurIndex() {
      this.setCurrentIndex(this.selectedListItem)
    },
    changeView() {
      if (!this.isListView) {
        this.selectedListItem = this.curIndex
      }
      this.isListView = !this.isListView
    },
    async goToOrder(id) {
      await this.setCurrentIndex(this.getIndexByOrderID(id))
      this.changeView()
    },
  },
}
</script>

<style scoped>
.floating-header {
  position: -webkit-sticky; /* Safari */
  position: sticky;
  top: 40px; /* Ajusta este valor según la altura de tu app-bar */
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
.sticky-summary {
  position: -webkit-sticky;
  position: sticky;
  top: 125px;
  z-index: 2;
}
</style>
