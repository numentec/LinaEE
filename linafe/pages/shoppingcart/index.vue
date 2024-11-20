<template>
  <div class="shopping-cart">
    <v-btn block color="primary lighten-2" @click="$router.push(link)">
      Start
    </v-btn>
  </div>
</template>

<script>
export default {
  data() {
    return {
      link: '/shoppingcart/categories/departments',
    }
  },
}
</script>

<style scoped>
.shopping-cart {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
</style>
