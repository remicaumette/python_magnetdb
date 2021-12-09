<template>
  <div v-if="site">
    <div class="flex items-center justify-between mb-6">
      <div class="display-1">
        Site Definition: {{ site.name }}
      </div>
      <Button class="btn btn-danger" type="button" @click="destroy">
        Supprimer
      </Button>
    </div>

    <Alert v-if="error" class="alert alert-danger mb-6" :error="error"/>

    <Card class="mb-6">
      <template #header>
        Details
      </template>

      <Form :initial-values="site" @submit="submit" @validate="validate">
        <FormField
            label="Name"
            name="name"
            type="text"
            :component="FormInput"
            :required="true"
        />
        <FormField
            label="Config file"
            name="conffile"
            type="text"
            :component="FormInput"
            :required="true"
            :disabled="true"
        />
        <FormField
            label="Status"
            name="status"
            :component="FormSelect"
            :required="true"
            :options="[
            { name: 'Study', value: 'in_study' },
            { name: 'Operation', value: 'in_operation' },
            { name: 'Stock', value: 'in_stock' },
            { name: 'Defunct', value: 'defunct' },
          ]"
        />
        <Button type="submit" class="btn btn-primary">
          Save
        </Button>
      </Form>
    </Card>

    <Card>
      <template #header>
        Related Magnets
      </template>

      <div class="table-responsive">
        <table>
          <thead class="bg-white">
            <tr>
              <th>#</th>
              <th>Name</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="magnet in site.magnets" :key="magnet.id">
              <td>{{ magnet.id }}</td>
              <td>{{ magnet.name }}</td>
              <td>{{ magnet.status }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </Card>
  </div>
  <Alert v-else-if="error" class="alert alert-danger" :error="error"/>
</template>

<script>
import * as Yup from 'yup'
import * as siteService from '@/services/siteService'
import Card from '@/components/Card'
import Form from "@/components/Form";
import FormField from "@/components/FormField";
import FormInput from "@/components/FormInput";
import FormSelect from "@/components/FormSelect";
import Button from "@/components/Button";
import Alert from "@/components/Alert";

export default {
  name: 'SiteShow',
  components: {
    Alert,
    Button,
    FormField,
    Form,
    Card,
  },
  data() {
    return {
      FormInput,
      FormSelect,
      error: null,
      site: null,
    }
  },
  methods: {
    submit(values, {setRootError}) {
      const payload = {
        id: this.site.id,
        name: values.name,
        status: values.status,
      }

      return siteService.update(payload)
          .then(this.fetch)
          .catch(setRootError)
    },
    validate() {
      return Yup.object().shape({
        name: Yup.string().required(),
        status: Yup.string().required(),
      })
    },
    fetch() {
      return siteService.find({id: this.$route.params.id})
          .then((site) => {
            this.site = site
          })
          .catch((error) => {
            this.error = error
          })
    },
    destroy() {
      return siteService.destroy({id: this.$route.params.id})
          .then(() => {
            this.$router.push({ name: 'sites' })
          })
          .catch((error) => {
            this.error = error
          })
    },
  },
  async mounted() {
    await this.fetch()
  },
}
</script>
