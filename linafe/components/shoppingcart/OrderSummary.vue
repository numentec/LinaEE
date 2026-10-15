<template>
  <v-card :outlined="outlined" :tile="outlined" class="mx-auto">
    <v-toolbar dense flat rounded>
      <v-card-title>Order Summary</v-card-title>
    </v-toolbar>
    <v-divider></v-divider>
    <v-card-text>
      <!-- Cliente -->
      <div class="d-flex align-start">
        <v-avatar color="primary lighten-2" class="mr-4">
          <v-icon large dark> mdi-account </v-icon>
        </v-avatar>
        <div class="customer-info">
          <div class="text-subtitle-1 font-weight-bold text--primary">
            {{ curOrder.customer_name || 'Customer' }}
          </div>
          <div v-if="curOrder.customer_email" class="d-flex align-center">
            <v-icon small class="mr-1">mdi-email-outline</v-icon>
            <span class="text-truncate">{{ curOrder.customer_email }}</span>
          </div>
          <div v-if="curOrder.customer_cel" class="d-flex align-center">
            <v-icon small class="mr-1">mdi-phone-outline</v-icon>
            <span>{{ curOrder.customer_cel }}</span>
          </div>
        </div>
      </div>

      <v-divider class="my-3"></v-divider>

      <!-- Fechas -->
      <div class="d-flex justify-space-between align-center mb-1">
        <span>
          <v-icon small class="mr-1">mdi-calendar-plus</v-icon>
          Created
        </span>
        <span class="text--primary">{{ formatDate(curOrder.created_at) }}</span>
      </div>
      <div class="d-flex justify-space-between align-center">
        <span>
          <v-icon small class="mr-1">mdi-calendar-edit</v-icon>
          Last modified
        </span>
        <span class="text--primary">
          {{ formatDateTime(curOrder.modified_at) }}
        </span>
      </div>

      <v-divider class="my-3"></v-divider>

      <!-- Total -->
      <div class="text-center">
        <div class="text-overline">Total</div>
        <div class="text-h5 font-weight-bold text--primary">
          {{ formatedPrice }}
        </div>
      </div>
      <v-row dense no-gutters>
        <v-col cols="12">
          <v-row dense justify="center" align="center">
            <v-btn
              v-show="!hideControls && curOrder.status === 'pending'"
              color="green darken-1"
              text
              :loading="loading"
              :disabled="loading"
              @click="$emit('keep-selling')"
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
      default: () => ({}),
    },
    outlined: {
      type: Boolean,
      default: false,
    },
    hideControls: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      loading: false,
    }
  },

  computed: {
    formatedPrice() {
      return Number(this.curOrder.total).toLocaleString('es-US', {
        style: 'currency',
        currency: 'USD',
      })
    },
  },

  methods: {
    formatDate(value) {
      if (!value) return '—'
      return new Date(value).toLocaleDateString()
    },
    formatDateTime(value) {
      if (!value) return '—'
      return new Date(value).toLocaleString([], {
        dateStyle: 'short',
        timeStyle: 'short',
      })
    },
  },
}
</script>

<style scoped>
.customer-info {
  min-width: 0;
}
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
