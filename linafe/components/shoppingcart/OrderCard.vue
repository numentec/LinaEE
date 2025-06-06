<template>
  <v-card flat width="1100" max-height="200" class="my-2">
    <v-row dense>
      <v-col cols="4" class="d-flex justify-center shrink">
        <v-img
          :src="imgSrc"
          class="mr-4"
          :max-width="cardWidth"
          :height="cardHeight"
          contain
          :lazy-src="lazySrc"
          @error="onImgError"
          @load="addImage({ id: item.id, url: imgSrc })"
        ></v-img>
      </v-col>
      <v-col sm="8" md="6" align-self="stretch">
        <v-row no-gutters>
          <h3>{{ item.sku }}</h3>
        </v-row>
        <v-row no-gutters>
          <p>{{ item.name }}</p>
        </v-row>
        <v-row v-if="!isMobile" no-gutters>
          <v-chip color="green lighten-2" text-color="white" class="my-4">
            {{ formatedPrice }}
          </v-chip>
        </v-row>
        <v-row v-if="!isMobile" no-gutters>
          <v-text-field
            :value="item.quantity"
            readonly
            filled
            rounded
            dense
            class="centered-input mx-2 mt-2 mb-6"
          ></v-text-field>
        </v-row>
        <v-row v-if="isMobile" no-gutters justify="space-between">
          <v-col cols="6">
            <p class="green--text">{{ formatedPrice }}</p>
          </v-col>
          <v-col cols="6">
            <p class="light-blue--text lighten-2">
              {{ `qty. ${item.quantity}` }}
            </p>
          </v-col>
        </v-row>
      </v-col>
      <v-col
        v-if="!isMobile"
        cols="2"
        class="d-flex flex-column justify-center"
      >
        <div :class="[isMobile ? 'h4-aux' : 'h3-aux', 'text-center']">
          {{
            `${itemSubTotal.toLocaleString('es-US', {
              style: 'currency',
              currency: 'USD',
            })}`
          }}
        </div>
      </v-col>
    </v-row>
    <v-row v-if="isMobile" no-gutters justify="center">
      <div class="h4-aux">
        {{
          `${itemSubTotal.toLocaleString('es-US', {
            style: 'currency',
            currency: 'USD',
          })}`
        }}
      </div>
    </v-row>
  </v-card>
</template>

<script>
import { mapActions, mapGetters, mapState } from 'vuex'
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
      lazySrc: '/no_image.png',
      imgError: false,
    }
  },
  computed: {
    ...mapGetters('shoppingcart/products', ['getImage']),
    ...mapState('shoppingcart/orders', ['getLoadingStatus']),

    isMobile() {
      return this.$vuetify.breakpoint.mobile
    },

    cardWidth() {
      return this.isMobile ? 75 : 120
    },

    cardHeight() {
      return this.isMobile ? 100 : 160
    },

    imgSrc() {
      if (this.imgError) {
        return '/no_image.png'
      }

      // return this.getImage(this.item.id) || this.item.image
      return (
        this.getImage(this.item.id) || this.$config.fotosURL + this.item.image
      )
    },

    itemSubTotal() {
      return this.item.price * this.item.quantity
    },
    formatedPrice() {
      return Number(this.item.price).toLocaleString('es-US', {
        style: 'currency',
        currency: 'USD',
      })
    },
  },

  // watch: {
  //   // Observa cambios en el item para cargar la imagen
  //   item: {
  //     immediate: true, // Ejecuta el watcher al montar el componente
  //     handler(newItem) {
  //       this.loadImage(newItem)
  //     },
  //   },
  // },
  // mounted() {
  //   this.loadImage(this.item)
  // },
  // beforeDestroy() {
  //   this.lazySrc = null
  // },

  methods: {
    ...mapActions('shoppingcart/products', ['addImage']),

    onImgError() {
      this.imgError = true
      this.$emit('no-image')
    },

    async loadImage(item) {
      if (!item) return

      const imageUrl =
        this.getImage(item.id) || this.$config.fotosURL + item.image

      try {
        const response = await fetch(imageUrl)
        const blob = await response.blob()
        this.lazySrc = await this.convertToBase64(blob)
      } catch (error) {
        console.error('Error loading image:', error)
        this.lazySrc = '/no_image.png'
      }
    },

    convertToBase64(blob) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onloadend = () => resolve(reader.result)
        reader.onerror = reject
        reader.readAsDataURL(blob)
      })
    },
  },
}
</script>

<style scoped>
.centered-input >>> input {
  text-align: center;
}
.h2-aux {
  font-size: 1.5em; /* Tamaño de fuente equivalente a <h2> */
  font-weight: bold; /* Peso de fuente equivalente a <h2> */
  margin: 0.83em 0; /* Margen equivalente a <h2> */
}

.h3-aux {
  font-size: 1.17em; /* Tamaño de fuente equivalente a <h3> */
  font-weight: bold; /* Peso de fuente equivalente a <h3> */
  margin: 1em 0; /* Margen equivalente a <h3> */
}

.h4-aux {
  font-size: 1.17em; /* Tamaño de fuente equivalente a <h4> */
  font-weight: bold; /* Peso de fuente equivalente a <h4> */
  margin: 1.33em 0; /* Margen equivalente a <h4> */
}

.h6-aux {
  font-size: 0.67em; /* Tamaño de fuente equivalente a <h6> */
  font-weight: bold; /* Peso de fuente equivalente a <h6> */
  margin: 1.67em 0; /* Margen equivalente a <h6> */
}
/* .v-card {
  max-width: 600px;
} */
</style>
