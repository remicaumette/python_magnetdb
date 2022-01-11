<template>
  <div v-if="!error">
    <div class="flex items-center justify-between mb-6">
      <div class="display-1">
        Parts from MagnetDB
      </div>
      <router-link class="btn btn-success" :to="{ name: 'new_part' }">
        New part
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
                v-for="part in parts" :key="part.id" class="cursor-pointer"
                @click="$router.push({ name: 'part', params: { id: part.id } })"
            >
              <td>{{ part.name }}</td>
              <td>
                <template v-if="part.description">{{ part.description }}</template>
                <span v-else class="text-gray-500 italic">Not available</span>
              </td>
              <td>{{ part.status }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </Card>
  </div>
</template>

<script>
import * as partService from '@/services/partService'
import Card from '@/components/Card'

export default {
  name: 'PartList',
  components: {
    Card,
  },
  data() {
    return {
      error: null,
      parts: [],
    }
  },
  async mounted() {
    partService.list()
        .then((res) => {
          this.parts = res.items
        })
        .catch((error) => {
          this.error = error
        })
  },
}
</script>
