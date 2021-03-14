<template>
  <div>
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
        :fav="curfav"
      />
    </v-card>
  </div>
</template>

<script>
import FavoritoCard from '~/components/linabi/FavoritoCard.vue'

export default {
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
    }
  },
  methods: {
    delFavorito(favid) {
      alert(favid)
    },
  },
  head() {
    return {
      title: 'Favoritos',
    }
  },
}
</script>
