<template>
  <v-card
    class="mx-4 my-4"
    max-width="300"
    :loading="loadingView"
    @click="goToView"
  >
    <!-- <v-badge color="green" content="6" bottom overlap>
      <v-img :src="product.image" height="400px" cover></v-img>
    </v-badge> -->
    <v-img :src="product.image" height="400px" cover>
      <v-app-bar flat color="rgba(0, 0, 0, 0)">
        <v-chip
          v-if="cartquantity > 0"
          class="ma-2"
          color="rgba(0, 0, 0, 0.65)"
          text-color="white"
        >
          {{ cartquantity }}
        </v-chip>
      </v-app-bar>
    </v-img>
    <v-card flat tile width="100%">
      <v-card-actions>
        <v-card-title>{{ product.name }}</v-card-title>
        <v-spacer></v-spacer>
        <v-chip color="green lighten-2" text-color="white">
          {{
            `${product.price.toLocaleString('es-US', {
              style: 'currency',
              currency: 'USD',
            })}`
          }}
        </v-chip>
      </v-card-actions>
      <v-card-actions>
        <v-chip color="light-blue lighten-2" text-color="white">
          {{ `In Stock: ${product.instock}` }}
        </v-chip>
        <v-spacer></v-spacer>
        <v-dialog v-model="dialog" max-width="500px">
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              color="deep-purple lighten-2"
              fab
              small
              dark
              v-bind="attrs"
              v-on="on"
              @click="openDialog"
            >
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </template>
          <v-card>
            <v-card-title class="headline">{{ product.name }}</v-card-title>
            <v-card-subtitle>{{ product.description }}</v-card-subtitle>
            <v-card-text>
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    v-model="cartquantity"
                    label="Cantidad"
                    type="number"
                    placeholder="1"
                    class="centered-input"
                    prepend-icon="mdi-minus"
                    append-icon="mdi-plus"
                    @click:prepend="decreaseQuantity"
                    @click:append="increaseQuantity"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="cartprice"
                    label="Precio"
                    class="centered-input"
                    prefix="$"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="green darken-1" text @click.stop="addProdToCart"
                >Add to Cart</v-btn
              >
            </v-card-actions>
            <v-btn
              icon
              class="ma-2"
              style="position: absolute; top: 0; right: 0"
              @click="dialog = false"
            >
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-card>
        </v-dialog>
      </v-card-actions>
    </v-card>
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
  </v-card>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  name: 'ProductCard',
  props: {
    product: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      loadingView: false,
      snackbar: false,
      dialog: false,
      cartquantity: 0,
      cartprice: this.product.price,
    }
  },
  watch: {
    cartquantity(value) {
      if (isNaN(value)) {
        this.cartquantity = 0
      }
    },
  },
  activated() {
    this.loadingView = false
  },
  methods: {
    ...mapActions('shoppingcart/cart', ['addToCart']),
    goToView() {
      this.loadingView = true
      if (
        this.product.link === null ||
        this.product.link === '' ||
        this.product.link === undefined
      ) {
        this.$router.push('/shoppingcart/categories/departments')
      } else {
        this.$router.push(this.product.link)
      }
    },
    makeAction() {
      this.loadingView = true
      this.snackbar = true

      setTimeout(() => (this.loadingView = false), 2000)
    },
    decreaseQuantity() {
      if (this.cartquantity > 0) {
        this.cartquantity--
      }
    },
    increaseQuantity() {
      this.cartquantity++
    },
    addProdToCart() {
      if (this.cartquantity > 0) {
        this.addToCart({
          product: { ...this.product },
          quantity: Number(this.cartquantity, 10),
          price: this.cartprice,
        })
        this.dialog = false
      }
    },
    openDialog() {
      if (this.cartquantity === 0) {
        this.cartquantity = 1
      }
    },
  },
}
</script>

<style scoped>
.mx-2 {
  margin-left: 8px;
  margin-right: 8px;
}
.centered-input >>> input {
  text-align: center;
}
</style>
