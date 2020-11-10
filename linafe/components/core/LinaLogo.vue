<template>
  <client-only>
    <v-container class="ma-0 pa-0">
      <img :class="logosize" alt="LinaEE" src="/lina-logo.png" />
    </v-container>
  </client-only>
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
.xstr {
  height: 150px;
  width: 150px;
  transform: rotateY(560deg);
  animation: turn 3.5s ease-out forwards 1s;
}

.smtr {
  height: 200px;
  width: 200px;
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
