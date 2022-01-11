<template>
  <div v-if="!error">
    <div class="display-1 mb-6">
      Welcome to MagnetDB
    </div>

    <Card>
      <template #header>Introduction</template>
      <p>This is a demonstrator for MagnetDB. You can list, view, update and create objects by selecting appropriate object in the menu.</p>
      <p>An API also exists. To view the API docs and eventually test it, select the corresponding entry in the menubar.</p>
    </Card>
  </div>
</template>

<script>
import * as siteService from '@/services/siteService'
import Card from '@/components/Card'

export default {
  name: 'Root',
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
