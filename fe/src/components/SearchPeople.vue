<template>
  <v-container class="pb-0">
    <h3>SEARCH</h3>
    <v-divider class="mt-2 mb-7" />
    <v-autocomplete
      label="Add People"
      :items="users"
      item-title="email"
      item-value="id"
      :custom-filter="filterUsers"
      variant="outlined"
      auto-select-first
      prepend-inner-icon="mdi-plus"
      color="happy"
      v-model="selectedUsers"
      return-object
      chips
      closable-chips
      multiple
    >
      <template v-slot:chip="{ props, item }">
        <v-chip
          v-bind="props"
          :text="[item.raw.first_name, item.raw.last_name].join(' ')"
          color="happy"
        ></v-chip>
      </template>
      <template v-slot:item="{ props, item }">
        <v-list-item
          v-bind="props"
          v-on="props"
          :title="[item.raw.first_name, item.raw.last_name].join(' ')"
          :subtitle="item.raw.email"
        />
      </template>
    </v-autocomplete>
  </v-container>
</template>

<script setup lang="ts">
import { type Responses } from '@/clients/user.client'
import { onMounted, ref, watch } from 'vue'
import { userStore } from '@/stores/user'

const emit = defineEmits(['selected-users-updated'])
defineProps<{
  users: readonly Responses.User[]
}>()

const selectedUsers = ref([])
watch(selectedUsers, () => emit('selected-users-updated', selectedUsers.value));

onMounted(() => {
  if (userStore().isLoggedIn) {
    selectedUsers.value = [userStore().userData];
  }
})

function filterUsers(value: string, queryText: string, item: any) {
  return (
    item.raw.email.toLocaleLowerCase().indexOf(queryText.toLocaleLowerCase()) > -1 ||
    item.raw.first_name.toLocaleLowerCase().indexOf(queryText.toLocaleLowerCase()) > -1 ||
    item.raw.last_name.toLocaleLowerCase().indexOf(queryText.toLocaleLowerCase()) > -1
  );
}
</script>

<style scoped></style>
