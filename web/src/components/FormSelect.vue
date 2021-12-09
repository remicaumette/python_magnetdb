<template>
  <select
    class="form-select"
    :class="{ 'form-select-error': hasError }"
    :value="value"
    @input="$emit('input', $event)"
  >
    <option v-for="opt in options" :key="opt.value" :value="opt.value">
      {{opt.name}}
    </option>
  </select>
</template>

<script>
export default {
  name: 'FormSelect',
  props: ['hasError', 'options', 'value'],
}
</script>

<style scoped>
.form-select {
  @apply focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md;
}

.form-select:disabled {
  @apply bg-gray-100 cursor-not-allowed;
}

.form-select-error {
  @apply ring-1 border-red-500 ring-red-500 !important;
}
</style>
