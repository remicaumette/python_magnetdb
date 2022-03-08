<template>
  <div v-if="record">
    <div class="display-1 mb-6">
      Record Definition: {{ record.name }}
    </div>

    <Alert v-if="error" class="alert alert-danger mb-6" :error="error"/>

    <Card class="mb-6">
      <template #header>
        Details
      </template>

      <Form :initial-values="record" @submit="submit" @validate="validate">
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
            label="Site"
            name="site"
            :component="FormSelect"
            :required="true"
            :options="siteOptions"
        />
        <FormField
            label="File"
            name="attachment"
            type="file"
            :required="true"
            :component="FormUpload"
            :default-value="record.attachment"
        />
        <Button type="submit" class="btn btn-primary">
          Save
        </Button>
      </Form>
    </Card>

    <VisualisationCard :recordId="record.id"></VisualisationCard>
  </div>
  <Alert v-else-if="error" class="alert alert-danger" :error="error"/>
</template>

<script>
import * as Yup from "yup";
import * as recordService from '@/services/recordService'
import * as siteService from "@/services/siteService";
import Card from '@/components/Card'
import Form from "@/components/Form";
import FormField from "@/components/FormField";
import FormInput from "@/components/FormInput";
import FormSelect from "@/components/FormSelect";
import FormUpload from "@/components/FormUpload";
import Button from "@/components/Button";
import Alert from "@/components/Alert";
import VisualisationCard from "@/views/records/show/VisualisationCard";

export default {
  name: 'RecordShow',
  components: {
    VisualisationCard,
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
      record: null,
      siteOptions: [],
    }
  },
  methods: {
    submit(values, {setRootError}) {
      // return recordService.create({
      //   name: values.name,
      //   site_id: values.site.value,
      //   attachment: values.attachment,
      // })
      //     .then((record) => {
      //       this.$router.push({ name: 'record', params: { id: record.id } })
      //     })
      //     .catch(setRootError)
    },
    validate() {
      return Yup.object().shape({
        name: Yup.string().required(),
        site: Yup.mixed().required(),
        attachment: Yup.mixed().required(),
      })
    },
  },
  async mounted() {
    const sitesRes = await siteService.list()
    this.siteOptions = sitesRes.items.map(site => ({
      name: site.name,
      value: site.id,
    }))

    try {
      this.record = await recordService.find({id: this.$route.params.id})
    } catch (error) {
      this.error = error
    }
  },
}
</script>
