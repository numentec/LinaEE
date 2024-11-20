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
          v-if="product.quantity > 0"
          class="ma-2"
          color="rgba(0, 0, 0, 0.65)"
          text-color="white"
        >
          {{ product.quantity }}
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
        <v-btn color="deep-purple lighten-2" fab small dark @click="makeAction">
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-card>
</template>

<script>
export default {
  name: 'ShopCard',
  props: {
    product: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      loadingView: false,
    }
  },
  activated() {
    this.loadingView = false
  },
  methods: {
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

      setTimeout(() => (this.loadingView = false), 2000)
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
