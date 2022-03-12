<template>
  <div>
    {{ status | statusName }}
  </div>
</template>

<script>
export default {
  name: 'StatusBadge',
  props: ['status']
}
</script>
