/* eslint-disable no-console */
<template>
  <div>
    <v-card
      class="d-flex align-content-start flex-wrap"
      flat
      tile
      min-height="200"
    >
      <template v-for="curfav in favoritos">
        <FavoritoCard
          v-if="accReject(curfav.perm)"
          :key="curfav.id"
          class="pa-2"
          :on-delete="delFavorito"
          :on-edit="editFavorito"
          :fav="curfav"
        />
      </template>
    </v-card>
    <v-snackbar v-model="snackbar" timeout="2000">
      No implementado
      <template v-slot:action="{ attrs }">
        <v-btn color="secondary" text v-bind="attrs" @click="snackbar = false">
          Cerrar
        </v-btn>
      </template>
    </v-snackbar>
    <v-dialog v-model="noAccess" persistent max-width="300">
      <v-card>
        <v-card-title class="headline"> Acceso Denegado </v-card-title>
        <v-card-text>
          No tiene autorización para ejecutar este comando
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click.stop="noAccess = false">
            Aceptar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
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
      noAccess: false,
      perms: this.$auth.user.perms,
    }
  },
  computed: {
    ...mapState('linabi/favoritos', ['breadCrumbsItems']),
    ...mapGetters(['loggedInUser']),
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
    accReject(perm) {
      let showv = false
      if (this.loggedInUser.is_superuser || this.perms[perm]) {
        showv = true
      }
      return showv
    },
  },
  head() {
    return {
      title: 'Favoritos',
    }
  },
}
</script>
