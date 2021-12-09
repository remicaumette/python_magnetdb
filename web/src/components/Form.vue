<template>
  <form @submit.prevent="submit">
    <Alert v-if="rootError" class="alert alert-danger" :error="rootError" />
    <slot />
  </form>
</template>

<script>
import { cloneDeep, isEqual } from 'lodash'
import Alert from "@/components/Alert";

export default {
  name: 'Form',
  props: ['initialValues'],
  components: {
    Alert,
  },
  data() {
    return {
      loading: false,
      values: cloneDeep(this.initialValues || {}),
      errors: {},
      rootError: null,
      dirty: false,
    }
  },
  reactiveProvide: {
    name: 'form',
    include: ['values', 'errors', 'loading', 'dirty'],
  },
  watch: {
    values: {
      immediate: true,
      deep: true,
      handler() {
        this.computeDirty()
      },
    },
    initialValues: {
      immediate: true,
      deep: true,
      handler() {
        this.computeDirty()
      },
    },
  },
  methods: {
    computeDirty() {
      this.dirty = !isEqual(this.initialValues, this.values)
    },
    async submit() {
      this.errors = await this.validate()
      if (Object.keys(this.errors).length) {
        return
      }

      this.loading = true
      try {
        await this.$listeners.submit(this.values, {
          setErrors(errors) {
            this.errors = errors
          },
          setRootError(rootError) {
            this.rootError = rootError
          },
        })
      } catch (e) {
        // this.errors = errors
      } finally {
        this.loading = false
      }
    },
    async validate() {
      const res = this.$listeners.validate(this.values)
      try {
        await res.validate(this.values, { strict: true, abortEarly: false, recursive: true })
        return {}
      } catch (e) {
        return Object.fromEntries(e.inner.map((error) => [error.path, error.errors]))
      }
    },
  }
}
</script>
