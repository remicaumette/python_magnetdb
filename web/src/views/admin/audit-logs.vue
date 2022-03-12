<template>
  <div>
    <div class="display-1 mb-6">
      Audit Logs
    </div>

    <Card>
      <DataTable :headers="headers" @fetch="fetch">
        <template v-slot:item.date="{ item }">
          {{ item.created_at | datetime }}
        </template>
        <template v-slot:item.message="{ item }">
          {{ item.message }}
        </template>
        <template v-slot:item.resource="{ item }">
          <span v-if="item.resource_name">{{ item.resource_name }}</span>
          <span v-else class="italic">Unknown</span>
          <span v-if="item.resource_id" class="text-gray-500">
            ({{ item.resource_type }}_{{ item.resource_id }})
          </span>
        </template>
        <template v-slot:item.user="{ item }">
          <template v-if="item.user">
            {{ item.user.name }} <span class="text-gray-500">({{ item.user.username }})</span>
          </template>
          <span v-else class="italic">Unavailable</span>
        </template>
      </DataTable>
    </Card>
  </div>
</template>

<script>
import * as auditLogService from '@/services/admin/auditLogService'
import Card from '@/components/Card'
import Alert from "@/components/Alert";
import DataTable from "@/components/DataTable";

export default {
  name: 'AuditLogs',
  components: {
    DataTable,
    Alert,
    Card,
  },
  data() {
    return {
      headers: [
        {
          key: 'date',
          name: 'Date',
          default: true,
        },
        {
          key: 'message',
          name: 'Message',
          default: true,
        },
        {
          key: 'user',
          name: 'User',
        },
        {
          key: 'resource',
          name: 'Resource',
        },
      ]
    }
  },
  methods: {
    fetch({ page, perPage }) {
      return auditLogService.list({ page, perPage }).then((res) => ({
        currentPage: res.current_page,
        lastPage: res.last_page,
        items: res.items,
        perPage,
      }))
    },
  },
}
</script>
