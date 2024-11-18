<template>
  <v-card
    class="mx-4 my-4"
    max-width="300"
    :loading="loadingView"
    @click="goToView"
  >
    <v-img :src="category.image" height="400px" cover></v-img>
    <v-card flat tile width="100%">
      <v-card-title>{{ category.name }}</v-card-title>
      <v-card-text>
        {{ category.description }}
      </v-card-text>
    </v-card>
  </v-card>
</template>

<script>
export default {
  name: 'ShopCard',
  props: {
    category: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      loadingView: false,
      quantity: 1,
    }
  },
  activated() {
    this.loadingView = false
  },
  methods: {
    goToView() {
      this.loadingView = true
      if (
        this.category.link === null ||
        this.category.link === '' ||
        this.category.link === undefined
      ) {
        this.$router.push('/shoppingcart/categories/departments')
      } else {
        this.$router.push(this.category.link)
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
</style>
