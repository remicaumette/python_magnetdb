import { get, set } from 'lodash'

export function createFormField() {
  return {
    inject: ['form'],
    methods: {
      onInput(event) {
        this.setValue(this.fieldName, event.target.value)
      },
      setValue(name, value) {
        set(this.form.values, name, value)
      },
    },
    computed: {
      fieldName() {
        return this.$props.name
      },
      value() {
        return get(this.form.values, this.fieldName)
      },
      errors() {
        return get(this.form.errors, this.fieldName) || []
      }
    }
  }
}
