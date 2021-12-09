<template>
  <div class="mx-auto w-full max-w-lg">
    <div class="display-1 text-center mb-6">
      New site
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
            label="Config file"
            name="conffile"
            type="text"
            :component="FormInput"
            :required="true"
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
  </div>
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
      error: null,
      site: null,
    }
  },
  methods: {
    submit(values, {setRootError}) {
      return siteService.create(values)
          .then((site) => {
            this.$router.push({ name: 'site', params: { id: site.id } })
          })
          .catch(setRootError)
    },
    validate() {
      return Yup.object().shape({
        name: Yup.string().required(),
        status: Yup.string().required(),
        conffile: Yup.string().required(),
      })
    },
  },
}
</script>
