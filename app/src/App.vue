<script module="es2015" lang="ts">
import 'leaflet/dist/leaflet.css'
import Navbar from './components/Navbar.vue'

export default {
  components: {
    Navbar,
  },
}
</script>

<template>
  <Navbar />
  <RouterView />
</template>

<style scoped></style>
