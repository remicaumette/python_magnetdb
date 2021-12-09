<template>
  <input
    class="form-input"
    :class="{ 'form-input-error': hasError }"
    @input="$emit('input', $event)"
  />
</template>

<script>
export default {
  name: 'FormInput',
  props: ['hasError'],
}
</script>

<style scoped>
.form-input {
  @apply focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md;
}

.form-input:disabled {
  @apply bg-gray-100 cursor-not-allowed;
}

.form-input-error {
  @apply ring-1 border-red-500 ring-red-500 !important;
}
</style>
