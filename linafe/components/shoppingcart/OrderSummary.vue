<template>
  <v-card :outlined="outlined" :tile="outlined" class="mx-auto">
    <v-toolbar dense flat rounded>
      <v-card-title>Order Summary</v-card-title>
    </v-toolbar>
    <v-divider></v-divider>
    <v-card-text>
      <v-row dense no-gutters>
        <v-col cols="12">
          <v-row dense justify="start" align="start" class="ml-4 mb-0">
            <v-col cols="2" align="start">
              <div class="my-0">
                <v-avatar>
                  <v-img
                    src="https://cdn.vuetifyjs.com/images/john.jpg"
                  ></v-img>
                </v-avatar>
              </div>
            </v-col>
            <v-col cols="10" align="start">
              <div class="my-0">
                <strong>{{ curOrder.customer_name }}</strong>
              </div>
              <div class="my-0">
                <p>{{ curOrder.customer_email }}</p>
              </div>
            </v-col>
          </v-row>
          <v-row dense justify="start" align="start" class="ml-4 mb-4 mt-0">
            <v-col cols="2" align="start">
              <div class="my-0">
                <strong>Date:</strong>
              </div>
            </v-col>
            <v-col cols="10" align="start">
              <div class="my-0">
                {{ new Date(curOrder.created_at).toLocaleString() }}
              </div>
            </v-col>
          </v-row>
          <v-row dense justify="center" align="center">
            <h3>Total</h3>
          </v-row>
          <v-row dense justify="center" align="center">
            <h3>
              {{
                `${curOrder.total.toLocaleString('es-US', {
                  style: 'currency',
                  currency: 'USD',
                })}`
              }}
            </h3>
          </v-row>
        </v-col>
      </v-row>
      <v-row dense no-gutteers>
        <v-col cols="12">
          <v-row dense justify="center" align="center">
            <v-btn
              color="green darken-1"
              text
              :loading="loading"
              :disabled="loading"
              @click="$emit('go-to-products')"
            >
              Keep selling
              <template v-slot:loader>
                <span class="custom-loader">
                  <v-icon light>mdi-cached</v-icon>
                </span>
              </template>
            </v-btn>
          </v-row>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: {
    curOrder: {
      type: Object,
      required: true,
    },
    outlined: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      loading: false,
    }
  },
}
</script>

<style scoped>
.custom-loader {
  animation: loader 1s infinite;
  display: flex;
}
@-moz-keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}
@-webkit-keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}
@-o-keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}
@keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
