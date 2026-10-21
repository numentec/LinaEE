<template>
  <div>
    <MaterialCard class="mt-10">
      <template v-slot:heading>
        <v-toolbar dense color="secondary" class="mx-1" dark flat>
          <v-spacer />
          <v-toolbar-title>SaleApp settings</v-toolbar-title>
          <v-spacer />
        </v-toolbar>
      </template>
      <v-tabs v-model="tab" color="secondary" class="mt-8">
        <v-tab>
          <v-icon left>mdi-email-outline</v-icon>
          Email
        </v-tab>
      </v-tabs>
      <v-tabs-items v-model="tab">
        <v-tab-item>
          <v-card-text>
            <SaleAppSettingsForm />
          </v-card-text>
        </v-tab-item>
      </v-tabs-items>
    </MaterialCard>
  </div>
</template>

<script>
export default {
  components: {
    MaterialCard: () => import('~/components/core/MaterialCard'),
    SaleAppSettingsForm: () =>
      import('~/components/saleapp/SaleAppSettingsForm'),
  },

  data() {
    return {
      tab: 0,
    }
  },
}
</script>
