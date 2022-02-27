<template>
  <div class="mx-auto w-full max-w-sm">
    <div class="display-1 text-center mb-6">
      Sign in to MagnetDB
    </div>

    <Card>
      <Form @submit="submit" @validate="validate">
        <FormField
            label="Username"
            name="username"
            type="text"
            :component="FormInput"
            :required="true"
        />
        <FormField
            label="Password"
            name="password"
            type="password"
            :component="FormInput"
            :required="true"
        />
        <Button type="submit" class="btn btn-primary btn-block">
          Sign In
        </Button>
      </Form>
    </Card>
  </div>
</template>

<script>
import * as Yup from 'yup'
import * as sessionService from '@/services/sessionService'
import Card from '@/components/Card'
import Form from "@/components/Form";
import FormField from "@/components/FormField";
import FormInput from "@/components/FormInput";
import FormUpload from "@/components/FormUpload";
import Button from "@/components/Button";

export default {
  name: 'SignIn',
  components: {
    Button,
    FormField,
    Form,
    Card,
  },
  data() {
    return {
      FormInput,
      FormUpload,
      error: null,
    }
  },
  methods: {
    submit(values, {setRootError}) {
      return sessionService.create(values)
        .then((res) => {
          this.$store.commit('setToken', res.token)
          this.$router.push('/')
        })
        .catch(setRootError)
    },
    validate() {
      return Yup.object().shape({
        username: Yup.string().required(),
        password: Yup.string().required(),
      })
    },
  },
}
</script>
