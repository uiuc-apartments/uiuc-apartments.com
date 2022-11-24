<script module="es2015" lang="ts">
import ApartmentCard from '../components/ApartmentCard.vue'
import MapCard from '../components/MapCard.vue'
import FilterControls from '../components/FilterControls.vue'
import { onMounted, type Ref } from 'vue'
import VirtualList from 'vue3-virtual-scroll-list'
import { ref } from 'vue'
import type { Apartment, Filter } from '../types'

function dateIsBetween(date: Date, start: Date, end: Date) {
  // create new date without the time component
  const d = new Date(date.getFullYear(), date.getMonth(), date.getDate())
  const s = new Date(start.getFullYear(), start.getMonth(), start.getDate())
  const e = new Date(end.getFullYear(), end.getMonth(), end.getDate())
  return d >= s && d <= e
}

export default {
  components: {
    ApartmentCard,
    FilterControls,
    MapCard,
    VirtualList,
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
    const apartmentCard = ApartmentCard

    onMounted(async () => {
      try {
        const response = await fetch(import.meta.env.VITE_DATA_ENDPOINT_URL)
        const document = await response.json()
        const data = Object.entries(document.fields).map(([id, value]) => {
          var elem = JSON.parse(value.stringValue)
          elem['id'] = id
          return elem
        });
        allApartments.value = data
        filteredApartments.value = data.sort((a: Apartment, b: Apartment) => {
          const perPersonA = a.rent / Math.max(1, a.bedrooms)
          const perPersonB = b.rent / Math.max(1, b.bedrooms)
          return perPersonA - perPersonB
        })
      } catch (err: any) {
        error.value = err.message
      } finally {
        loading.value = false
      }
    })

    return {
      apartmentCard,
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
            apartment.rent / Math.max(1, apartment.bedrooms) >=
              filter.minRent &&
            apartment.rent / Math.max(1, apartment.bedrooms) <=
              filter.maxRent &&
            (filter.selectedAgencies.length == 0 ||
              filter.selectedAgencies.includes(apartment.agency))
          )
        })
        .filter((apartment) => {
          return typeof apartment.available_date === 'string' &&
            filter.dateRange?.length == 2
            ? dateIsBetween(
                // remove timezone from date
                new Date(apartment.available_date.replace(' 00:00:00 GMT', '')),
                filter.dateRange[0],
                filter.dateRange[1]
              )
            : true
        })
        .sort((a, b) => {
          const perPersonA = a.rent / Math.max(1, a.bedrooms)
          const perPersonB = b.rent / Math.max(1, b.bedrooms)
          return perPersonA - perPersonB
        })
    },
  },
}
</script>

<template>
  <main>
    <h1 class="my-8 text-4xl font-bold text-center">UIUC Apartments</h1>
    <div class="md:grid md:grid-cols-2 lg:grid-cols-4 mt-4">
      <div class="col-span-1 mx-4">
        <FilterControls
          :agencies="agencies"
          @filter-apartments="filterApartments"
        />
      </div>
      <div class="col-span-2 m-4">
        <MapCard :apartments="filteredApartments" />
      </div>
      <div class="col-span-1 mx-4">
        <VirtualList
          style="height: 75vh; overflow-y: auto"
          :data-key="'id'"
          :data-sources="filteredApartments"
          :data-component="apartmentCard"
        />
        <!-- <ApartmentCard
          v-for="apartment in filteredApartments"
          :key="apartment.id"
          :apartment="apartment"
        /> -->
      </div>
    </div>
  </main>
</template>
