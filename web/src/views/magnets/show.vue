<template>
  <div v-if="magnet">
    <div class="flex items-center justify-between mb-6">
      <div class="display-1">
        Magnet Definition: {{ magnet.name }}
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

      <Form :initial-values="magnet" @submit="submit" @validate="validate">
        <FormField
            label="Name"
            name="name"
            type="text"
            :component="FormInput"
            :required="true"
        />
        <FormField
            label="Description"
            name="description"
            type="text"
            :component="FormInput"
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
            :default-value="magnet.status"
        />
        <FormField
            label="Design Office Reference"
            name="design_office_reference"
            type="text"
            :component="FormInput"
        />
        <FormField
            label="CAO"
            name="cao"
            type="file"
            :component="FormUpload"
            :default-value="magnet.cao"
        />
        <FormField
            label="Geometry"
            name="geometry"
            type="file"
            :component="FormUpload"
            :default-value="magnet.geometry"
        />
        <Button type="submit" class="btn btn-primary">
          Save
        </Button>
      </Form>
    </Card>

    <Card class="mb-6">
      <template #header>
        Related Parts
      </template>

      <div class="table-responsive">
        <table>
          <thead class="bg-white">
            <tr>
              <th>Name</th>
              <th>Description</th>
              <th>Status</th>
              <th>Commissioned At</th>
              <th>Decommissioned At</th>
            </tr>
          </thead>
          <tbody>
            <tr
                v-for="magnetPart in magnet.magnet_parts" :key="magnetPart.id"
                @click="$router.push({ name: 'part', params: { id: magnetPart.part.id } })"
                class="cursor-pointer"
            >
              <td>{{ magnetPart.part.name }}</td>
              <td>
                <template v-if="magnetPart.part.description">{{ magnetPart.part.description }}</template>
                <span v-else class="text-gray-500 italic">Not available</span>
              </td>
              <td>{{ magnetPart.part.status }}</td>
              <td>{{ magnetPart.commissioned_at }}</td>
              <td>{{ magnetPart.decommissioned_at }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </Card>

    <Card class="mb-6">
      <template #header>
        Related Site
      </template>

      <div class="table-responsive">
        <table>
          <thead class="bg-white">
            <tr>
              <th>Name</th>
              <th>Description</th>
              <th>Status</th>
              <th>Commissioned At</th>
              <th>Decommissioned At</th>
            </tr>
          </thead>
          <tbody>
            <tr
                v-for="siteMagnet in magnet.site_magnets" :key="siteMagnet.id"
                @click="$router.push({ name: 'site', params: { id: siteMagnet.site.id } })"
                class="cursor-pointer"
            >
              <td>{{ siteMagnet.site.name }}</td>
              <td>
                <template v-if="siteMagnet.site.description">{{ siteMagnet.site.description }}</template>
                <span v-else class="text-gray-500 italic">Not available</span>
              </td>
              <td>{{ siteMagnet.site.status }}</td>
              <td>{{ siteMagnet.commissioned_at }}</td>
              <td>{{ siteMagnet.decommissioned_at }}</td>
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
import * as magnetService from '@/services/magnetService'
import Card from '@/components/Card'
import Form from "@/components/Form";
import FormField from "@/components/FormField";
import FormInput from "@/components/FormInput";
import FormSelect from "@/components/FormSelect";
import FormUpload from "@/components/FormUpload";
import Button from "@/components/Button";
import Alert from "@/components/Alert";

export default {
  name: 'MagnetShow',
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
      FormUpload,
      error: null,
      magnet: null,
    }
  },
  methods: {
    submit(values, {setRootError}) {
      let payload = {
        id: this.magnet.id,
        name: values.name,
        description: values.description,
        status: values.status.value,
        design_office_reference: values.design_office_reference,
      }
      if (values.cao instanceof File) {
        payload.cao = values.cao
      }
      if (values.geometry instanceof File) {
        payload.geometry = values.geometry
      }

      return magnetService.update(payload)
          .then(this.fetch)
          .catch(setRootError)
    },
    validate() {
      return Yup.object().shape({
        name: Yup.string().required(),
        status: Yup.object().required(),
      })
    },
    fetch() {
      return magnetService.find({id: this.$route.params.id})
          .then((magnet) => {
            this.magnet = magnet
          })
          .catch((error) => {
            this.error = error
          })
    },
    destroy() {
      return magnetService.destroy({id: this.$route.params.id})
          .then(() => {
            this.$router.push({name: 'magnets'})
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
