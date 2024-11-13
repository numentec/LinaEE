<template>
  <div>
    <div class="floating-header">
      <v-toolbar flat color="grey lighten-4">
        <v-select
          v-model="selected_brands"
          :items="brands"
          multiple
          label="Filter by brand"
          chips
          dense
        ></v-select>
        <v-spacer></v-spacer>
        <v-text-field
          v-show="cur_child_view == 'departments'"
          id="depatments"
          v-model="search_department"
          solo
          flat
          hide-details
          prepend-inner-icon="mdi-magnify"
          label="Search"
          dense
          rounded
          clearable
        ></v-text-field>
        <v-text-field
          v-show="cur_child_view == 'categoriesmain'"
          id="categories"
          v-model="search_category"
          solo
          flat
          hide-details
          prepend-inner-icon="mdi-magnify"
          label="Search"
          dense
          rounded
          clearable
        ></v-text-field>
        <v-text-field
          v-show="cur_child_view == 'categoriessub'"
          id="subcategories"
          v-model="search_subcategory"
          solo
          flat
          hide-details
          prepend-inner-icon="mdi-magnify"
          label="Search"
          dense
          rounded
          clearable
        ></v-text-field>
      </v-toolbar>
    </div>
    <div>
      <nuxt-child></nuxt-child>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      brands: ['Brand 1', 'Brand 2', 'Brand 3', 'Brand 4', 'Brand 5'],
      selected_brands: [],
      cur_child_view: 'departments',
      search_department: '',
      search_category: '',
      search_subcategory: '',
    }
  },

  provide() {
    return {
      selected_brands: this.selected_brands,
      search_department: this.search_department,
      search_category: this.search_category,
      search_subcategory: this.search_subcategory,
    }
  },
  computed: {},
}
</script>

<style scoped>
.floating-header {
  position: -webkit-sticky; /* Safari */
  position: sticky;
  top: 56px; /* Ajusta este valor según la altura de tu app-bar */
  z-index: 1000; /* Asegúrate de que esté por encima de otros elementos */
  background-color: white;
}
</style>
