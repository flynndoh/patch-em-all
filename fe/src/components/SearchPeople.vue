<template>
  <v-autocomplete
    clearable
    label="Add People"
    :items="people"
    multiple
    variant="outlined"
    auto-select-first
    prepend-inner-icon="mdi-plus"
  ></v-autocomplete>
</template>

<script setup lang="ts">
defineProps<{
  people: {
    type: Object,
    required: true
  }
}>()
</script>

<style scoped>

</style>