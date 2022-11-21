<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <div class="display-1">
        Your servers
      </div>
      <router-link class="btn btn-success" :to="{ name: 'new_server' }">
        New server
      </router-link>
    </div>

    <Card>
      <DataTable :headers="headers" @fetch="fetch" config-persistence-key="server-list">
        <template v-slot:item.name="{ item }">
          {{ item.name }}
        </template>
        <template v-slot:item.username="{ item }">
          {{ item.username }}
        </template>
        <template v-slot:item.public_key="{ item }">
          <button class="link" @click="copy(item.public_key)">
            Click to copy
          </button>
        </template>
        <template v-slot:item.created_at="{ item }">
          {{ item.created_at | datetime }}
        </template>
        <template v-slot:item.updated_at="{ item }">
          {{ item.updated_at | datetime }}
        </template>
      </DataTable>
    </Card>
  </div>
</template>

<script>
import * as serverService from '@/services/serverService'
import Card from '@/components/Card'
import DataTable from "@/components/DataTable";

export default {
  name: 'ServerList',
  components: {
    Card,
    DataTable,
  },
  data() {
    return {
      headers: [
        {
          key: 'name',
          name: 'Name',
          default: true,
          sortable: true,
        },
        {
          key: 'host',
          name: 'Host',
          default: true,
        },
        {
          key: 'username',
          name: 'SSH username',
          default: true,
        },
        {
          key: 'image_directory',
          name: 'Image directory',
          default: true,
        },
        {
          key: 'public_key',
          name: 'SSH public key',
          default: true,
        },
        {
          key: 'created_at',
          name: 'Created At',
          default: true,
          sortable: true,
        },
        {
          key: 'updated_at',
          name: 'Updated At',
          sortable: true,
        },
      ]
    }
  },
  methods: {
    fetch({ query, page, perPage, sortBy, sortDesc }) {
      return serverService.list({ query, page, perPage, sortBy, sortDesc }).then((res) => ({
        currentPage: res.current_page,
        lastPage: res.last_page,
        items: res.items,
        perPage,
        query,
        sortBy,
        sortDesc,
      }))
    },
    copy(value) {
      navigator.clipboard.writeText(value)
    },
  },
}
</script>
