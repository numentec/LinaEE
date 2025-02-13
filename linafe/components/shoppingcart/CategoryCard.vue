<template>
  <v-card
    class="mx-4 my-4"
    :max-width="cardWidth"
    :loading="loadingView"
    @click="goToView"
  >
    <v-img
      :src="imgSrc"
      :height="imgHeight"
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
        <v-toolbar-title
          :class="[
            'white--text',
            isMobile ? 'toolbar-title--small' : 'toolbar-title',
          ]"
        >
          {{ category.name }}
        </v-toolbar-title>
      </v-toolbar>
    </v-img>
  </v-card>
</template>

<script>
export default {
  name: 'CategoryCard',
  props: {
    category: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      loadingView: false,
      // imgSrc: this.$config.fotosURL + this.category.image,
      imgSrc: this.category.image,
      lazySrc: this.$config.fotosURL + 'nophoto_sm.png',
    }
  },

  computed: {
    isMobile() {
      return this.$vuetify.breakpoint.mobile
    },
    cardWidth() {
      return this.isMobile ? 125 : 300
    },
    cardHeight() {
      return this.isMobile ? 250 : 600
    },
    imgHeight() {
      return this.isMobile ? '200px' : '400px'
    },
  },

  activated() {
    this.loadingView = false
  },

  methods: {
    goToView() {
      this.loadingView = true
      this.$emit('card-clicked', {
        key: this.category.type,
        value: this.category.id,
      })
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
.toolbar-title {
  font-size: 1.25rem; /* Tamaño de fuente por defecto */
}

.toolbar-title--small {
  font-size: 1rem; /* Tamaño de fuente más pequeño para dispositivos móviles */
}
</style>
