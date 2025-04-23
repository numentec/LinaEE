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
            v-model="filterOrdersBy"
            solo
            flat
            hide-details
            prepend-inner-icon="mdi-magnify"
            label="Search"
            dense
            rounded
            clearable
            @input="updateFilter"
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
          <v-menu v-model="vmenu" :close-on-content-click="false" offset-y>
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
              <v-list-group v-show="!isListView" no-action>
                <template v-slot:activator>
                  <v-list-item-content>
                    <v-list-item-title>Download Order</v-list-item-title>
                  </v-list-item-content>
                </template>
                <v-list-item @click="pdfD">
                  <v-list-item-title>PDF</v-list-item-title>
                  <v-list-item-icon>
                    <v-icon>mdi-file-pdf-box</v-icon>
                  </v-list-item-icon>
                </v-list-item>
                <v-list-item @click="csvD">
                  <v-list-item-title>CSV</v-list-item-title>
                  <v-list-item-icon>
                    <v-icon>mdi-file-delimited-outline</v-icon>
                  </v-list-item-icon>
                </v-list-item>
              </v-list-group>

              <v-list-item @click="printOrderPDF">
                <v-list-item-title>Print</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-toolbar>
      </v-row>
    </div>
    <div id="orders-view">
      <v-row>
        <v-col cols="12" :md="isListView ? 12 : 8">
          <v-card v-show="!isListView">
            <v-toolbar dense flat rounded>
              <v-card-title>{{ `Order # ${cOrderID}` }}</v-card-title>
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
              <v-row
                v-for="(item, index) in curOrder ? curOrder.items : []"
                :key="item.id"
              >
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
            <v-list-item-group
              :key="listKey"
              v-model="selectedListItem"
              color="primary"
            >
              <OrderListItem
                v-for="order in orders"
                :key="order.id"
                ref="selectedOrder"
                :order="order"
                @resend-mail="snackbar = true"
                @order-clicked="goToOrder"
              />
            </v-list-item-group>
          </v-list>
        </v-col>
        <v-col v-show="!isListView" cols="12" md="4">
          <OrderSummary
            :cur-order="curOrder"
            :hide-controls="hideControls"
            class="sticky-summary"
            @go-to-products="goToProducts"
          />
        </v-col>
      </v-row>
    </div>
    <v-snackbar v-model="snackbar" timeout="3000" :color="snackbarColor" dark>
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
import html2pdf from 'html2pdf.js'

function debounce(func, delay) {
  let timeout
  return function (...args) {
    clearTimeout(timeout) // Limpia el temporizador anterior
    timeout = setTimeout(() => {
      func.apply(this, args) // Ejecuta la función después del retraso
    }, delay)
  }
}

function filtro(func) {
  return function (...args) {
    return new Promise((resolve) => {
      debounce(() => {
        resolve(func.apply(this, args))
      }, 500)()
    })
  }
}

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
      snackbarColor: 'info',
      loading: false,
      showSummary: false,
      filterOrdersBy: '',
      listKey: 0, // Agregar una clave dinámica para forzar la actualización de la lista
      hideControls: false,
      vmenu: false,
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
    curOrderItems() {
      return this.curOrder ? this.curOrder.items : []
    },
    isMobile() {
      return this.$vuetify.breakpoint.mobile
    },
    cOrderID() {
      return this.curOrder ? String(this.curOrder?.id) : ''
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
    // filterOrdersBy() {
    //   this.listKey += 1 // Incrementar la clave dinámica cuando el filtro cambie
    // },
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
      'setFilterCriteria',
      'csvDownload',
      'pdfDownload',
    ]),
    async goToProducts() {
      this.loading = true
      await this.$router.push('/shoppingcart/categories/products')
      this.loading = false
      this.vmenu = false
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
      this.vmenu = false
      this.isListView = !this.isListView
      this.$nextTick(() => {
        if (this.isListView) {
          this.selectedListItem = this.curIndex
          const selectedOrder = this.$refs.selectedOrder?.[
            this.selectedListItem
          ]

          if (selectedOrder) {
            // console.log('SELECTED ORDER: ', selectedOrder)
            selectedOrder.$el.scrollIntoView({
              behavior: 'smooth',
              block: 'center',
            })
          }
        } else {
          window.scrollTo(0, 0)
        }
      })
    },
    goToOrder(id) {
      // await this.setCurrentIndex(this.getIndexByOrderID(id))
      this.changeView()
    },
    async updateFilter() {
      await filtro(this.setFilterCriteria.bind(this))(this.filterOrdersBy)
      this.listKey += 1 // Incrementar la clave dinámica cuando el filtro cambie
    },
    async printOrderPDF() {
      this.vmenu = false
      this.snackbar = true
      this.snackbarText = 'Generating PDF'

      const element = document.getElementById('orders-view')
      const opt = {
        margin: 0.25,
        filename: `order_${this.cOrderID}.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: {
          scale: 4,
          letterRendering: true,
          useCORS: true,
        },
        jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' },
      }

      this.hideControls = true

      await html2pdf().from(element).set(opt).save()

      this.hideControls = false
    },

    // Download CSV
    // This function is called when the user clicks on the CSV download button
    // It uses the csvDownload method from the Vuex store to download the CSV file
    // It also handles errors and shows a snackbar with the download status
    csvD() {
      this.vmenu = false

      this.snackbarText = 'Downloading csv'
      this.snackbarColor = 'info'
      this.snackbar = true

      try {
        this.csvDownload(this.cOrderID)
      } catch (error) {
        console.error('Error downloading CSV:', error)
        this.snackbarText = error.message
        this.snackbarColor = 'error'
        this.snackbar = true
      }
    },

    // Download PDF
    // This function is called when the user clicks on the PDF download button
    // It uses the pdfDownload method from the Vuex store to download the PDF file
    // It also handles errors and shows a snackbar with the download status
    pdfD() {
      this.vmenu = false

      this.snackbarText = 'Downloading pdf'
      this.snackbarColor = 'info'
      this.snackbar = true

      try {
        this.pdfDownload(this.cOrderID)
      } catch (error) {
        console.error('Error downloading CSV:', error)
        this.snackbarText = error.message
        this.snackbarColor = 'error'
        this.snackbar = true
      }
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
