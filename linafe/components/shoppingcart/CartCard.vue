<template>
  <v-card flat width="1100" max-height="225" class="my-2">
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
      <v-col sm="8" md="6" align-self="stretch">
        <v-row no-gutters>
          <h3>SKU: {{ item.id }}</h3>
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
            :prepend-inner-icon="preIcon"
            append-icon="mdi-plus"
            @click:prepend-inner="() => decreaseQuantity(item.index)"
            @click:append="() => increaseQuantity(item.index)"
          ></v-text-field>
        </v-row>
        <v-row v-if="isMobile" no-gutters justify="space-between">
          <v-col cols="3">
            <p class="green--text">{{ formatedPrice }}</p>
          </v-col>
          <v-col cols="9">
            <v-text-field
              :value="item.quantity"
              readonly
              filled
              rounded
              dense
              class="centered-input"
              :prepend-inner-icon="preIcon"
              append-icon="mdi-plus"
              @click:prepend-inner="() => decreaseQuantity(item.index)"
              @click:append="() => increaseQuantity(item.index)"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-col>
      <v-col
        v-if="!isMobile"
        cols="2"
        class="d-flex flex-column justify-space-around"
      >
        <div class="text-center">
          <v-dialog v-model="dialog" max-width="500px">
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                large
                icon
                color="green lighten-1"
                :disabled="isLoading"
                v-bind="attrs"
                v-on="on"
                @click="openDialog"
              >
                <v-icon large>mdi-pencil-box-outline</v-icon>
              </v-btn>
            </template>
            <v-card>
              <v-card-title class="headline">{{ item.name }}</v-card-title>
              <v-card-subtitle>{{ item.description }}</v-card-subtitle>
              <v-card-text>
                <v-row>
                  <v-col cols="12">
                    <v-text-field
                      v-model="itemQuantity"
                      label="Cantidad"
                      type="number"
                      placeholder="1"
                      class="centered-input"
                      prepend-icon="mdi-minus"
                      append-icon="mdi-plus"
                      @click:prepend="decreaseItemQuantity"
                      @click:append="increaseItemQuantity"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-text-field
                      v-if="showPrice"
                      v-model="itemPrice"
                      label="Precio"
                      class="centered-input"
                      prefix="$"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="green darken-1" text @click.stop="updateItem">
                  Update
                </v-btn>
              </v-card-actions>
              <v-btn
                icon
                class="ma-2"
                style="position: absolute; top: 0; right: 0"
                @click="closeDialog"
              >
                <v-icon>mdi-close</v-icon>
              </v-btn>
            </v-card>
          </v-dialog>
        </div>
        <h3 class="text-center">
          {{
            `${itemSubTotal.toLocaleString('es-US', {
              style: 'currency',
              currency: 'USD',
            })}`
          }}
        </h3>
        <div class="text-center">
          <v-btn
            large
            icon
            color="red lighten-1"
            :disabled="isLoading"
            @click="removeItemID(item.id)"
          >
            <v-icon large>{{ delIcon }}</v-icon>
          </v-btn>
        </div>
      </v-col>
    </v-row>
    <v-row v-if="isMobile" no-gutters justify="space-between">
      <div class="text-center">
        <v-dialog v-model="dialog" max-width="500px">
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              large
              icon
              color="green lighten-1"
              :disabled="isLoading"
              v-bind="attrs"
              v-on="on"
              @click="openDialog"
            >
              <v-icon large>mdi-pencil-box-outline</v-icon>
            </v-btn>
          </template>
          <v-card>
            <v-card-title class="headline">{{ item.name }}</v-card-title>
            <v-card-subtitle>{{ item.description }}</v-card-subtitle>
            <v-card-text>
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    v-model="itemQuantity"
                    label="Cantidad"
                    type="number"
                    placeholder="1"
                    class="centered-input"
                    prepend-icon="mdi-minus"
                    append-icon="mdi-plus"
                    @click:prepend="decreaseItemQuantity"
                    @click:append="increaseItemQuantity"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="itemPrice"
                    label="Precio"
                    class="centered-input"
                    prefix="$"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="green darken-1" text @click.stop="updateItem">
                Update
              </v-btn>
            </v-card-actions>
            <v-btn
              icon
              class="ma-2"
              style="position: absolute; top: 0; right: 0"
              @click="closeDialog"
            >
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-card>
        </v-dialog>
      </div>
      <h3 class="text-center">
        {{
          `${itemSubTotal.toLocaleString('es-US', {
            style: 'currency',
            currency: 'USD',
          })}`
        }}
      </h3>
      <div class="text-center">
        <v-btn
          large
          icon
          color="red lighten-1"
          :disabled="isLoading"
          @click="removeItemID(item.id)"
        >
          <v-icon large>{{ delIcon }}</v-icon>
        </v-btn>
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
    showPrice: {
      type: Boolean,
      default: true,
    },
    minQty: {
      type: Number,
      default: 1,
    },
    maxQty: {
      type: Number,
      default: 999,
    },
  },
  data() {
    return {
      itemQuantity: this.item.quantity,
      itemPrice: this.item.price,
      lazySrc: '/no_image.png',
      imgError: false,
      dialog: false,
    }
  },
  computed: {
    ...mapGetters('shoppingcart/cart', [
      'getCartItemCount',
      'getCartItemQuantity',
      'getCartTotalPrice',
    ]),
    ...mapGetters('shoppingcart/products', ['getImage']),
    ...mapState('shoppingcart/orders', ['isLoading']),

    isMobile() {
      return this.$vuetify.breakpoint.mobile
    },
    imgHeight() {
      return this.isMobile ? '100px' : '200px'
    },
    cardHeight() {
      return this.isMobile ? 100 : 160
    },
    cardWidth() {
      return this.isMobile ? 75 : 120
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
    preIcon() {
      return this.item.quantity > 1 ? 'mdi-minus' : 'mdi-delete-outline'
    },
    delIcon() {
      return this.getCartItemCount > 1
        ? 'mdi-delete-outline'
        : 'mdi-delete-empty'
    },
    formatedPrice() {
      return Number(this.item.price).toLocaleString('es-US', {
        style: 'currency',
        currency: 'USD',
      })
    },
  },
  methods: {
    ...mapActions('shoppingcart/cart', [
      'decreaseQuantity',
      'increaseQuantity',
      'removeItemID',
      'clearCart',
    ]),
    ...mapActions('shoppingcart/products', ['addImage']),
    decreaseItemQuantity() {
      if (this.itemQuantity > 1) {
        this.itemQuantity--
      }
    },
    increaseItemQuantity() {
      this.itemQuantity++
    },
    updateItem() {
      if (this.itemQuantity > 0) {
        this.$store.commit('shoppingcart/cart/UPDATE_ITEM', {
          index: this.item.index,
          quantity: parseInt(this.itemQuantity, 10),
          price: parseFloat(parseFloat(this.itemPrice).toFixed(2)),
        })
        this.dialog = false
      }
    },
    openDialog() {
      this.itemQuantity = this.item.quantity
      this.itemPrice = this.item.price
      if (this.itemQuantity === 0) {
        this.itemQuantity = 1
      }
    },
    closeDialog() {
      this.itemQuantity = this.item.quantity
      this.itemPrice = this.item.price
      this.dialog = false
    },
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
/* .v-card {
  max-width: 600px;
} */
</style>
