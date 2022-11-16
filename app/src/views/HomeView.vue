<script module="es2015" lang="ts">
import ApartmentCard from '../components/ApartmentCard.vue'
import Map from '../components/Map.vue'
import { onMounted, type Ref } from 'vue'
import { ref } from 'vue'

// TODO: probably a good idea to move this somewhere else
interface Apartment {
  address: string,
  agency: string,
  available_date: string,
  bathrooms: number,
  bedrooms: number,
  id: number,
  is_studio: boolean,
  link: string,
  rent: number
}

export default {
  data() {
    return {
      apartments: [],
    }
  },
  components: {
    ApartmentCard,
    Map,
  },
  setup() {
    const data: Ref<Array<Apartment>> = ref([])
    const loading = ref(true)
    const error = ref(null)

    onMounted(async () => {
      console.log(import.meta.env)
      try {
        const response = await fetch(import.meta.env.VITE_FUNCTION_URL)
        data.value = await response.json()
      } catch (err: any) {
        error.value = err.message
      } finally {
        loading.value = false
      }
    })

    return {
      data,
      loading,
      error,
    }
  },
}
</script>

<template>
  <main>
    <h1 class="text-4xl font-bold text-center">Apartments</h1>
    <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <ApartmentCard
        v-for="apartment in data"
        :key="apartment.id"
        :apartment="apartment"
      />
    </div>
    <Map/>
  </main>
</template>
