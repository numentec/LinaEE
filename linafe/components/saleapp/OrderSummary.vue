<template>
  <v-card :outlined="outlined" :tile="outlined" class="mx-auto">
    <v-toolbar dense flat rounded>
      <v-card-title>Order Summary</v-card-title>
      <v-spacer />
      <v-btn
        v-if="!hideControls"
        icon
        @click.stop="$emit('resend-mail', curOrder)"
      >
        <v-icon>mdi-share-variant-outline</v-icon>
      </v-btn>
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

      <template
        v-if="curOrder.name || curOrder.delivery_to || curOrder.carrier_tag"
      >
        <v-divider class="my-3"></v-divider>

        <!-- Detalles de la orden -->
        <div v-if="curOrder.name" class="d-flex align-start mb-1">
          <v-icon small class="mr-1">mdi-tag-outline</v-icon>
          <span class="mr-2">Order name</span>
          <v-spacer />
          <span class="text--primary text-right">{{ curOrder.name }}</span>
        </div>
        <div v-if="curOrder.delivery_to" class="d-flex align-start mb-1">
          <v-icon small class="mr-1">mdi-map-marker-outline</v-icon>
          <span class="mr-2">Delivery To</span>
          <v-spacer />
          <span class="text--primary text-right">
            {{ curOrder.delivery_to }}
          </span>
        </div>
        <div v-if="curOrder.carrier_tag" class="d-flex align-start">
          <v-icon small class="mr-1">mdi-truck-outline</v-icon>
          <span class="mr-2">Carrier Tag</span>
          <v-spacer />
          <span class="text--primary text-right">
            {{ curOrder.carrier_tag }}
          </span>
        </div>
      </template>

      <v-divider class="my-3"></v-divider>

      <!-- Fechas (en la vista pública solo la fecha de modificación) -->
      <div
        v-if="!publicView"
        class="d-flex justify-space-between align-center mb-1"
      >
        <span>
          <v-icon small class="mr-1">mdi-calendar-plus</v-icon>
          Created
        </span>
        <span class="text--primary">{{ formatDate(curOrder.created_at) }}</span>
      </div>
      <div class="d-flex justify-space-between align-center">
        <span>
          <v-icon small class="mr-1">
            {{ publicView ? 'mdi-calendar' : 'mdi-calendar-edit' }}
          </v-icon>
          {{ publicView ? 'Date' : 'Last modified' }}
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
            <v-btn
              v-show="!hideControls && curOrder.status !== 'pending'"
              color="primary"
              text
              @click="$emit('clone-order')"
            >
              <v-icon left small>mdi-content-copy</v-icon>
              Clone order
            </v-btn>
          </v-row>
        </v-col>
      </v-row>

      <!-- Vendedor (vista pública): datos de contacto en un globo -->
      <template v-if="publicView && seller">
        <v-divider class="my-3"></v-divider>
        <div class="d-flex justify-space-between align-center">
          <span>
            <v-icon small class="mr-1">mdi-account-tie-outline</v-icon>
            Seller
          </span>
          <v-menu
            v-model="sellerMenu"
            :close-on-content-click="false"
            offset-y
            left
            max-width="320"
          >
            <template v-slot:activator="{ on, attrs }">
              <span class="seller-name text--primary" v-bind="attrs" v-on="on">
                {{ seller.name }}
                <v-icon small color="primary" class="ml-1">
                  mdi-information-outline
                </v-icon>
              </span>
            </template>
            <v-card>
              <v-list dense>
                <v-subheader>{{ seller.name }}</v-subheader>
                <v-list-item v-for="row in sellerContacts" :key="row.key">
                  <v-list-item-icon class="mr-3">
                    <v-icon small>{{ row.icon }}</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>{{ row.value }}</v-list-item-title>
                  </v-list-item-content>
                  <v-list-item-action>
                    <v-btn
                      icon
                      small
                      :title="`Copy ${row.label}`"
                      @click="copy(row)"
                    >
                      <v-icon small>
                        {{
                          copied === row.key ? 'mdi-check' : 'mdi-content-copy'
                        }}
                      </v-icon>
                    </v-btn>
                  </v-list-item-action>
                </v-list-item>
                <v-list-item v-if="!sellerContacts.length">
                  <v-list-item-content class="text--secondary">
                    No contact information available.
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-card>
          </v-menu>
        </div>
      </template>
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
    // Vista pública (enlace compartido): solo fecha de modificación y contacto del vendedor
    publicView: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      loading: false,
      sellerMenu: false,
      copied: '',
    }
  },

  computed: {
    seller() {
      return this.curOrder.seller || null
    },
    sellerContacts() {
      if (!this.seller) return []
      return [
        {
          key: 'email',
          label: 'email',
          icon: 'mdi-email-outline',
          value: this.seller.email,
        },
        {
          key: 'phone',
          label: 'phone',
          icon: 'mdi-phone-outline',
          value: this.seller.phone,
        },
      ].filter((row) => row.value)
    },
    formatedPrice() {
      return Number(this.curOrder.total).toLocaleString('es-US', {
        style: 'currency',
        currency: 'USD',
      })
    },
  },

  methods: {
    async copy(row) {
      try {
        await navigator.clipboard.writeText(row.value)
        this.copied = row.key
        setTimeout(() => {
          if (this.copied === row.key) this.copied = ''
        }, 1500)
        this.$emit('copied', row.label)
      } catch (error) {
        this.$emit('copy-error', row.label)
      }
    },
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
.seller-name {
  cursor: pointer;
  display: inline-flex;
  align-items: center;
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
