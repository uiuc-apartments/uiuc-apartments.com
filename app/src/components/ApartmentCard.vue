<script lang="ts">
import type { Apartment } from '../types'
export default {
  props: {
    source: {
      type: Object as () => Apartment,
      required: true,
    },
  },
  methods: {
    apartmentHover(apartment: Apartment) {
      this.$parent?.$parent?.$emit('apartment-hover', apartment)
    },
  },
  emits: ['apartment-hover'],
  computed: {
    pricePerPerson(): string {
      // show the price per person rounded to 2 decimal places only if it is not an integer
      let perPerson = this.source.rent / Math.max(1, this.source.bedrooms)
      let rounded = Math.round(perPerson * 100) / 100
      let tolerance = 0.001
      if (rounded - Math.floor(rounded) > tolerance) {
        return rounded.toFixed(2)
      }
      return rounded.toString()
    },
  },
}
</script>
<template>
  <!-- apartment card with bedrooms bathrooms agency, rent, location with link to apartment using tailwind css -->

  <div
    class="my-3 relative flex items-center space-x-3 rounded-lg border border-gray-300 bg-white px-6 py-5 shadow-sm focus-within:ring-2 focus-within:ring-indigo-500 focus-within:ring-offset-2 hover:border-gray-400"
    :key="source.link"
    @mouseover="apartmentHover(source)"
    @mouseleave="apartmentHover({} as Apartment)"
  >
    <div class="min-w-0 flex-1">
      <a
        :href="source.link"
        target="_blank"
        rel="noreferrer noopener"
        class="focus:outline-none"
      >
        <p class="text-sm font-medium text-gray-900">{{ source.address }}</p>
        <div class="truncate text-sm text-gray-500">
          <span class="font-bold text-gray-900">
            <font-awesome-icon icon="dollar-sign" />
            {{ source.rent }} (<font-awesome-icon icon="dollar-sign" />
            {{ pricePerPerson }} / person)
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
