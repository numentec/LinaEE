<template>
  <v-card class="mx-4 my-4" max-width="400">
    <v-img :src="product.image" height="200px"></v-img>
    <v-card-title>{{ product.name }}</v-card-title>
    <v-card-subtitle>{{ product.price | currency }}</v-card-subtitle>
    <v-card-text>
      {{ product.description }}
    </v-card-text>
    <v-card-actions>
      <v-row align="center" justify="space-between">
        <v-col cols="6">
          <v-btn icon @click="decreaseQuantity">
            <v-icon>mdi-minus</v-icon>
          </v-btn>
          <v-text-field
            v-model="quantity"
            type="number"
            min="1"
            class="mx-2"
            style="max-width: 50px"
          ></v-text-field>
          <v-btn icon @click="increaseQuantity">
            <v-icon>mdi-plus</v-icon>
          </v-btn>
        </v-col>
        <v-col cols="6" class="text-right">
          <v-btn color="primary" @click="addToCart">Agregar al carrito</v-btn>
        </v-col>
      </v-row>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'ShopCard',
  filters: {
    currency(value) {
      return new Intl.NumberFormat('es-PA', {
        style: 'currency',
        currency: 'USD',
      }).format(value)
    },
  },
  props: {
    product: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      quantity: 1,
    }
  },
  methods: {
    increaseQuantity() {
      this.quantity++
    },
    decreaseQuantity() {
      if (this.quantity > 1) {
        this.quantity--
      }
    },
    addToCart() {
      this.$emit('add-to-cart', {
        product: this.product,
        quantity: this.quantity,
      })
    },
  },
}
</script>

<style scoped>
.mx-2 {
  margin-left: 8px;
  margin-right: 8px;
}
</style>
