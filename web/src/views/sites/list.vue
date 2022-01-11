<template>
  <div v-if="!error">
    <div class="flex items-center justify-between mb-6">
      <div class="display-1">
        Sites from MagnetDB
      </div>
      <router-link class="btn btn-success" :to="{ name: 'new_site' }">
        New site
      </router-link>
    </div>

    <Card>
      <div class="table-responsive">
        <table>
          <thead class="bg-white">
            <tr>
              <th>Name</th>
              <th>Description</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="site in sites.items" :key="site.id" class="cursor-pointer"
              @click="$router.push({ name: 'site', params: { id: site.id } })"
            >
              <td>{{ site.name }}</td>
              <td>
                <template v-if="site.description">{{ site.description }}</template>
                <span v-else class="text-gray-500 italic">Not available</span>
              </td>
              <td>{{ site.status }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </Card>
  </div>
</template>

<script>
import * as siteService from '@/services/siteService'
import Card from '@/components/Card'

export default {
  name: 'SiteList',
  components: {
    Card,
  },
  data() {
    return {
      error: null,
      sites: [],
    }
  },
  async mounted() {
    siteService.list()
      .then((sites) => {
        this.sites = sites
      })
      .catch((error) => {
        this.error = error
      })
  },
}
</script>
