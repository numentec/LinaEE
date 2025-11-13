<template>
  <v-hover>
    <template v-slot:default="{ hover }">
      <v-card
        :elevation="hover ? 5 : 0"
        :outlined="!hover"
        :class="['mx-4 my-4']"
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
        <v-overlay absolute :value="overlay">
          <v-progress-circular indeterminate size="32"></v-progress-circular>
        </v-overlay>
      </v-card>
    </template>
  </v-hover>
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
      overlay: false,
      imgSrc: this.category.img_full_path
        ? this.$config.publicURL + this.category.img_full_path
        : this.$config.fotosURL + this.category.image,
      // imgSrc: this.category.image,
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
    this.overlay = false
  },

  methods: {
    goToView() {
      this.loadingView = true
      this.overlay = true

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
        let catname = this.category.name

        if (this.isMobile) {
          catname = this.category.abreviated_name ?? catname
        }

        this.$router.push({
          path: this.category.link,
          query: { parent_id: this.category.id, category: catname },
        })
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
