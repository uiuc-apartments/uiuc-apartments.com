<script setup lang="ts">
const navigation = [
  { name: 'Home', href: '/' },
  { name: 'About', href: '/about' },
]
</script>

<template>
  <header class="bg-teal-600">
    <nav class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8" aria-label="Top">
      <div
        class="flex w-full items-center justify-between border-b border-indigo-500 py-6 lg:border-none"
      >
        <div class="flex items-center">
          <a href="#">
            <span class="sr-only">Your Company</span>
            <img
              class="h-10 w-auto"
              src="https://tailwindui.com/img/logos/mark.svg?color=white"
              alt=""
            />
            (logo)
          </a>
          <div class="ml-10 hidden space-x-8 lg:block">
            <RouterLink
              v-for="link in navigation"
              :key="link.name"
              :to="link.href"
              class="text-base font-medium text-white hover:text-indigo-50"
            >
              {{ link.name }}
            </RouterLink>
          </div>
        </div>
      </div>
      <div class="flex flex-wrap justify-center space-x-6 py-4 lg:hidden">
        <RouterLink
          v-for="link in navigation"
          :key="link.name"
          :to="link.href"
          class="text-base font-medium text-white hover:text-indigo-50"
        >
          {{ link.name }}
        </RouterLink>
      </div>
    </nav>
  </header>
</template>

<style scoped></style>
