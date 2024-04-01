<template>
  <v-container>
    <v-row no-gutters>
      <v-col cols="12" sm="4" md="4" lg="4" xl="3" xxl="2" class="cool-column">
        <v-row no-gutters style="flex-direction: column;" class="pa-2">
          <v-sheet class="cool-sheet" rounded :elevation="5">
            <SearchPeople :users="allUsers" @selected-users-updated="(x) => selectedUsers = x"/>

            <v-container v-if="!userStore().isLoggedIn || userStore().patches.length < 1" class="px-5">
              <p v-if="!userStore().isLoggedIn" class="helper-text my-10"> Don't see your name here?<br>
                <a @click="openLoginDialog">Login</a> or
                <a @click="openRegisterDialog">register</a> to track your patches.
              </p>
              <p v-else class="helper-text mb-10">You haven't added any patches :(<br /><a @click="openAddPatchDialog">Add some!</a></p>
            </v-container>
          </v-sheet>
        </v-row>
      </v-col>

      <v-col cols="12" sm="8" md="8" lg="8" xl="9" xxl="10" class="cool-column pa-2">
        <v-sheet class="cool-sheet" rounded :elevation="5">
          <LineChart :users="selectedUsers"/>
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import SearchPeople from '@/components/SearchPeople.vue'
import LineChart from '@/components/LineChart.vue'
import { userStore } from '@/stores/user'
import { type Responses } from '@/clients/user.client'
import { EventBus, events } from '@/event-bus'

const selectedUsers = ref<Responses.User[]>([]);

const allUsers = computed(() => {
  return userStore().allUsers
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

<style scoped lang="scss">
.cool-sheet {
  padding: 8px;
  height: 100%;
}

.cool-column {
  display: flex;
  flex-direction: column;
}

.patch {
  margin-top: 60px;
  margin-bottom: 40px;
  filter: drop-shadow(0px 0px 15px red) invert(75%);
}
</style>