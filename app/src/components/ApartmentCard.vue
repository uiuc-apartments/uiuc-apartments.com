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

  <div
    class="my-3 relative flex items-center space-x-3 rounded-lg border border-gray-300 bg-white px-6 py-5 shadow-sm focus-within:ring-2 focus-within:ring-indigo-500 focus-within:ring-offset-2 hover:border-gray-400"
  >
    <div class="min-w-0 flex-1">
      <a :href="source.link" target="_blank" rel="noreferrer noopener" class="focus:outline-none">
        <p class="text-sm font-medium text-gray-900">{{ source.address }}</p>
        <div class="truncate text-sm text-gray-500">
          <span class="font-bold text-gray-900">
            <font-awesome-icon icon="dollar-sign" /> {{ source.rent }} / <font-awesome-icon icon="dollar-sign" />  {{ pricePerPerson }}
              
          </span>
          <div v-if="source.is_studio">
            <font-awesome-icon icon="bed" /> Studio
          </div>
          <div v-else>
            <font-awesome-icon icon="bed" /> {{ source.bedrooms }}
            <font-awesome-icon icon="bath" /> {{ source.bathrooms }}
          </div>
          Available: {{ source.available_date }} <br />
          {{ source.agency }}
        </div>
      </a>
    </div>
  </div>
</template>
