<template>
  <v-container>
    <v-row no-gutters>
      <v-btn @click="logout" v-if="userStore().isLoggedIn" >Logout</v-btn>
    </v-row>
  </v-container>
</template>


<script setup lang="ts">
import { userStore } from '@/stores/user'
function logout() {
  return userStore().logout();
}

</script>