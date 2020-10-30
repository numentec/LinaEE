<template>
  <v-container>
    <img :class="logosize" alt="LinaEE" src="/lina-logo.png" />
  </v-container>
</template>

<script>
export default {
  name: 'LinaLogo',
  props: {
    logosize: {
      type: String,
      default: 'smtr',
    },
  },
}
</script>

<style>
.smtr {
  height: 180px;
  width: 180px;
  transform: rotateY(560deg);
  animation: turn 3.5s ease-out forwards 1s;
}

.mdtr {
  height: 250px;
  width: 250px;
  transform: rotateY(560deg);
  animation: turn 3.5s ease-out forwards 1s;
}

.lgtr {
  height: 350px;
  width: 350px;
  transform: rotateY(560deg);
  animation: turn 3.5s ease-out forwards 1s;
}

.xltr {
  height: 450px;
  width: 450px;
  transform: rotateY(560deg);
  animation: turn 3.5s ease-out forwards 1s;
}

@keyframes turn {
  100% {
    transform: rotateY(0deg);
  }
}
</style>
