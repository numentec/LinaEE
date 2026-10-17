<template>
  <v-row v-if="!isVertical" no-gutters justify="space-between">
    <v-col v-if="isVertical" class="d-flex flex-column justify-space-between">
      <div class="text-center">
        <v-dialog v-model="dialog" max-width="500px">
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              large
              icon
              color="green lighten-1"
              :disabled="isLoading"
              v-bind="attrs"
              v-on="on"
              @click="openDialog"
            >
              <v-icon large>mdi-pencil-box-outline</v-icon>
            </v-btn>
          </template>
          <v-card>
            <v-card-title class="headline">{{ item.name }}</v-card-title>
            <v-card-subtitle>{{ item.description }}</v-card-subtitle>
            <v-card-text>
              <v-row>
                <v-col cols="12">
                  <v-text-field
                    v-model="itemQuantity"
                    label="Cantidad"
                    type="number"
                    placeholder="1"
                    class="centered-input"
                    prepend-icon="mdi-minus"
                    append-icon="mdi-plus"
                    @click:prepend="$emit('decreaseItemQuantity')"
                    @click:append="$emit('increaseItemQuantity')"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="itemPrice"
                    label="Precio"
                    class="centered-input"
                    prefix="$"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="green darken-1" text @click.stop="updateItem">
                Update
              </v-btn>
            </v-card-actions>
            <v-btn
              icon
              class="ma-2"
              style="position: absolute; top: 0; right: 0"
              @click="closeDialog"
            >
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-card>
        </v-dialog>
      </div>
      <h3 class="text-center">
        {{
          `${itemSubTotal.toLocaleString('es-US', {
            style: 'currency',
            currency: 'USD',
          })}`
        }}
      </h3>
      <div class="text-center">
        <v-btn
          large
          icon
          color="red lighten-1"
          :disabled="isLoading"
          @click="removeItemID(item.id)"
        >
          <v-icon large>{{ delIcon }}</v-icon>
        </v-btn>
      </div>
    </v-col>
  </v-row>
</template>

<script>
export default {}
</script>

<style lang="scss" scoped></style>
