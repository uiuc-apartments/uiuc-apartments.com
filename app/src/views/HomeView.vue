<script module="es2015" lang="ts">
import ApartmentCard from '../components/ApartmentCard.vue'
import MapCard from '../components/MapCard.vue'
import FilterControls from '../components/FilterControls.vue'
import { onMounted, type Ref } from 'vue'
import VirtualList from 'vue3-virtual-scroll-list'
import { ref } from 'vue'
import type { Apartment, Filter } from '../types'
import leaflet from 'leaflet'

function dateIsBetween(date: Date, start: Date, end: Date) {
  // create new date without the time component
  const d = new Date(date.getFullYear(), date.getMonth(), date.getDate())
  const s = new Date(start.getFullYear(), start.getMonth(), start.getDate())
  const e = new Date(end.getFullYear(), end.getMonth(), end.getDate())
  return d >= s && d <= e
}

function getData() {
  return fetch(import.meta.env.VITE_DATA_ENDPOINT_URL).then(response => response.json()).then((document: any) => {
    localStorage.last_stored = document.updateTime;
    return Object.entries(document.fields).map(([id, value]) => {
      var elem = JSON.parse(value.stringValue)
      elem['id'] = id
      return elem
    })
  })
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
    boundedFilteredApartments(): Apartment[] {
      return this.filteredApartments.filter((apartment: Apartment) => {
        return (
          apartment.latitude >= this.bounds.getSouthWest().lat &&
          apartment.latitude <= this.bounds.getNorthEast().lat &&
          apartment.longitude >= this.bounds.getSouthWest().lng &&
          apartment.longitude <= this.bounds.getNorthEast().lng
        )
      })
    },
  },
  setup() {
    const allApartments: Ref<Array<Apartment>> = ref([])
    const filteredApartments: Ref<Array<Apartment>> = ref([])
    const boundedFilteredApartments: Ref<Array<Apartment>> = ref([])
    const loading = ref(true)
    const error = ref(null)
    const apartmentCard = ApartmentCard
    const bounds: Ref<leaflet.LatLngBounds> = ref(leaflet.latLngBounds(new leaflet.LatLng(0, 0), new leaflet.LatLng(0, 0)))
    onMounted(async () => {
      
        if(localStorage.data && localStorage.last_stored) {
          const day = 1000 * 60 * 60 * 24;
          const day_ago = Date.now() - day;
          if(new Date(localStorage.last_stored) < day_ago) {
            getData().then(data => {
              localStorage.data = JSON.stringify(data);
              allApartments.value = data
              filteredApartments.value = data.sort((a: Apartment, b: Apartment) => {
                const perPersonA = a.rent / Math.max(1, a.bedrooms)
                const perPersonB = b.rent / Math.max(1, b.bedrooms)
                return perPersonA - perPersonB
              })
            })
          } else {
            allApartments.value = JSON.parse(localStorage.data)
            filteredApartments.value = allApartments.value.sort((a: Apartment, b: Apartment) => {
              const perPersonA = a.rent / Math.max(1, a.bedrooms)
              const perPersonB = b.rent / Math.max(1, b.bedrooms)
              return perPersonA - perPersonB
            })
          }
        } else {
          getData().then(data => {
            localStorage.data = JSON.stringify(data);
            allApartments.value = data
            filteredApartments.value = data.sort((a: Apartment, b: Apartment) => {
              const perPersonA = a.rent / Math.max(1, a.bedrooms)
              const perPersonB = b.rent / Math.max(1, b.bedrooms)
              return perPersonA - perPersonB
            })
          })
        }
        
      // } catch (err: any) {
      //   error.value = err.message
      // } finally {
      //   loading.value = false
      // }
    })

    return {
      apartmentCard,
      allApartments,
      filteredApartments,
      bounds,
      loading,
      error,
    }
  },
  methods: {
    filterApartments(filter: Filter) {
      // console.log('received event', filter)
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
                new Date(apartment.available_date.replace(' 00:00:00 GMT', '') + 'GMT-0500'),
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
        <MapCard v-model:bounds="bounds" :apartments="filteredApartments" />
      </div>
      <div class="col-span-1 mx-4">
        <VirtualList
          style="height: 75vh; overflow-y: auto"
          :data-key="'id'"
          :data-sources="boundedFilteredApartments"
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
