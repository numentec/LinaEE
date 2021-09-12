<template>
  <div class="text-center">
    <v-btn
      fab
      x-small
      class="mr-1"
      color="primary"
      :disabled="!enabledStep.s1"
      @click="clickStep(1)"
    >
      <v-icon v-if="enabledStep.s1 && curStep != 1" dark> mdi-pencil </v-icon>
      <span v-else> 1 </span>
    </v-btn>
    <v-btn
      fab
      x-small
      class="mx-1"
      color="primary"
      :disabled="!enabledStep.s2"
      @click="clickStep(2)"
    >
      <v-icon v-if="enabledStep.s2 && curStep != 2" dark> mdi-pencil </v-icon>
      <span v-else> 2 </span>
    </v-btn>
    <v-btn
      fab
      x-small
      class="mx-1"
      color="primary"
      :disabled="!enabledStep.s3"
      @click="clickStep(3)"
    >
      <v-icon v-if="enabledStep.s3 && curStep != 3" dark> mdi-pencil </v-icon>
      <span v-else> 3 </span>
    </v-btn>
    <v-btn
      fab
      x-small
      class="ml-1"
      color="primary"
      :disabled="!enabledStep.s4"
      @click="clickStep(4)"
    >
      <v-icon v-if="enabledStep.s4 && curStep != 4" dark> mdi-pencil </v-icon>
      <span v-else> 4 </span>
    </v-btn>
  </div>
</template>

<script>
export default {
  name: 'MobileSteps',
  props: {
    enabledStep: {
      type: Object,
      required: true,
      default: () => {
        return { s1: true, s2: false, s3: false, s4: false }
      },
    },
    curStep: {
      type: Number,
      required: true,
      default: 1,
    },
  },
  methods: {
    clickStep(v) {
      this.$emit('clickStep', v)
    },
  },
}
</script>

<style lang="scss" scoped></style>
