<template>
  <v-img
    :src="imgSrc"
    :lazy-src="lazySrc"
    contain
    :max-width="$vuetify.breakpoint.mobile ? swidth : lwidth"
    @error="onImgError"
  >
    <template v-slot:placeholder>
      <v-row class="fill-height ma-0" align="center" justify="center">
        <v-progress-circular
          indeterminate
          color="grey lighten-5"
        ></v-progress-circular>
      </v-row>
    </template>
  </v-img>
</template>

<script>
export default {
  name: 'ImgForGrid',
  props: {
    imgFile: {
      type: String,
      required: true,
      default: '/no_image.png',
    },
    swidth: {
      type: Number,
      default: 100,
    },
    lwidth: {
      type: Number,
      default: 200,
    },
  },
  data() {
    return {
      lazySrc: this.$config.fotosURL + 'nophoto_sm.png',
      imgSrc: this.imgFile,
    }
  },
  computed: {},
  watch: {
    imgFile() {
      this.imgSrc = this.imgFile
    },
  },
  methods: {
    onImgError() {
      this.imgSrc = '/no_image.png'
      this.$emit('no-image')
    },
  },
}
</script>

<style scoped></style>
