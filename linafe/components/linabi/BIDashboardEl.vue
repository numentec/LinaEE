/* eslint-disable no-console */
<template>
  <v-card
    class="mx-auto my-4"
    :width="el.width"
    style="height: 100%"
    :shaped="false"
    :loading="loadingView"
    @click="goView"
  >
    <v-img v-if="!qry" :src="el.image" height="200px"></v-img>

    <v-card-title v-if="qry">
      <v-icon large left color="orange darken-2">{{
        typeOpc[cardType].icon
      }}</v-icon>
      {{ el.name }}
    </v-card-title>
    <v-card-title v-else>
      <v-badge :value="!el.todos" color="warning" icon="mdi-account-star">
        {{ el.name }}
      </v-badge>
    </v-card-title>

    <v-card-subtitle v-if="qry">{{ el.qdescrip }}</v-card-subtitle>
    <v-card-subtitle v-else>Usuario: {{ el.username }}</v-card-subtitle>

    <v-card-actions v-if="!qry">
      <v-btn icon color="success" @click.stop="onEdit(el.id)">
        <v-icon>mdi-pencil</v-icon>
      </v-btn>
      <v-btn icon color="error" @click.stop="onDelete(el.id)">
        <v-icon>mdi-trash-can</v-icon>
      </v-btn>

      <v-spacer></v-spacer>

      <v-btn icon @click.stop="descrip = !descrip">
        <v-icon>{{ descrip ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
      </v-btn>
    </v-card-actions>

    <v-expand-transition v-if="!qry">
      <div v-show="descrip">
        <v-divider></v-divider>
        <v-card-text>{{ el.descrip }}</v-card-text>
      </div>
    </v-expand-transition>
  </v-card>
</template>

<script>
const typeOpc = {
  map: {
    icon: 'mdi-text-search',
  },
  chart: {
    icon: 'mdi-file-chart-outline',
  },
  table: {
    icon: 'mdi-tools',
  },
}

export default {
  name: 'BIDashboardEl',
  props: {
    qry: {
      type: Boolean,
      default: false,
    },
    el: {
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
    cardType: {
      type: String,
      default: 'chart',
    },
  },

  async fetch() {
    // Lista de plantillas xlsx
    await this.$axios
      .get('linabi/extbidashboard')
      .then((response) => response.data)
  },

  data() {
    return {
      descrip: false,
      loadingView: false,
      perms: this.$auth.user.perms,
      typeOpc,
    }
  },
  computed: {},
  activated() {
    this.loadingView = false
  },
  methods: {
    goView() {
      this.loadingView = true
      this.$router.push(this.el.link)
    },
    refreshData() {
      this.$fetch()
    },
  },
}
</script>

<style lang="scss" scoped></style>
