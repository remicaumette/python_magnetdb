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
            label="Be Ref"
            name="be"
            type="text"
            :component="FormInput"
            :required="true"
        />
        <FormField
            label="Geometry file"
            name="geom"
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

<!--    <Card>-->
<!--      <template #header>-->
<!--        Related Magnets-->
<!--      </template>-->

<!--      <div class="table-responsive">-->
<!--        <table>-->
<!--          <thead class="bg-white">-->
<!--            <tr>-->
<!--              <th>#</th>-->
<!--              <th>Name</th>-->
<!--              <th>Status</th>-->
<!--            </tr>-->
<!--          </thead>-->
<!--          <tbody>-->
<!--            <tr v-for="magnet in site.magnets" :key="magnet.id">-->
<!--              <td>{{ magnet.id }}</td>-->
<!--              <td>{{ magnet.name }}</td>-->
<!--              <td>{{ magnet.status }}</td>-->
<!--            </tr>-->
<!--          </tbody>-->
<!--        </table>-->
<!--      </div>-->
<!--    </Card>-->
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
      error: null,
      magnet: null,
    }
  },
  methods: {
    submit(values, {setRootError}) {
      const payload = {
        id: this.magnet.id,
        name: values.name,
        status: values.status,
      }

      return magnetService.update(payload)
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
