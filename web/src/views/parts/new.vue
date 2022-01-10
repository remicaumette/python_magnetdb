<template>
  <div class="mx-auto w-full max-w-lg">
    <div class="display-1 text-center mb-6">
      New part
    </div>

    <Card>
      <Form @submit="submit" @validate="validate">
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
        />
        <FormField
            label="CAO"
            name="cao"
            type="file"
            :component="FormUpload"
            :required="true"
        />
        <FormField
            label="Geometry"
            name="geometry"
            type="file"
            :component="FormUpload"
            :required="true"
        />
        <Button type="submit" class="btn btn-primary">
          Save
        </Button>
      </Form>
    </Card>
  </div>
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
import Button from "@/components/Button";
import FormUpload from "@/components/FormUpload";

export default {
  name: 'SiteNew',
  components: {
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
      site: null,
      materialOptions: [],
    }
  },
  methods: {
    submit(values, {setRootError}) {
      return partService.create({
        ...values,
        material_id: values.material.value,
        status: values.status.value,
      })
          .then((part) => {
            this.$router.push({ name: 'part', params: { id: part.id } })
          })
          .catch(setRootError)
    },
    validate() {
      return Yup.object().shape({
        name: Yup.string().required(),
        status: Yup.object().required(),
        type: Yup.string().required(),
        material: Yup.object().required(),
        cao: Yup.mixed().required(),
        geometry: Yup.mixed().required(),
      })
    },
  },
  async mounted() {
    const materialsRes = await materialService.list()
    this.materialOptions = materialsRes.items.map(material => ({
      name: material.name,
      value: material.id,
    }))
  },
}
</script>
