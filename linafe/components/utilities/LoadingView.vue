<template>
  <v-overlay :absolute="true" :z-index="1" :value="busyWith">
    <div>
      <v-progress-linear
        indeterminate
        color="yellow darken-2"
      ></v-progress-linear>
      <v-card-title>{{ message }}</v-card-title>
    </div>
  </v-overlay>
</template>

<script>
export default {
  name: 'LoadingView',
  props: {
    busyWith: {
      type: Boolean,
      required: true,
      default() {
        return false
      },
    },
    message: {
      type: String,
      required: false,
      default() {
        return 'Cargando...'
      },
    },
  },
}
</script>

<style lang="scss" scoped></style>
