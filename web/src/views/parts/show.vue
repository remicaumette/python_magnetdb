<template>
  <div v-if="part">
    <div class="flex items-center justify-between mb-6">
      <div class="display-1">
        Part Definition: {{ part.name }}
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

      <Form :initial-values="part" @submit="submit" @validate="validate">
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
            :default-value="part.status"
        />
        <FormField
            label="Type"
            name="type"
            type="text"
            :component="FormInput"
            :required="true"
        />
        <FormField
            label="Material"
            name="material"
            :component="FormSelect"
            :required="true"
            :options="materialOptions"
            :default-value="part.material.id"
        />
        <FormField
            label="CAO"
            name="cao"
            type="file"
            :component="FormUpload"
            :required="true"
            :default-value="part.cao"
        />
        <FormField
            label="Geometry"
            name="geometry"
            type="file"
            :component="FormUpload"
            :required="true"
            :default-value="part.geometry"
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
              <th>Name</th>
              <th>Description</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr
                v-for="magnet in part.magnets" :key="magnet.id"
                @click="$router.push({ name: 'magnet', params: { id: magnet.id } })"
                class="cursor-pointer"
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
  <Alert v-else-if="error" class="alert alert-danger" :error="error"/>
</template>

<script>
import * as Yup from 'yup'
import * as partService from '@/services/partService'
import * as materialService from '@/services/materialService'
import Card from '@/components/Card'
import Form from "@/components/Form";
import FormField from "@/components/FormField";
import FormInput from "@/components/FormInput";
import FormSelect from "@/components/FormSelect";
import FormUpload from "@/components/FormUpload";
import Button from "@/components/Button";
import Alert from "@/components/Alert";

export default {
  name: 'PartShow',
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
      part: null,
      materialOptions: [],
    }
  },
  methods: {
    submit(values, {setRootError}) {
      let payload = {
        id: this.part.id,
        name: values.name,
        description: values.description,
        status: values.status.value,
        type: values.type,
        material_id: values.material.value,
      }
      if (values.cao instanceof File) {
        payload.cao = values.cao
      }
      if (values.geometry instanceof File) {
        payload.geometry = values.geometry
      }

      return partService.update(payload)
          .then(this.fetch)
          .catch(setRootError)
    },
    validate() {
      return Yup.object().shape({
        name: Yup.string().required(),
        status: Yup.object().required(),
        type: Yup.string().required(),
        material: Yup.object().required(),
      })
    },
    fetch() {
      return partService.find({id: this.$route.params.id})
          .then((part) => {
            this.part = part
          })
          .catch((error) => {
            this.error = error
          })
    },
    destroy() {
      return partService.destroy({id: this.$route.params.id})
          .then(() => {
            this.$router.push({name: 'parts'})
          })
          .catch((error) => {
            this.error = error
          })
    },
  },
  async mounted() {
    const materialsRes = await materialService.list()
    this.materialOptions = materialsRes.items.map(material => ({
      name: material.name,
      value: material.id,
    }))
    await this.fetch()
  },
}
</script>
