<template>
  <v-container>
    <div class="heading mb-2">
      <h3>PATCH COLLECTION</h3>
      <v-btn style="margin-top: -10px" color="#28BD7E" icon="mdi-plus" density="comfortable" @click="clientLoggedIn ? openAddPatchDialog : openLoginDialog"/>
    </div>
    <v-divider class="mb-5" />
    <v-container v-if="clientLoggedIn && myPatches.length > 0" class="pa-0 ma-0">
      <v-virtual-scroll :height="600" :items="myPatches" style="scrollbar-width: thin;">
        <template v-slot:default="{ item }">
          <v-list-item :prepend-avatar="pngProxy(item.image)" :key="item.id" class="px-0 py-2">
            <v-list-item-title>#{{item.patch_number}}<span class="subtext">{{item.flight.timestamp.toLocaleString().replace("T", ", ")}} (UTC)</span></v-list-item-title>
            <v-list-item-subtitle>{{item.flight.name}}</v-list-item-subtitle>
          </v-list-item>
        </template>
      </v-virtual-scroll>
    </v-container>
    <v-container v-else class="px-5">
      <v-img src="../../../patch.svg" class="patch" height="180" contain/>
      <p v-if="!clientLoggedIn" class="helper-text">
        <a @click="openLoginDialog">Login</a> or
        <a @click="openRegisterDialog">register</a> to track your patches.
      </p>
      <p v-else class="helper-text">You haven't added any patches :(<br /><a @click="openAddPatchDialog">Add some!</a></p>
    </v-container>
  </v-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { userStore } from '@/stores/user'
import { EventBus, events } from '@/event-bus'
import { pngProxy } from '@/mixins/cors-proxy'

const clientLoggedIn = computed(() => {
  return userStore().isLoggedIn;
})

const myPatches = computed(() => {
  return userStore().patches;
})

function openLoginDialog() {
  EventBus.emit(events.OPEN_LOGIN_DIALOG)
}

function openRegisterDialog() {
  EventBus.emit(events.OPEN_REGISTER_DIALOG)
}

function openAddPatchDialog() {
  EventBus.emit(events.OPEN_ADD_PATCH_DIALOG)
}
</script>

<style scoped>
.heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.patch {
  margin-top: 50px;
  margin-bottom: 40px;
  filter: drop-shadow(0px 0px 15px red) invert(75%);
}

.subtext {
  font-size: 8pt;
  color: gray;
  margin-left: 8px;
}
</style>
