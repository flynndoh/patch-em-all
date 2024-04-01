<template>
  <v-container>
    <v-row no-gutters>
      <v-col cols="12" sm="4" md="4" lg="4" xl="3" xxl="2" class="cool-column">
        <v-row no-gutters style="flex-direction: column;" class="pa-2">
          <v-sheet class="cool-sheet" rounded :elevation="5">
            <v-container>
              <div>
                <h3>PROFILE</h3>
                <v-divider class="mt-2 mb-5" />
                <v-container class="ma-0 pa-0" v-if="userStore().isLoggedIn">
                  <v-row class="ml-0">
                    <v-list density="compact">
                      <v-tooltip location="top">
                        <template v-slot:activator="{ isActive, props }">
                          <v-list-item prepend-icon="mdi-account-heart" v-on="isActive" v-bind="props">
                            <v-list-item-title :class="userStore().userData.is_superuser ? 'cool-shine' : ''">{{userStore().userData.first_name}} {{userStore().userData.last_name}}</v-list-item-title>
                          </v-list-item>
                        </template>
                        <span>Awesome person</span>
                      </v-tooltip>

                      <v-tooltip location="top">
                        <template v-slot:activator="{ isActive, props }">
                          <v-list-item prepend-icon="mdi-email" v-on="isActive" v-bind="props">
                            <v-list-item-title>{{userStore().userData.email}}</v-list-item-title>
                          </v-list-item>
                        </template>
                        <span>Account email</span>
                      </v-tooltip>

                      <v-tooltip location="top">
                        <template v-slot:activator="{ isActive, props }">
                          <v-list-item prepend-icon="mdi-cake-variant" v-on="isActive" v-bind="props">
                            <v-list-item-title>{{userStore().userData.created.toLocaleString().slice(0, 10)}}</v-list-item-title>
                          </v-list-item>
                        </template>
                        <span>Account creation date</span>
                      </v-tooltip>
                    </v-list>
                  </v-row>
                  <v-row class="ml-0">
                    <h3 class="mt-10">ACTIONS</h3>
                    <v-divider class="mt-2 mb-5" />
                    <v-container class="ma-0 pa-0" v-if="userStore().isLoggedIn">
                      <v-btn color="happy" @click="logout">Logout</v-btn>
                    </v-container>
                  </v-row>
                </v-container>
                <v-container v-else>
                  <p class="helper-text">
                    <v-img src="../../../id-card.svg" class="user" height="180" contain/>
                    <a @click="openLoginDialog">Login</a> or <a @click="openRegisterDialog">register</a> to manage your profile.
                  </p>
                </v-container>
              </div>
            </v-container>
          </v-sheet>
        </v-row>
      </v-col>

      <v-col cols="12" sm="8" md="8" lg="4" xl="6" xxl="8" class="cool-column pa-2">
        <v-sheet class="cool-sheet" rounded :elevation="5">
          <PatchList />
        </v-sheet>
      </v-col>

      <v-col cols="12" sm="12" md="12" lg="4" xl="3" xxl="2" class="cool-column px-2 py-2">
        <v-sheet class="cool-sheet" rounded :elevation="5">
          <LatestPatch/>
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>


<script setup lang="ts">
import { userStore } from '@/stores/user'
import LatestPatch from '@/components/LatestPatch.vue'
import PatchList from '@/components/PatchList.vue'
import { EventBus, events } from '@/event-bus'
function logout() {
  return userStore().logout();
}
function openLoginDialog() {
  EventBus.emit(events.OPEN_LOGIN_DIALOG)
}

function openRegisterDialog() {
  EventBus.emit(events.OPEN_REGISTER_DIALOG)
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

.user {
  margin-top: 40px;
  margin-bottom: 50px;
  filter: drop-shadow(0px 0px 15px red) invert(75%);
}

.cool-shine {
  padding-left: 48px;
  margin-left: -48px;
  background: linear-gradient(to right, fuchsia 0%, gold 15%, fuchsia 25%) 0;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shine 2s infinite ease-in-out;
  animation-fill-mode: forwards;
  -webkit-text-size-adjust: none;
  font-weight: 600;
  font-size: 16px;
  text-decoration: none;
  white-space: nowrap;
  font-style: italic;
}

@keyframes shine {
  0% {
    background-position: 0;
  }
  50% {
    background-position: 130px;
  }
  100% {
    background-position: 0;
  }
}
</style>