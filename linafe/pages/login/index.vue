<template>
  <v-container class="d-flex justify-space-around">
    <v-row>
      <v-col
        cols="12"
        sm="6"
        :class="{
          'text-center': $vuetify.breakpoint.smAndDown,
          'd-flex flex-column justify-center': $vuetify.breakpoint.mdAndUp,
        }"
      >
        <!-- <img
          :class="{
            smtr: $vuetify.breakpoint.smAndDown,
            xltr: $vuetify.breakpoint.mdAndUp,
          }"
          alt="LinaEE"
          src="/lina-logo.png"
        /> -->
        <!-- <LinaLogo :logosize="$vuetify.breakpoint.mdAndUp ? 'xltr' : 'smtr'" /> -->
        <LinaLogo :logosize="is_screen_small ? 'smtr' : 'xltr'" />
      </v-col>
      <v-col cols="12" sm="6" class="text-center">
        <UserLogin />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { authComputed } from '~/store/core.js'

export default {
  layout: 'login',
  components: {
    UserLogin: () => import('~/components/core/UserLogin.vue'),
    LinaLogo: () => import('~/components/core/LinaLogo.vue'),
  },
  computed: {
    is_screen_small() {
      return this.$vuetify.breakpoint.smAndDown
    },
    ...authComputed,
  },
}
</script>

<style></style>
