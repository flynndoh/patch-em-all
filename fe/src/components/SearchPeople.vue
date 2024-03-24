<template>
  <v-container>
    <h3>SEARCH</h3>
    <v-divider class="mt-2 mb-5" />
    <v-autocomplete
      label="Add People"
      :items="people"
      multiple
      variant="outlined"
      auto-select-first
      prepend-inner-icon="mdi-plus"
    ></v-autocomplete>
  </v-container>

</template>

<script setup lang="ts">
defineProps<{
  people: readonly any[]
}>()
</script>

<style scoped></style>
