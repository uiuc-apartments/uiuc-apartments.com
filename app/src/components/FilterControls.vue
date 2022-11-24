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
      // console.log('filtering', filter)
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
  <div class="bg-gray-100 px-4 py-4">
    <div class="">
      <h2 class="text-xl pb-3">Agencies</h2>
      <fieldset class="pl-2">
        <div
          class="relative flex items-center"
          v-for="agency in agencies"
          :key="agency"
        >
          <div class="flex h-5 items-center">
            <input
              type="checkbox"
              class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
              :id="agency"
              :value="agency"
              v-model="selectedAgencies"
            />
          </div>
          <div class="p-2 ml-3 text-sm">
            <label :for="agency" class="p-2 font-medium text-gray-700">
              {{ agency }}
            </label>
          </div>
        </div>
      </fieldset>
    </div>
    <div class="my-4 flex flex-row space-x-6">
      <!-- min to max bathrooms -->
      <div>
        <label
          for="min-bathrooms"
          class="block text-sm font-medium text-gray-700"
        >
          Min baths
        </label>
        <div class="mt-1">
          <input
            class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            type="number"
            id="min-bathrooms"
            v-model="minBathrooms"
            min="1"
            max="10"
          />
        </div>
      </div>
      <div class="flex flex-col">
        <label
          for="max-bathrooms"
          class="block text-sm font-medium text-gray-700"
        >
          Max baths
        </label>
        <div class="mt-1">
          <input
            class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            type="number"
            id="max-bathrooms"
            v-model="maxBathrooms"
            min="1"
            max="10"
          />
        </div>
      </div>
    </div>
    <div class="my-4 flex flex-row space-x-6">
      <!-- min to max bedrooms -->
      <div>
        <label
          for="min-bedrooms"
          class="block text-sm font-medium text-gray-700"
        >
          Min bedrooms
        </label>
        <div class="mt-1">
          <input
            class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            type="number"
            id="min-bedrooms"
            v-model="minBedrooms"
            min="1"
            max="10000"
          />
        </div>
      </div>
      <div class="flex flex-col">
        <label
          for="max-bedrooms"
          class="block text-sm font-medium text-gray-700"
        >
          Max bedrooms
        </label>
        <div class="mt-1">
          <input
            class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            type="number"
            id="max-bedrooms"
            v-model="maxBedrooms"
            min="1"
            max="10000"
          />
        </div>
      </div>
    </div>
    <div class="my-4 flex flex-row space-x-6">
      <!-- min to max rent -->
      <div>
        <label for="min-rent" class="block text-sm font-medium text-gray-700">
          Min rent
        </label>
        <div class="mt-1">
          <input
            class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            type="number"
            id="min-rent"
            v-model="minRent"
            min="1"
            max="10000"
          />
        </div>
      </div>
      <div class="flex flex-col">
        <label for="max-rent" class="block text-sm font-medium text-gray-700">
          Max rent
        </label>
        <div class="mt-1">
          <input
            class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            type="number"
            id="max-rent"
            v-model="maxRent"
            min="1"
            max="10000"
          />
        </div>
      </div>
    </div>
    <Datepicker v-model="dateRange" range :enableTimePicker="false" />
  </div>
</template>
<style scoped></style>
