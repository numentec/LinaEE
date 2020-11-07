<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="8" md="6">
      <div class="text-center">
        <h1 class="display-4 font-weight-black grey--text text-darken-1 mt-5">
          ERROR {{ statusCode }}
        </h1>
      </div>
      <v-alert
        border="right"
        colored-border
        type="error"
        class="title"
        elevation="2"
      >
        {{ message }}
      </v-alert>
      <h3 v-if="statusCode === 404">
        <NuxtLink to="/lina"> Home page </NuxtLink>
      </h3>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'LinaErrorPage',
  // layout: 'empty',
  props: {
    error: {
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      pageNotFound: '404 Not Found',
      otherError: 'An error occurred',
    }
  },
  computed: {
    statusCode() {
      return (this.error && this.error.statusCode) || 500
    },
    message() {
      return this.error.message
    },
  },
  head() {
    // const title =
    //   this.error.statusCode === 404 ? this.pageNotFound : this.otherError
    return {
      title: this.message,
    }
  },
}
</script>

<style scoped>
h1 {
  font-size: 20px;
}
</style>
