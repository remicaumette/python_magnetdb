<template>
  <div v-if="!error">
    <div class="flex items-center justify-between mb-6">
      <div class="display-1">
        Records from MagnetDB
      </div>
      <router-link class="btn btn-success" :to="{ name: 'new_record' }">
        New record
      </router-link>
    </div>

    <Card>
      <div class="table-responsive">
        <table>
          <thead class="bg-white">
            <tr>
              <th>Name</th>
              <th>Description</th>
              <th>Created at</th>
            </tr>
          </thead>
          <tbody>
            <tr
                v-for="record in records" :key="record.id" class="cursor-pointer"
                @click="$router.push({ name: 'record', params: { id: record.id } })"
            >
              <td>{{ record.name }}</td>
              <td>
                <template v-if="record.description">{{ record.description }}</template>
                <span v-else class="text-gray-500 italic">Not available</span>
              </td>
              <td>to do</td>
            </tr>
          </tbody>
        </table>
      </div>
    </Card>
  </div>
</template>

<script>
import * as recordService from '@/services/recordService'
import Card from '@/components/Card'

export default {
  name: 'RecordList',
  components: {
    Card,
  },
  data() {
    return {
      error: null,
      records: [],
    }
  },
  async mounted() {
    recordService.list()
        .then((res) => {
          this.records = res.items
        })
        .catch((error) => {
          this.error = error
        })
  },
}
</script>
