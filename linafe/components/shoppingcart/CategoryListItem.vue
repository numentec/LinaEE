<template>
  <div>
    <v-divider></v-divider>
    <v-list-item class="ml-0 mr-2 pl-0 pr-1" @click="goToView">
      <v-list-item-avatar rounded size="100" left class="mx-0 pl-0 pr-1">
        <v-img
          :src="imgSrc"
          :height="imgHeight"
          contain
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
        </v-img>
      </v-list-item-avatar>
      <v-list-item-content>
        <v-list-item-title
          :class="isMobile ? 'toolbar-title--small' : 'toolbar-title'"
        >
          {{ category.name }}
        </v-list-item-title>
      </v-list-item-content>
    </v-list-item>
  </div>
</template>

<script>
export default {
  name: 'CategoryListItem',
  props: {
    category: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      loadingView: false,
      imgSrc: this.$config.fotosURL + this.category.image,
      // imgSrc: this.category.image,
      lazySrc: this.$config.fotosURL + 'nophoto_sm.png',
    }
  },

  computed: {
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
.toolbar-title {
  font-size: 1.25rem; /* Tamaño de fuente por defecto */
}

.toolbar-title--small {
  font-size: 1rem; /* Tamaño de fuente más pequeño para dispositivos móviles */
}
</style>
