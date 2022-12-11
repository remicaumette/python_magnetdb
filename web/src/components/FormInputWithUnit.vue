<template>
  <div class="form-input-with-unit-container">
    <input
        v-bind="$attrs"
        class="form-input"
        :class="{ 'form-input-error': hasError }"
        type="number"
        v-model="displayableValue"
    />
    <select :value="unit.value" @change="changeUnit" class="border-none rounded-r-md">
      <option v-for="opt in unitOptions" :key="opt.value" :value="opt.value">
        {{opt.symbol}}
      </option>
    </select>
  </div>
</template>

<script>
import { unit } from 'mathjs'

window.mathUnit = unit

export default {
  name: 'FormInputWithUnit',
  inheritAttrs: false,
  props: ['value', 'unitOptions', 'hasError'],
  inject: ['form'],
  data() {
    return {
      displayableValue: this.value,
      defaultUnit: null,
      unit: null,
    }
  },
  watch: {
    displayableValue(value) {
      this.$emit('value', unit(value, this.unit.value).to(this.defaultUnit.value).value)
    }
  },
  methods: {
    changeUnit(event) {
      const newUnit = this.unitOptions.find((opt) => opt.value === event.target.value)
      this.displayableValue = String(
          parseFloat(unit(this.displayableValue, this.unit.value).to(newUnit.value).format({ notation: 'fixed' }))
      )
      this.unit = newUnit
    },
  },
  created() {
    this.defaultUnit = this.unitOptions.find((opt) => opt.default)
    this.unit = this.defaultUnit
  },
}
</script>

<style scoped>
.form-input-with-unit-container {
  @apply z-0 relative flex items-center block w-full shadow-sm sm:text-sm border border-gray-300 rounded-md
  focus:ring-blue-500 focus:border-blue-500;
}

.form-input-with-unit-container > .form-input {
  @apply block border-none w-full sm:text-sm rounded-l-md focus:ring-0;
}

.form-input:disabled {
  @apply bg-gray-100 cursor-not-allowed;
}

.form-input-error {
  @apply ring-1 border-red-500 ring-red-500 !important;
}
</style>
