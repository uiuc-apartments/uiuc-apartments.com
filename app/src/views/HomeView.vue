<script module="es2015" lang="ts">
import ApartmentCard from '../components/ApartmentCard.vue'
import { onMounted } from 'vue'
import { ref } from 'vue'

export default {
  data() {
    return {
      apartments: [],
    }
  },
  components: {
    ApartmentCard,
  },
  setup() {
    const data = ref([])
    const loading = ref(true)
    const error = ref(null)

    onMounted(async () => {
      try {
        const response = await fetch('/api/search')
        data.value = await response.json()
      } catch (err) {
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
  </main>
</template>
