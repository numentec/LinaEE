<template>
  <div>
    <v-img
      :src="imgSrc"
      :lazy-src="lazySrc"
      contain
      max-width="175"
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
  </div>
</template>

<script>
export default {
  name: 'ImgForGrid',
  props: {
    imgFile: {
      type: String,
      required: true,
      default: 'noimg.jpg',
    },
  },
  data() {
    return {
      lazySrc: this.$config.fotosURL + 'nophoto_sm.png',
      imgErr: false,
    }
  },
  computed: {
    imgSrc() {
      let imgsrc = '/no_image.png'

      if (!this.imgErr) {
        imgsrc = this.imgFile
      }
      return imgsrc
    },
  },
  methods: {
    onImgError() {
      this.imgErr = true
      this.$emit('no-image')
    },
  },
}
</script>

<style scoped></style>
