<template>
  <v-card
    class="mx-4 my-4"
    max-width="300"
    :loading="loadingView"
    @click="goToView"
  >
    <v-img :src="category.image" height="400px" cover>
      <v-toolbar
        flat
        color="rgba(0, 0, 0, 0.65)"
        bottom
        absolute
        style="width: 100%"
      >
        <v-toolbar-title class="white--text">
          {{ category.name }}
        </v-toolbar-title>
      </v-toolbar>
    </v-img>
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
