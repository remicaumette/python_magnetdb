<template>
  <div v-if="!error">
    <div class="flex items-center justify-between mb-6">
      <div class="display-1">
        Magnets from MagnetDB
      </div>
      <router-link class="btn btn-success" :to="{ name: 'new_magnet' }">
        New magnet
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
                v-for="magnet in magnets" :key="magnet.id" class="cursor-pointer"
                @click="$router.push({ name: 'magnet', params: { id: magnet.id } })"
            >
              <td>{{ magnet.name }}</td>
              <td>
                <template v-if="magnet.description">{{ magnet.description }}</template>
                <span v-else class="text-gray-500 italic">Not available</span>
              </td>
              <td>{{ magnet.status }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </Card>
  </div>
</template>

<script>
import * as magnetService from '@/services/magnetService'
import Card from '@/components/Card'

export default {
  name: 'MagnetList',
  components: {
    Card,
  },
  data() {
    return {
      error: null,
      magnets: [],
    }
  },
  async mounted() {
    magnetService.list()
        .then((res) => {
          this.magnets = res.items
        })
        .catch((error) => {
          this.error = error
        })
  },
}
</script>
