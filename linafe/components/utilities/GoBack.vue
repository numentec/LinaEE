<template>
  <div class="ml-0 px-0">
    <v-tooltip bottom>
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          icon
          v-bind="attrs"
          class="ml-0"
          v-on="on"
          @click="$router.back()"
        >
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>
      </template>
      <span>Volver a vista anterior</span>
    </v-tooltip>
  </div>
</template>

<script>
export default {}
</script>

<style lang="scss" scoped></style>
