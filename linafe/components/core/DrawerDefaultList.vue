<template>
  <v-list shaped>
    <v-list-item nuxt to="/">
      <v-list-item-icon>
        <v-icon>mdi-home</v-icon>
      </v-list-item-icon>
      <v-list-item-content>
        <v-list-item-title class="title">Inico</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
    <v-list-group
      v-for="item in modulosDisponibles"
      v-show="getCurUser.perms[item.perm]"
      :key="item.title"
      :prepend-icon="item.icon"
      no-action
    >
      <template v-slot:activator>
        <v-list-item-content>
          <v-list-item-title v-text="item.title" />
        </v-list-item-content>
      </template>
      <v-list-item
        v-for="subitem in item.items"
        v-show="getCurUser.perms[subitem.perm]"
        :key="subitem.title"
        nuxt
        :to="subitem.to"
        router
        exact
      >
        <v-list-item-content>
          <v-list-item-title v-text="subitem.title" />
        </v-list-item-content>
      </v-list-item>
    </v-list-group>
  </v-list>
</template>

<script>
import { mapGetters } from 'vuex'
import { modulos } from '~/assets/utilities'

export default {
  name: 'CoreDrawer',
  async fetch() {
    await this.$axios.get('modul-actives/').then((response) => {
      const modulosActivos = response.data
      this.modulos_disponibles = this.modulos.filter((el) => {
        return modulosActivos.find((element) => {
          return element.nombre === el.name
        })
      })
    })
  },
  data() {
    return {
      modulos_disponibles: [],
      modulos,
    }
  },

  computed: {
    ...mapGetters('sistema', ['getCurUser']),
    modulosDisponibles() {
      return this.modulos_disponibles
    },
  },
}
</script>

<style></style>
