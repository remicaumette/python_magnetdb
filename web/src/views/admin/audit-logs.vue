<template>
  <div>
    <div class="display-1 mb-6">
      Audit Logs
    </div>

    <Card>
      <Alert v-if="error" :error="error" />

      <div class="table-responsive">
        <table>
          <thead class="bg-white">
            <tr>
              <th>Date</th>
              <th>Message</th>
              <th>Resource</th>
              <th>User</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="log in logs" :key="log.id">
              <td>{{ log.created_at | datetime }}</td>
              <td>{{ log.message }}</td>
              <td>
                <span v-if="log.resource_name">{{ log.resource_name }}</span>
                <span v-else class="italic">Unknown</span>
                <span v-if="log.resource_id" class="text-gray-500">
                  ({{log.resource_type}}_{{log.resource_id}})
                </span>
              </td>
              <td>
                <template v-if="log.user">
                  {{ log.user.name }} <span class="text-gray-500">({{log.user.username}})</span>
                </template>
                <span v-else class="italic">Unavailable</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </Card>
  </div>
</template>

<script>
import * as auditLogService from '@/services/admin/auditLogService'
import Card from '@/components/Card'
import Alert from "@/components/Alert";

export default {
  name: 'AuditLogs',
  components: {
    Alert,
    Card,
  },
  data() {
    return {
      error: null,
      logs: [],
    }
  },
  async mounted() {
    auditLogService.list()
      .then((res) => {
        this.logs = res.items
      })
      .catch((error) => {
        this.error = error
      })
  },
}
</script>
