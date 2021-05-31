/* eslint-disable no-console */
<template>
  <v-card
    class="mx-auto my-4"
    max-width="300"
    style="height: 100%"
    :loading="loadingView"
    @click="goView"
  >
    <v-img :src="fav.image" height="200px"></v-img>

    <v-card-title>
      <v-badge :value="!fav.todos" color="warning" icon="mdi-account-star">
        {{ fav.name }}
      </v-badge>
    </v-card-title>

    <v-card-subtitle>Usuario: {{ fav.username }}</v-card-subtitle>

    <v-card-actions>
      <v-btn icon color="success" @click.stop="onEdit(fav.id)">
        <v-icon>mdi-pencil</v-icon>
      </v-btn>
      <v-btn icon color="error" @click.stop="onDelete(fav.id)">
        <v-icon>mdi-trash-can</v-icon>
      </v-btn>

      <v-spacer></v-spacer>

      <v-btn icon @click.stop="descrip = !descrip">
        <v-icon>{{ descrip ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
      </v-btn>
    </v-card-actions>

    <v-expand-transition>
      <div v-show="descrip">
        <v-divider></v-divider>
        <v-card-text>{{ fav.descrip }}</v-card-text>
      </div>
    </v-expand-transition>
  </v-card>
</template>

<script>
export default {
  name: 'FavoritoCard',
  props: {
    fav: {
      type: Object,
      default: () => ({}),
    },
    onDelete: {
      type: Function,
      default: () => ({}),
    },
    onEdit: {
      type: Function,
      default: () => ({}),
    },
  },
  data: () => ({
    descrip: false,
    loadingView: false,
  }),
  activated() {
    this.loadingView = false
  },
  methods: {
    goView() {
      this.loadingView = true
      this.$router.push(this.fav.link)
    },
  },
}
</script>

<style lang="scss" scoped></style>
