<script lang="ts">
import { watch, ref } from 'vue'
import type { Filter } from '../types'

export default {
  props: ['agencies'],
  emits: ['filter-apartments'],

  setup(props: any, context: any) {
    const minBedrooms = ref(1)
    const maxBedrooms = ref(5)
    const minBathrooms = ref(1)
    const maxBathrooms = ref(5)
    const minRent = ref(0)
    const maxRent = ref(10000)
    const selectedAgencies = ref(props.agencies)
    const dateRange = ref([new Date(2023, 7, 1), new Date(2023, 8, 31)])

    const filterApartments = () => {
      const filter: Filter = {
        minBedrooms: minBedrooms.value,
        maxBedrooms: maxBedrooms.value,
        minBathrooms: minBathrooms.value,
        maxBathrooms: maxBathrooms.value,
        minRent: minRent.value,
        maxRent: maxRent.value,
        dateRange: dateRange.value,
        selectedAgencies: selectedAgencies.value,
      }
      console.log('filtering', filter)
      context.emit('filter-apartments', filter)
    }

    watch(
      [
        minBedrooms,
        maxBedrooms,
        minBathrooms,
        maxBathrooms,
        minRent,
        maxRent,
        selectedAgencies,
        dateRange,
      ],
      filterApartments
    )

    return {
      minBedrooms,
      maxBedrooms,
      minBathrooms,
      maxBathrooms,
      dateRange,
      minRent,
      maxRent,
      selectedAgencies,
    }
  },
}
</script>
<template>
  <div>
    <div class="flex" v-for="agency in agencies" :key="agency">
      <input
        type="checkbox"
        :id="agency"
        :value="agency"
        v-model="selectedAgencies"
      />
      <label :for="agency">{{ agency }}</label>
    </div>
    <div class="flex flex-row">
      <!-- min to max bathrooms -->
      <div class="flex flex-col">
        <label for="min-bathrooms">Min Bathrooms</label>
        <input
          type="number"
          id="min-bathrooms"
          v-model="minBathrooms"
          min="1"
          max="10"
        />
      </div>
      <div class="flex flex-col">
        <label for="max-bathrooms">Max Bathrooms</label>
        <input
          type="number"
          id="max-bathrooms"
          v-model="maxBathrooms"
          min="1"
          max="10"
        />
      </div>
    </div>
    <div class="flex flex-row">
      <!-- min to max bedrooms -->
      <div class="flex flex-col">
        <label for="min-bedrooms">Min Bedrooms</label>
        <input
          type="number"
          id="min-bedrooms"
          v-model="minBedrooms"
          min="1"
          max="10"
        />
      </div>
      <div class="flex flex-col">
        <label for="max-bedrooms">Max Bedrooms</label>
        <input
          type="number"
          id="max-bedrooms"
          v-model="maxBedrooms"
          min="1"
          max="10"
        />
      </div>
    </div>
    <div class="flex flex-row">
      <!-- min to max rent -->
      <div class="flex flex-col">
        <label for="min-rent">Min Rent</label>
        <input
          type="number"
          id="min-rent"
          v-model="minRent"
          min="0"
          max="10000"
        />
      </div>
      <div class="flex flex-col">
        <label for="max-rent">Max Rent</label>
        <input
          type="number"
          id="max-rent"
          v-model="maxRent"
          min="0"
          max="10000"
        />
      </div>
    </div>

    <Datepicker v-model="dateRange" range :enableTimePicker="false" />
  </div>
</template>
<style scoped></style>
