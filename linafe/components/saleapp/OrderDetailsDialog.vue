<template>
  <v-dialog :value="value" max-width="450" persistent>
    <v-card>
      <v-card-title>Order details</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="save">
          <v-text-field
            v-model="form.name"
            label="Order name"
            maxlength="100"
            outlined
            dense
          />
          <v-text-field
            v-model="form.delivery_to"
            label="Delivery To"
            maxlength="300"
            outlined
            dense
          />
          <v-text-field
            v-model="form.carrier_tag"
            label="Carrier Tag"
            maxlength="100"
            outlined
            dense
          />
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="$emit('input', false)">Cancel</v-btn>
        <v-btn color="primary" text @click="save">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'OrderDetailsDialog',
  props: {
    value: { type: Boolean, default: false },
  },
  data() {
    return {
      form: { name: '', delivery_to: '', carrier_tag: '' },
    }
  },
  computed: {
    ...mapGetters('saleapp/cart', ['getCartOrderDetails']),
  },
  watch: {
    value(open) {
      if (open) this.form = { ...this.getCartOrderDetails }
    },
  },
  methods: {
    save() {
      this.$store.commit('saleapp/cart/SET_ORDER_DETAILS', this.form)
      this.$emit('input', false)
    },
  },
}
</script>
