<template>
  <div>
    <v-img :src="imgSrc" :lazy-src="lazySrc" contain max-width="175">
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
    fullPath: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      lazySrc: this.$config.fotosURL + 'nophoto_sm.png',
    }
  },
  computed: {
    imgSrc() {
      let imgsrc = this.imgFile.value
      if (!this.fullPath) {
        imgsrc =
          this.$config.fotosURL + this.imgFile.value + this.$config.fotosExt
      }

      return imgsrc
    },
    imgID() {
      return this.imgFile.value
    },
  },
  mounted() {},
}
</script>

<style scoped></style>
