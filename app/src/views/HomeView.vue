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

function getData(): Promise<Apartment[]> {
  return fetch(import.meta.env.VITE_DATA_ENDPOINT_URL)
    .then((response) => response.json())
    .then((document: any) => {
      localStorage.last_stored = document.updateTime
      return Object.entries(document.fields).map(([id, value]) => {
        var elem = JSON.parse(value.stringValue)
        elem['id'] = id
        return elem
      })
    })
}

// source: https://stackoverflow.com/a/42532563
function isLatLongInsidePolygon(x: number, y: number, poly) {
  var inside = false
  for (var ii = 0; ii < poly.getLatLngs().length; ii++) {
    var polyPoints = poly.getLatLngs()[ii]
    for (var i = 0, j = polyPoints.length - 1; i < polyPoints.length; j = i++) {
      var xi = polyPoints[i].lat,
        yi = polyPoints[i].lng
      var xj = polyPoints[j].lat,
        yj = polyPoints[j].lng

      var intersect =
        yi > y != yj > y && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi
      if (intersect) inside = !inside
    }
  }

  return inside
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
    shapesFilteredApartments(): Apartment[] {
      return this.allApartments.filter((apartment) => {
        if (this.filterShapes.length === 0) {
          return true
        }
        for (const shape of this.filterShapes) {
          if (shape instanceof L.Polygon) {
            if (
              isLatLongInsidePolygon(
                apartment.latitude,
                apartment.longitude,
                shape
              )
            ) {
              return true
            }
          }
        }
        return false
      })
    },
    filteredApartments(): Apartment[] {
      // console.log('received event', filter)
      return this.shapesFilteredApartments
        .filter((apartment) => {
          return (
            apartment.bedrooms >= this.filter.minBedrooms &&
            apartment.bedrooms <= this.filter.maxBedrooms &&
            apartment.bathrooms >= this.filter.minBathrooms &&
            apartment.bathrooms <= this.filter.maxBathrooms &&
            apartment.rent / Math.max(1, apartment.bedrooms) >=
              this.filter.minRent &&
            apartment.rent / Math.max(1, apartment.bedrooms) <=
              this.filter.maxRent &&
            (this.filter.selectedAgencies.length == 0 ||
              this.filter.selectedAgencies.includes(apartment.agency))
          )
        })
        .filter((apartment) => {
          return typeof apartment.available_date === 'string' &&
            this.filter.dateRange?.length == 2
            ? dateIsBetween(
                // remove timezone from date
                new Date(
                  apartment.available_date.replace(' 00:00:00 GMT', '') +
                    'GMT-0500'
                ),
                this.filter.dateRange[0],
                this.filter.dateRange[1]
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
  setup() {
    const allApartments: Ref<Array<Apartment>> = ref([])
    const selectedApartment: Ref<Apartment> = ref({} as Apartment)
    const loading = ref(true)
    const error = ref(null)
    const apartmentCard = ApartmentCard
    const bounds: Ref<leaflet.LatLngBounds> = ref(
      leaflet.latLngBounds(new leaflet.LatLng(0, 0), new leaflet.LatLng(0, 0))
    )
    const filterShapes: Ref<Array<L.Draw.PolyLine>> = ref([])
    const filter: Ref<Filter> = ref({} as Filter)
    onMounted(async () => {
      if (localStorage.data && localStorage.last_stored) {
        const day = 1000 * 60 * 60 * 24
        const day_ago = Date.now() - day
        if (new Date(localStorage.last_stored) < day_ago) {
          getData().then((data) => {
            localStorage.data = JSON.stringify(data)
            allApartments.value = data
            // filteredApartments.value = data.sort((a: Apartment, b: Apartment) => {
            //   const perPersonA = a.rent / Math.max(1, a.bedrooms)
            //   const perPersonB = b.rent / Math.max(1, b.bedrooms)
            //   return perPersonA - perPersonB
            // })
          })
        } else {
          allApartments.value = JSON.parse(localStorage.data)
          // filteredApartments.value = allApartments.value.sort((a: Apartment, b: Apartment) => {
          //   const perPersonA = a.rent / Math.max(1, a.bedrooms)
          //   const perPersonB = b.rent / Math.max(1, b.bedrooms)
          //   return perPersonA - perPersonB
          // })
        }
      } else {
        getData().then((data) => {
          localStorage.data = JSON.stringify(data)
          allApartments.value = data
          // filteredApartments.value = data.sort((a: Apartment, b: Apartment) => {
          //   const perPersonA = a.rent / Math.max(1, a.bedrooms)
          //   const perPersonB = b.rent / Math.max(1, b.bedrooms)
          //   return perPersonA - perPersonB
          // })
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
      selectedApartment,
      allApartments,
      filter,
      bounds,
      filterShapes,
      loading,
      error,
    }
  },
  methods: {
    onApartmentHover(apartment: Apartment) {
      this.selectedApartment = apartment
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
          v-model:filter-apartments="filter"
        />
      </div>
      <div class="col-span-2 m-4">
        <MapCard
          v-model:bounds="bounds"
          v-model:filter-shapes="filterShapes"
          :apartments="filteredApartments"
          :selectedApartment="selectedApartment"
        />
      </div>
      <div class="col-span-1 mx-4">
        <VirtualList
          style="height: 75vh; overflow-y: auto"
          :data-key="'id'"
          :data-sources="boundedFilteredApartments"
          :data-component="apartmentCard"
          @apartment-hover="onApartmentHover"
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
