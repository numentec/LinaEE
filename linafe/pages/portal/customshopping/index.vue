<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="4">
        <v-skeleton-loader
          v-bind="attrs"
          type="card-avatar, article, actions"
        ></v-skeleton-loader>

        <v-skeleton-loader
          v-bind="attrs"
          type="date-picker"
        ></v-skeleton-loader>
      </v-col>

      <v-col cols="12" md="4">
        <v-skeleton-loader
          v-bind="attrs"
          type="article, actions"
        ></v-skeleton-loader>

        <v-skeleton-loader
          v-bind="attrs"
          type="table-heading, list-item-two-line, image, table-tfoot"
        ></v-skeleton-loader>
      </v-col>

      <v-col cols="12" md="4">
        <v-skeleton-loader
          v-bind="attrs"
          type="list-item-avatar, divider, list-item-three-line, card-heading, image, actions"
        ></v-skeleton-loader>

        <v-skeleton-loader
          v-bind="attrs"
          type="list-item-avatar-three-line, image, article"
        ></v-skeleton-loader>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'CustomShopping',
  layout: 'publicapps',
  data: () => ({
    attrs: {
      class: 'mb-6',
      boilerplate: false,
      elevation: 2,
    },
  }),
  head() {
    return {
      title: 'Shopping Cart',
      meta: [
        {
          hid: 'description',
          name: 'description',
          content: 'A custom shopping cart page for LinaEE Portal.',
        },
      ],
    }
  },
}
</script>
