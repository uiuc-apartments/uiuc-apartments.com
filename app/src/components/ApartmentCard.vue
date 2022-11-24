<script lang="ts">
import type { Apartment } from '../types'
export default {
  props: {
    source: {
      type: Object as () => Apartment,
      required: true,
    },
  },
  computed: {
    pricePerPerson(): number {
      return this.source.rent / Math.max(1, this.source.bedrooms)
    },
  },
}
</script>
<template>
  <!-- apartment card with bedrooms bathrooms agency, rent, location with link to apartment using tailwind css -->
  <a class="block rounded bg-teal-400 m-5 p-5" :href=source.link>
    <div>
      <font-awesome-icon icon="sign-hanging" /> {{ source.agency }}
      <font-awesome-icon icon="location-pin" /> {{ source.address }}
    </div>
    <div>
      <div v-if="source.is_studio">
        <font-awesome-icon icon="bed" /> Studio
      </div>
      <div v-else>
        <font-awesome-icon icon="bed" /> {{ source.bedrooms }}
        <font-awesome-icon icon="bath" /> {{ source.bathrooms }}
      </div>
      <font-awesome-icon icon="dollar-sign" /> {{ source.rent }} / <font-awesome-icon icon="dollar-sign" /> {{ pricePerPerson }}
      <br>
      {{ source.available_date }}
      <!-- {{ apartment.latitude }}, {{ apartment.longitude }} -->
    </div>
  </a>
</template>
