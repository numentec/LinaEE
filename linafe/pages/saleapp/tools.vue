<template>
  <v-row>
    <v-col class="text-center">
      <img src="/uc2.jpg" alt="***** En Construcción *****" class="mb-5" />
      <blockquote class="blockquote">
        <h5>{{ page_name }}</h5>
        &#8220;En desarrollo por el equipo de NumenTec.&#8221;
        <footer>
          <small>
            <em>&mdash;www.numentec.com</em>
          </small>
        </footer>
      </blockquote>
    </v-col>
  </v-row>
</template>

<script>
export default {
  data() {
    return {
      page_name: 'tools',
    }
  },
  created() {
    this.page_name = this.$nuxt.$route.name.toUpperCase()
  },
}
</script>
