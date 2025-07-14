<template>
  <v-card :outlined="outlined" :tile="outlined" class="mx-auto">
    <v-toolbar dense flat rounded>
      <v-card-title>Order Summary</v-card-title>
    </v-toolbar>
    <v-divider></v-divider>
    <v-card-text>
      <v-row>
        <v-col cols="12">
          <v-row dense class="mx-2 mb-0">
            <v-col cols="10">
              <div class="my-0">
                <v-autocomplete
                  v-model="cartCustomer"
                  :label="isCustomerCart ? 'Saleperson' : 'Customer'"
                  return-object
                  :items="customersList"
                  item-text="name"
                  item-value="id"
                  dense
                  background-color="#eafaff"
                  rounded
                  clearable
                  single-line
                  class="mb-0"
                ></v-autocomplete>
              </div>
            </v-col>
            <v-col cols="2">
              <div class="text-center my-0">
                <v-dialog v-model="dialog" max-width="500px">
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      large
                      icon
                      :disabled="!isSelectedCustomer"
                      color="green lighten-1"
                      v-bind="attrs"
                      v-on="on"
                      @click="openDialog"
                    >
                      <v-icon>mdi-email-edit</v-icon>
                    </v-btn>
                  </template>
                  <v-card>
                    <v-card-title class="headline">
                      {{ customerName }}
                    </v-card-title>
                    <v-card-text>
                      <v-row>
                        <v-col cols="12">
                          <v-text-field
                            v-model="editEmail"
                            label="email"
                            class="centered-input"
                          ></v-text-field>
                        </v-col>
                        <v-col cols="12">
                          <v-text-field
                            v-model="editTel"
                            label="Tel"
                            class="centered-input"
                          ></v-text-field>
                        </v-col>
                      </v-row>
                    </v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn
                        color="green darken-1"
                        text
                        @click.stop="
                          editCustomer()
                          closeDialog()
                        "
                      >
                        Update
                      </v-btn>
                    </v-card-actions>
                    <v-btn
                      icon
                      class="ma-2"
                      style="position: absolute; top: 0; right: 0"
                      @click="closeDialog"
                    >
                      <v-icon>mdi-close</v-icon>
                    </v-btn>
                  </v-card>
                </v-dialog>
              </div>
            </v-col>
          </v-row>
          <v-row
            dense
            justify="space-between"
            :class="isMobile ? 'mb-0' : 'mb-4'"
            class="mx-2 mt-0"
          >
            <div class="mt-0">
              {{ customerEmail }}
            </div>
            <div v-if="!isMobile" class="mt-0 mb-4">
              {{ customerTel }}
            </div>
          </v-row>
          <v-row v-if="isMobile" dense class="mx-2 mt-0 mb-4">
            <div class="mt-0">
              {{ customerTel }}
            </div>
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
              @click="$emit('go-to-checkout')"
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
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'CartOrderSummary',
  props: {
    customersList: {
      type: Array,
      required: true,
    },
    loading: {
      type: Boolean,
      default: false,
    },
    outlined: {
      type: Boolean,
      default: false,
    },
    isCustomerCart: {
      type: Boolean,
      default: false,
    },
  },

  data() {
    return {
      editEmail: '',
      editTel: '',
      dialog: false,
    }
  },

  computed: {
    ...mapGetters('shoppingcart/cart', [
      'getCartTotalPrice',
      'getCartCustomer',
    ]),

    cartCustomer: {
      get() {
        return this.getCartCustomer
      },
      set(value) {
        this.setCartCustomer(value)
      },
    },

    customerName() {
      return this.cartCustomer?.name || 'Customer'
    },
    customerEmail() {
      return this.cartCustomer?.email || 'email'
    },
    customerTel() {
      let t = ''
      if (this.cartCustomer) {
        t = this.cartCustomer?.tel ? `tel: ${this.cartCustomer?.tel}` : ''
      }
      return t
    },
    isMobile() {
      return this.$vuetify.breakpoint.smAndDown
    },
    isSelectedCustomer() {
      // if (this.cartCustomer) return true
      const k = Object.keys(this.cartCustomer ?? {})
      return this.cartCustomer && k.length !== 0
    },
  },

  mounted() {
    if (this.customersList.length > 0 && this.isCustomerCart) {
      this.cartCustomer = this.customersList[0] // Establece el primer ítem como predeterminado
    }
  },

  methods: {
    ...mapActions('shoppingcart/cart', ['setCartCustomer']),

    editCustomer() {
      this.setCartCustomer({
        ...this.cartCustomer,
        email: this.editEmail,
        tel: this.editTel,
      })
    },

    openDialog() {
      this.editEmail = this.cartCustomer?.email || ''
      this.editTel = this.cartCustomer?.tel || ''
    },

    closeDialog() {
      this.dialog = false
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
