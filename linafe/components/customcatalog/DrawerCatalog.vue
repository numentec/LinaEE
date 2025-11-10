<template>
  <v-list shaped>
    <v-list-item link nuxt :to="`/portal/customshopping/${customerULID}/`">
      <v-list-item-icon>
        <v-icon>mdi-bookshelf</v-icon>
      </v-list-item-icon>
      <v-list-item-content>
        <v-list-item-title class="title">Catalogs</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
    <v-list-item
      link
      nuxt
      :to="`/portal/customshopping/${customerULID}/${catalogToken}`"
    >
      <v-list-item-icon>
        <v-icon>mdi-sort-alphabetical-variant</v-icon>
      </v-list-item-icon>
      <v-list-item-content>
        <v-list-item-title class="title">All products</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
    <v-list-item link nuxt :to="`/portal/customshopping/${customerId}/cart`">
      <v-list-item-icon>
        <v-icon>mdi-cart-outline</v-icon>
      </v-list-item-icon>
      <v-list-item-content>
        <v-list-item-title class="title">Go to Cart</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
    <v-list-group prepend-icon="mdi-shape-outline">
      <template v-slot:activator>
        <v-list-item-content>
          <v-list-item-title>Categories</v-list-item-title>
        </v-list-item-content>
      </template>
      <v-list-item
        v-for="category in categories"
        :key="category.title"
        nuxt
        :to="category.to"
        router
        exact
      >
        <v-list-item-content>
          <v-list-item-title>{{ category.title }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list-group>
  </v-list>
</template>

<script>
import { mapGetters } from 'vuex'
const categories = [
  { title: 'Electronics', to: '' },
  { title: 'Books', to: '' },
  { title: 'Clothing', to: '' },
]
export default {
  data() {
    return {
      categories,
    }
  },
  computed: {
    ...mapGetters({
      customerId: 'customshopping/customcatalog/getCustomerId',
      customerULID: 'customshopping/customcatalog/getCustomerULID',
      catalogToken: 'customshopping/customcatalog/getCustomCatalogToken',
    }),
  },
}
</script>

<style lang="scss" scoped></style>
