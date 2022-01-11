<template>
  <div v-if="!error">
    <div class="flex items-center justify-between mb-6">
      <div class="display-1">
        Materials from MagnetDB
      </div>
      <router-link class="btn btn-success" :to="{ name: 'new_material' }">
        New material
      </router-link>
    </div>

    <Card>
      <div class="table-responsive">
        <table>
          <thead class="bg-white">
            <tr>
              <th>Name</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            <tr
                v-for="material in materials" :key="material.id" class="cursor-pointer"
                @click="$router.push({ name: 'material', params: { id: material.id } })"
            >
              <td>{{ material.name }}</td>
              <td>
                <template v-if="material.description">{{ material.description }}</template>
                <span v-else class="text-gray-500 italic">Not available</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </Card>
  </div>
</template>

<script>
import * as materialService from '@/services/materialService'
import Card from '@/components/Card'

export default {
  name: 'MaterialList',
  components: {
    Card,
  },
  data() {
    return {
      error: null,
      materials: [],
    }
  },
  async mounted() {
    materialService.list()
        .then((res) => {
          this.materials = res.items
        })
        .catch((error) => {
          this.error = error
        })
  },
}
</script>
