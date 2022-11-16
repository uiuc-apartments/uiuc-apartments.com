<script module="es2015" lang="ts">
import ApartmentCard from '../components/ApartmentCard.vue'
import MapCard from '../components/MapCard.vue'
import FilterControls from '../components/FilterControls.vue'
import { onMounted, type Ref } from 'vue'
import { ref } from 'vue'
import type { Apartment, Filter } from '../types'

export default {
  components: {
    ApartmentCard,
    FilterControls,
    MapCard,
  },
  computed: {
    agencies(): Array<string> {
      return [
        ...new Set(
          this.allApartments.map((apartment: Apartment) => apartment.agency)
        ),
      ]
    },
  },
  setup() {
    const allApartments: Ref<Array<Apartment>> = ref([])
    const filteredApartments: Ref<Array<Apartment>> = ref([])
    const loading = ref(true)
    const error = ref(null)

    onMounted(async () => {
      console.log(import.meta.env)
      try {
        const response = await fetch(import.meta.env.VITE_FUNCTION_URL)
        allApartments.value = await response.json()
      } catch (err: any) {
        error.value = err.message
      } finally {
        loading.value = false
      }
    })

    return {
      allApartments,
      filteredApartments,
      loading,
      error,
    }
  },
  methods: {
    filterApartments(filter: Filter) {
      console.log('received event', filter)
      this.filteredApartments = this.allApartments
        .filter((apartment) => {
          return (
            apartment.bedrooms >= filter.minBedrooms &&
            apartment.bedrooms <= filter.maxBedrooms &&
            apartment.bathrooms >= filter.minBathrooms &&
            apartment.bathrooms <= filter.maxBathrooms &&
            apartment.rent >= filter.minRent &&
            apartment.rent <= filter.maxRent &&
            filter.selectedAgencies.includes(apartment.agency)
          )
        })
        .filter((apartment) => {
          return filter.dateRange?.length == 2
            ? new Date(apartment.available_date) >= filter.dateRange[0] &&
                new Date(apartment.available_date) <= filter.dateRange[1]
            : true
        })
    },
  },
}
</script>

<template>
  <main>
    <h1 class="text-4xl font-bold text-center">Apartments</h1>
    <div class="grid grid-cols-4 gap-4 mt-4">
      <div class="col-span-1">
        <FilterControls
          :agencies="agencies"
          @filter-apartments="filterApartments"
        />
      </div>
      <div class="col-span-2">
        <MapCard :apartments="filteredApartments" />
      </div>
      <div class="col-span-1">
        <ApartmentCard
          v-for="apartment in filteredApartments"
          :key="apartment.id"
          :apartment="apartment"
        />
      </div>
    </div>
  </main>
</template>
