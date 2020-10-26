<template>
  <div>
    <!-- <v-card class="mx-auto mt-5">
      <v-toolbar dense color="secondary" dark>
        <v-btn icon>
          <v-icon>mdi-dots-vertical</v-icon>
        </v-btn>
        <v-spacer />
        <v-toolbar-title>Compañías</v-toolbar-title>
        <v-spacer />
        <v-btn icon>
          <v-icon>mdi-magnify</v-icon>
        </v-btn>
      </v-toolbar>
      <v-card-text>
        <div>Word of the Day</div>
        <p class="display-1 text--primary">be•nev•o•lent</p>
        <p>adjective</p>
        <div class="text--primary">
          well meaning and kindly.<br />
          "a benevolent smile"
        </div>
      </v-card-text>
      <v-card-actions>
        <v-btn text color="deep-purple accent-4"> Learn More </v-btn>
      </v-card-actions>
    </v-card> -->
    <MaterialCard class="mt-10">
      <template v-slot:heading>
        <v-toolbar dense color="secondary" dark flat>
          <v-btn icon>
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
          <v-spacer />
          <v-toolbar-title>Compañías</v-toolbar-title>
          <v-spacer />
          <v-btn icon>
            <v-icon>mdi-magnify</v-icon>
          </v-btn>
        </v-toolbar>
      </template>
      <v-card-text>
        <v-data-table :headers="headers" :items="items" />
      </v-card-text>
    </MaterialCard>
  </div>
</template>

<script>
export default {
  components: {
    MaterialCard: () => import('~/components/core/MaterialCard'),
  },
  data() {
    return {
      page_name: 'page',
    }
  },

  created() {
    this.page_name = this.$nuxt.$route.name.toUpperCase()
  },
}
</script>
