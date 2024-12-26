<template>
  <v-card
    class="mx-4 my-4"
    max-width="300"
    :loading="loadingView"
    @click="goToView"
  >
    <v-img
      :src="imgSrc"
      height="400px"
      cover
      :lazy-src="lazySrc"
      @error="onImgError"
    >
      <template v-slot:placeholder>
        <v-row class="fill-height ma-0" align="center" justify="center">
          <v-progress-circular
            indeterminate
            color="grey lighten-5"
          ></v-progress-circular>
        </v-row>
      </template>
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
      imgSrc: this.$config.fotosURL + this.category.image,
      lazySrc: this.$config.fotosURL + 'nophoto_sm.png',
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
    onImgError() {
      this.imgSrc = '/no_image.png'
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
</style>
