<template>
  <img class="LinaLogo" alt="LinaEE" src="/lina-logo.png" />
</template>

<style>
.LinaLogo {
  height: 180px;
  width: 180px;
  transform: rotateY(560deg);
  animation: turn 3.5s ease-out forwards 1s;
}

@keyframes turn {
  100% {
    transform: rotateY(0deg);
  }
}
</style>
