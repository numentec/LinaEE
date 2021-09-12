/* eslint-disable no-console */
<template>
  <div>
    <v-container class="d-flex align-content-start flex-wrap" min-height="200">
      <template v-for="curqry in queries">
        <FavoritoCard
          v-if="accReject(curqry.perm)"
          :key="curqry.id"
          :qry="true"
          class="pa-2"
          :fav="curqry"
          card-type="tool"
        />
      </template>
    </v-container>
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
import { mapGetters } from 'vuex'
import FavoritoCard from '~/components/linabi/FavoritoCard.vue'

export default {
  name: 'WMSTools',
  components: {
    FavoritoCard,
  },
  async asyncData({ $axios, error }) {
    try {
      const { data } = await $axios.get('wms/wmsqueries/', {
        params: { qtype: 'tool' },
      })
      return {
        queries: data,
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
      queries: [],
      snackbar: false,
      perms: this.$auth.user.perms,
    }
  },
  computed: {
    ...mapGetters(['loggedInUser']),
  },
  methods: {
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
      title: 'WMS Tools',
    }
  },
}
</script>
