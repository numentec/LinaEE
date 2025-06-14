<template>
  <div>
    <v-divider></v-divider>
    <v-list-item
      class="ml-0 mr-2 pl-0 pr-1"
      @click="$emit('click', { imgID, imgSrc })"
    >
      <v-list-item-avatar rounded size="100" left class="mx-0 pl-0 pr-1">
        <v-img
          :src="imgSrc"
          :height="imgHeight"
          contain
          :lazy-src="lazySrc"
          @error="onImgError"
          @load="addImage({ id: product.id, url: imgSrc })"
        >
          <v-app-bar flat color="rgba(0, 0, 0, 0)">
            <v-chip
              v-show="addedQuantity > 0"
              class="ma-2"
              color="rgba(0, 0, 0, 0.65)"
              text-color="white"
              small
            >
              {{ addedQuantity }}
            </v-chip>
          </v-app-bar>
        </v-img>
      </v-list-item-avatar>
      <v-list-item-content>
        <v-list-item-title>{{ product.id }}</v-list-item-title>
        <v-list-item-subtitle>{{ product.name }}</v-list-item-subtitle>
        <v-list-item-subtitle>
          <v-row justify="space-between" class="mx-1">
            <div class="green--text">{{ formatedPrice }}</div>
            <div class="light-blue--text lighten-2">
              {{ inStock }}
            </div>
          </v-row>
        </v-list-item-subtitle>
      </v-list-item-content>
      <v-list-item-icon>
        <v-dialog v-model="dialog" max-width="500px">
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              color="deep-purple lighten-2"
              fab
              x-small
              dark
              class="mt-4"
              v-bind="attrs"
              v-on="on"
              @click="openDialog"
            >
              <v-icon>mdi-cart-plus</v-icon>
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
                    v-if="showPrice"
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
              @click="closeDialog"
            >
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-card>
        </v-dialog>
      </v-list-item-icon>
    </v-list-item>
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
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'ProductListItem',
  props: {
    product: {
      type: Object,
      required: true,
    },
    showPrice: {
      type: Boolean,
      default: true,
    },
    minQty: {
      type: Number,
      default: 1,
    },
    maxQty: {
      type: Number,
      default: 999,
    },
  },

  data() {
    return {
      loadingView: false,
      snackbar: false,
      dialog: false,
      cartquantity: 0,
      cartprice: this.product.price,
      tmpCartQuantity: 0,
      tmpCartPrice: this.product.price,
      setNoImage: false,
      lazySrc: '/no_image.png',
      imgError: false,
    }
  },

  computed: {
    ...mapGetters('shoppingcart/cart', ['getItemQuantityById']),
    ...mapGetters('shoppingcart/products', ['getImage']),

    isMobile() {
      return this.$vuetify.breakpoint.mobile
    },
    sz() {
      // screen size
      return this.$vuetify.breakpoint.name
    },

    imgHeight() {
      return this.isMobile ? '100px' : '200px'
    },
    cardHeight() {
      return this.isMobile ? 280 : 450
    },
    cardWidth() {
      return this.isMobile ? 140 : 225
    },

    addedQuantity() {
      return this.getItemQuantityById(this.product.id)
    },

    imgSrc() {
      if (this.imgError) {
        return '/no_image.png'
      }

      // return this.getImage(this.product.id) || this.product.image
      return (
        this.getImage(this.product.id) ||
        this.$config.fotosURL + this.product.image
      )
    },

    imgID() {
      const imgx = this.getImage(this.product.id) || this.product.image

      const imgName = imgx.substring(
        imgx.lastIndexOf('/') + 1,
        imgx.lastIndexOf('.')
      )

      return imgName === '/' ? 'no_image' : imgName
    },

    formatedPrice() {
      return Number(this.product.price).toLocaleString('es-US', {
        style: 'currency',
        currency: 'USD',
      })
    },

    inStock() {
      return this.isMobile
        ? `Stk: ${this.product.instock}`
        : `In Stock: ${this.product.instock}`
    },
  },

  watch: {
    cartquantity(value) {
      if (isNaN(value)) {
        this.cartquantity = 0
      }
    },
  },

  methods: {
    ...mapActions('shoppingcart/cart', ['addToCart']),
    ...mapActions('shoppingcart/products', ['addImage']),

    goToView() {
      this.loadingView = true
      const link = this.product.link || this.$route.path
      this.$router.push(link)
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
        const { id, name, description, instock, brand } = this.product

        this.addToCart({
          id,
          name,
          description,
          instock,
          quantity: Number(this.cartquantity, 10),
          price: this.cartprice,
          brand,
        })
        this.dialog = false
      }
    },
    openDialog() {
      this.tmpCartQuantity = this.cartquantity
      this.tmpCartPrice = this.cartprice
      if (this.cartquantity === 0) {
        this.cartquantity = 1
      }
    },
    closeDialog() {
      this.cartquantity = this.tmpCartQuantity
      this.cartprice = this.tmpCartPrice
      this.dialog = false
    },
    onImgError() {
      this.imgError = true
      this.$emit('no-image')
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
