<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import 'leaflet/dist/leaflet.css'
</script>

<template>
  <v-app>
    <header>
      <!-- header bar with tailwind -->
      <nav class="flex items-center bg-teal-500">
        <div class="flex items-center flex-shrink-0 text-white mr-6">
          <span class="font-semibold text-xl tracking-tight"
            >Apartment Finder</span
          >
        </div>
        <div class="w-full block flex-grow lg:flex lg:items-center lg:w-auto">
          <div class="text-sm lg:flex-grow">
            <RouterLink
              to="/"
              class="block mt-4 lg:inline-block lg:mt-0 text-teal-200 hover:text-white mr-4"
              >Home</RouterLink
            >
            <RouterLink
              to="/about"
              class="block mt-4 lg:inline-block lg:mt-0 text-teal-200 hover:text-white mr-4"
              >About</RouterLink
            >
          </div>
        </div>
      </nav>
    </header>
    <v-main>
      <RouterView />
    </v-main>
  </v-app>
</template>

<style scoped></style>
