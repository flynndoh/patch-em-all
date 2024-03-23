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
  people: readonly any[]
}>()
</script>

<style scoped></style>
