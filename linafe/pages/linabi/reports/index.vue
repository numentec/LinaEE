<template>
  <v-row>
    <v-col class="text-center">
      <blockquote class="blockquote">
        <h3>
          <v-btn color="primary" :loading="loading" @click="goToSalesReport">
            Sales Reports
          </v-btn>
        </h3>
        <footer>
          <small>
            <em>numen.pa</em>
          </small>
        </footer>
      </blockquote>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'Reportes',
  data() {
    return {
      page_name: 'page',
      fi: new Date(new Date().getFullYear(), 0, 1),
      ff: new Date(new Date().getFullYear(), 11, 31),
      loading: false,
    }
  },
  created() {
    this.page_name = this.$nuxt.$route.name.toUpperCase()
  },
  activated() {
    this.loading = false
  },
  methods: {
    goToSalesReport() {
      this.loading = true
      const route = `/linabi/reports/rpt-pivotsales/?row=CLIENTE&fechini=${this.fi
        .toISOString()
        .slice(0, 10)}&fechfin=${this.ff
        .toISOString()
        .slice(0, 10)}&filtered=true`

      this.$router.push(route)
    },
  },
}
</script>
