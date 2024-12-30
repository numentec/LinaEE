<template>
  <v-card flat width="1200" class="my-2">
    <v-card-text>
      <v-row>
        <v-col cols="4" class="d-flex justify-center shrink">
          <v-img
            :src="item.product.image"
            class="mr-4"
            max-width="150"
            height="200"
          ></v-img>
        </v-col>
        <v-col cols="6">
          <h3>SKU: {{ item.product.id }}</h3>
          <p>{{ item.product.description }}</p>
          <v-chip color="green lighten-2" text-color="white" class="my-4">
            {{
              `${item.price.toLocaleString('es-US', {
                style: 'currency',
                currency: 'USD',
              })}`
            }}
          </v-chip>
          <v-text-field
            :value="item.quantity"
            readonly
            filled
            rounded
            dense
            class="centered-input mx-2 mt-6"
            :prepend-inner-icon="preIcon"
            append-icon="mdi-plus"
            @click:prepend-inner="decreaseQuantity(item.index)"
            @click:append="increaseQuantity(item.index)"
          ></v-text-field>
        </v-col>
        <v-col cols="2" class="d-flex flex-column justify-space-between">
          <div class="text-center">
            <v-btn large icon color="green lighten-1">
              <v-icon large>mdi-pencil-box-outline</v-icon>
            </v-btn>
          </div>
          <h3 class="text-center">
            {{
              `${itemSubTotal.toLocaleString('es-US', {
                style: 'currency',
                currency: 'USD',
              })}`
            }}
          </h3>
          <div class="text-center">
            <v-btn
              large
              icon
              color="red lighten-1"
              @click="removeFromCart(item.product.id)"
            >
              <v-icon large>{{ delIcon }}</v-icon>
            </v-btn>
          </div>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
// Guiarse con ventas/tools/qryprod.vue
export default {
  name: 'CartCard',
  props: {
    item: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      quantity: this.item.quantity,
    }
  },
  computed: {
    ...mapGetters('shoppingcart/cart', [
      'getCartItemCount',
      'getCartItemQuantity',
      'getCartTotalPrice',
    ]),
    itemSubTotal() {
      return this.item.price * this.item.quantity
    },
    preIcon() {
      return this.item.quantity > 1 ? 'mdi-minus' : 'mdi-delete-outline'
    },
    delIcon() {
      return this.getCartItemCount > 1
        ? 'mdi-delete-outline'
        : 'mdi-delete-empty'
    },
  },
  methods: {
    ...mapActions('shoppingcart/cart', [
      'removeFromCart',
      'clearCart',
      'increaseQuantity',
      'decreaseQuantity',
    ]),
  },
}
</script>

<style scoped>
.centered-input >>> input {
  text-align: center;
}
/* .v-card {
  max-width: 600px;
} */
</style>
