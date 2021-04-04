<template>
  <div>
    <v-img :src="imgSrc" :lazy-src="lazySrc" contain max-width="200">
      <template v-slot:placeholder>
        <v-row class="fill-height ma-0" align="center" justify="center">
          <v-progress-circular
            indeterminate
            color="grey lighten-5"
          ></v-progress-circular>
        </v-row>
      </template>
    </v-img>
  </div>
</template>

<script>
export default {
  name: 'ImgForGrid',
  props: {
    imgFile: {
      type: Object,
      required: true,
      default: () => {},
    },
  },
  data() {
    return {
      lazySrc: this.$config.fotosURL + 'nophoto_sm.png',
    }
  },
  computed: {
    imgSrc() {
      return this.$config.fotosURL + this.imgFile.value + this.$config.fotosExt
    },
    imgID() {
      return this.imgFile.value
    },
  },
}
</script>

<style scoped></style>
