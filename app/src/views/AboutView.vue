<template>
  <div class="flex h-screen flex-col px-10">
    <h1 class="text-4xl mt-5 mb-5">About</h1>
    <p>
      This is an app to help you find apartments in Champaign-Urbana. We noticed that popular apartment search sites
      like
      <a class="text-blue-600 hover:text-blue-800" href="https://www.zillow.com/">Zillow</a>, <a class="text-blue-600 hover:text-blue-800" href="https://www.apartments.com/">apartments.com</a>, and
      <a class="text-blue-600 hover:text-blue-800" href="https://www.rentcollegepads.com/">College Pads</a> don't contain up to date information about apartments
      on campus. Rental agencies do not update their listings on these sites, and the information is often incorrect. We
      wanted to create a site that would allow students to find apartments that are actually available.
    </p>
    <p>
      It is a work in progress, and is not affiliated with any real estate
      agencies. We scrape data from the agency websites daily. Found a bug?
      Submit an issue on  <a class="text-blue-600 hover:text-blue-800" href="https://github.com/uiuc-apartments/uiuc-apartments.com/issues">Github</a>.
    </p>
    <div>
      <h2 class="text-4xl mt-5 mb-5">Contributors</h2>
      <div class="flex flex-col md:flex-row w-full justify-around">
        <div class="rounded shadow px-5 mx-10 flex-grow">
          <img src="@/assets/hassam_pfp.jpeg" alt="avatar"
            class="w-60 h-60 rounded-full mx-auto" />
          <div class="text-center pt-10">
            <h3 class="text-3xl">Hassam</h3>
            <p><a href="https://github.com/heasummmn"><font-awesome-icon icon="fa-brands fa-github" /> Github </a></p>
          </div>
        </div>
        <div class="rounded shadow px-5 mx-10 flex-grow">
          <img src="@/assets/richard_pfp.png" alt="avatar"
            class="w-60 h-60 rounded-full mx-auto" />
          <div class="text-center pt-10">
            <h3 class="text-3xl">Richard</h3>
            <p><a href="https://github.com/richyliu"><font-awesome-icon icon="fa-brands fa-github" /> Github </a></p>
          </div>
        </div>
        <div class="rounded shadow px-5 mx-10 flex-grow">
          <img src="@/assets/pete_pfp.jpeg" alt="avatar"
            class="w-60 h-60 rounded-full mx-auto" />
          <div class="text-center pt-10">
            <h3 class="text-3xl">Pete</h3>
            <p><a href="https://github.com/reteps"><font-awesome-icon icon="fa-brands fa-github" /> Github </a></p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
</style>
