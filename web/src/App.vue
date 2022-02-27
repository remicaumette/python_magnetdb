<template>
  <div id="app" class="mb-16">
    <div class="topbar">
      <div class="container-center">
        <div class="topbar-left">
          <router-link class="topbar-title" :to="{ name: 'root' }">
            MagnetDB
          </router-link>
          <div v-if="$store.getters.isLogged" class="topbar-link-list">
            <router-link class="topbar-link" active-class="topbar-link-active" :to="{ name: 'sites' }">
              Sites
            </router-link>
            <router-link class="topbar-link" active-class="topbar-link-active" :to="{ name: 'magnets' }">
              Magnets
            </router-link>
            <router-link class="topbar-link" active-class="topbar-link-active" :to="{ name: 'parts' }">
              Parts
            </router-link>
            <router-link class="topbar-link" active-class="topbar-link-active" :to="{ name: 'materials' }">
              Materials
            </router-link>
          </div>
        </div>
        <div class="topbar-right">

        </div>
      </div>
    </div>

    <div class="container-center">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  components: {
  }
}
</script>

<style scoped>
.topbar {
  @apply bg-white shadow-md mb-10;
}

.topbar > .container-center {
  @apply flex items-center justify-between;
}

.topbar-title,
.topbar-link {
  @apply h-16 flex items-center;
}

.topbar-title {
  @apply text-xl font-semibold text-blue-700 mr-8;
}

.topbar-left {
  @apply flex items-center;
}

.topbar-link-list {
  @apply flex items-center;
}

.topbar-link {
  @apply px-4 text-gray-700 font-medium;
}

.topbar-link-active {
  @apply bg-gray-100;
}
</style>
