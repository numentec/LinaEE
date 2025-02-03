<template>
  <v-card flat width="1100" max-height="200" class="my-2">
    <v-card-text>
      <v-row dense>
        <v-col cols="4" class="d-flex justify-center shrink">
          <v-img
            :src="imgSrc"
            class="mr-4"
            :max-width="cardWidth"
            :height="cardHeight"
            :lazy-src="lazySrc"
            @error="onImgError"
            @load="addImage({ id: item.id, url: imgSrc })"
          ></v-img>
        </v-col>
        <v-col cols="6" align-self="stretch">
          <h3>SKU: {{ item.id }}</h3>
          <p>{{ item.name }}</p>
          <v-chip color="green lighten-2" text-color="white" class="my-4">
            {{ formattedPrice }}
          </v-chip>
          <v-text-field
            :value="item.quantity"
            readonly
            filled
            rounded
            dense
            class="centered-input mx-2 mt-2 mb-6"
          ></v-text-field>
        </v-col>
        <v-col cols="2" class="d-flex flex-column justify-center">
          <div :class="[isMobile ? 'h4-aux' : 'h2-aux', 'text-center']">
            {{
              `${itemSubTotal.toLocaleString('es-US', {
                style: 'currency',
                currency: 'USD',
              })}`
            }}
          </div>
        </v-col>
      </v-row>
    </v-card-text>
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
    formattedPrice() {
      return Number(this.item.price).toLocaleString('es-US', {
        style: 'currency',
        currency: 'USD',
      })
    },
  },
  methods: {
    ...mapActions('shoppingcart/products', ['addImage']),

    onImgError() {
      this.imgError = true
      this.$emit('no-image')
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

.h4-aux {
  font-size: 1.17em; /* Tamaño de fuente equivalente a <h4> */
  font-weight: bold; /* Peso de fuente equivalente a <h4> */
  margin: 1.33em 0; /* Margen equivalente a <h4> */
}
/* .v-card {
  max-width: 600px;
} */
</style>
