/* eslint-disable no-console */
<template>
  <div>
    <div>
      <v-breadcrumbs :items="breadCrumbsItems"></v-breadcrumbs>
    </div>
    <v-card
      class="d-flex align-content-start flex-wrap"
      flat
      tile
      min-height="200"
    >
      <FavoritoCard
        v-for="curfav in favoritos"
        :key="curfav.id"
        class="pa-2"
        :on-delete="delFavorito"
        :on-edit="editFavorito"
        :fav="curfav"
      />
    </v-card>
    <v-snackbar v-model="snackbar" timeout="2000">
      No implementado
      <template v-slot:action="{ attrs }">
        <v-btn color="secondary" text v-bind="attrs" @click="snackbar = false">
          Cerrar
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import FavoritoCard from '~/components/linabi/FavoritoCard.vue'

export default {
  name: 'Favoritos',
  components: {
    FavoritoCard,
  },
  async asyncData({ $axios, error }) {
    try {
      const { data } = await $axios.get('linabi/favoritos/')
      return {
        favoritos: data,
      }
    } catch (err) {
      if (err.response) {
        error({
          statusCode: err.response.status,
          message: err.response.data.detail,
        })
      } else {
        error({
          statusCode: 503,
          message: 'No se pudo cargar la lista. Intente luego',
        })
      }
    }
  },
  data() {
    return {
      favoritos: [],
      snackbar: false,
    }
  },
  computed: {
    ...mapState('linabi/favoritos', ['breadCrumbsItems']),
  },
  created() {
    const defaultBC = [
      {
        text: 'FAVORITOS',
        exact: true,
        append: true,
        replace: true,
        to: '/linabi/favoritos',
        nuxt: true,
      },
    ]
    this.$store.dispatch('linabi/favoritos/setBreadCrumbsItems', defaultBC)
  },
  methods: {
    delFavorito(favid) {
      this.snackbar = true
    },
    editFavorito(favid) {
      this.snackbar = true
    },
  },
  head() {
    return {
      title: 'Favoritos',
    }
  },
}
</script>
