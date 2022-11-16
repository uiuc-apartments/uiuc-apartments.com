<script lang="ts">
import type { Apartment } from '../types'
export default {
  props: {
    apartment: {
      type: Object as () => Apartment,
      required: true,
    },
  },
  computed: {
    pricePerPerson(): number {
      return this.apartment.rent / this.apartment.bedrooms
    },
  },
}
</script>
<template>
  <!-- apartment card with bedrooms bathrooms agency, rent, location with link to apartment using tailwind css -->
  <div class="rounded bg-teal-400 m-5 p-5">
    <div>
      <font-awesome-icon icon="sign-hanging" /> {{ apartment.agency }}
      <font-awesome-icon icon="location-pin" /> {{ apartment.address }}
    </div>
    <div>
      <div v-if="apartment.is_studio">
        <font-awesome-icon icon="bed" /> Studio
      </div>
      <div v-else>
        <font-awesome-icon icon="bed" /> {{ apartment.bedrooms }}
        <font-awesome-icon icon="bath" /> {{ apartment.bathrooms }}
      </div>
      <font-awesome-icon icon="dollar-sign" /> {{ apartment.rent }}
      {{ apartment.available_date }}
    </div>
  </div>
</template>
