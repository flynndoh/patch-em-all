<template>
  <v-container>
    <v-row no-gutters>
      <v-col cols="12" sm="4" md="4" lg="4" xl="3" xxl="2" class="cool-column">
        <v-row no-gutters style="flex-direction: column;" class="pa-2">
          <v-sheet class="cool-sheet" rounded :elevation="5">
            <SearchPeople :users="allUsers" @selected-users-updated="(x) => selectedUsers = x"/>
          </v-sheet>
        </v-row>
        <v-row no-gutters style="flex-direction: column;" class="pa-2">
          <v-sheet class="cool-sheet" rounded :elevation="5">
            <PatchList />
          </v-sheet >
        </v-row>
      </v-col>

      <v-col cols="12" sm="8" md="8" lg="4" xl="6" xxl="8" class="cool-column pa-2">
        <v-sheet class="cool-sheet" rounded :elevation="5">
          <LineChart :users="selectedUsers"/>
        </v-sheet>
      </v-col>

      <v-col cols="12" sm="12" md="12" lg="4" xl="3" xxl="2" class="cool-column px-2 py-2">
        <v-row no-gutters style="flex-direction: column;">
          <v-sheet class="cool-sheet" rounded :elevation="5">
            <v-container>
              <h3>LATEST PATCH</h3>
              <v-divider class="mt-2 mb-5" />

              <v-tabs v-model="latestPatchTab" slider-color="happy">
                <v-tab value="one">Pokemon</v-tab>
                <v-tab value="two" disabled>Movie</v-tab>
                <v-tab value="three" disabled>US Patent</v-tab>
              </v-tabs>

              <v-card-text>
                <v-window v-model="latestPatchTab">
                  <v-window-item value="one">
                    <div v-if="latestPokemon" style="display: grid;" class="pokemon-container">
                      <v-img height="250" :style="pokemonHighlight" class="pokemon-highlight mt-0" :src="pngProxy(latestPokemon.image)"/>
                      <v-img height="250" class="pokemon" :src="pngProxy(latestPokemon.image)"/>
                      <div style="text-align: center; display: flex; align-items: center; justify-content: center;">
                        <a :href="pokedex(latestPokemon.name)" target="_blank"><h1 class="green">{{latestPokemon.name}}</h1></a>
                        <h3 class="ml-3" style="font-size: 16pt">#{{latestPokemon.id}}</h3>
                      </div>
                    </div>
                    <v-container v-else class="px-5">
                      <v-img src="../../../pokemon-1.svg" class="pokemon-placeholder" height="120" contain/>
                      <p v-if="!clientLoggedIn" class="helper-text">
                        <a @click="openLoginDialog">Login</a> or
                        <a @click="openRegisterDialog">register</a> to see your current pokemon.
                      </p>
                      <p v-else class="helper-text">you haven't added any patches :(<br /><a @click="openAddPatchDialog">add some!</a></p>
                    </v-container>
                  </v-window-item>

                  <v-window-item value="two"/>
                  <v-window-item value="three"/>
                </v-window>
              </v-card-text>
            </v-container>
          </v-sheet>
        </v-row>
      </v-col>
    </v-row>

  </v-container>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import SearchPeople from '@/components/SearchPeople.vue'
import PatchList from '@/components/PatchList.vue'
import LineChart from '@/components/LineChart.vue'
import { EventBus, events } from '@/event-bus'
import { userStore } from '@/stores/user'
import { pngProxy } from '@/mixins/cors-proxy'
import { type Responses } from '@/clients/user.client'
import { randomColourHex } from '@/mixins/visuals'

const selectedUsers = ref<Responses.User[]>([]);

function pokedex(name: string) {
  return `https://www.pokemon.com/us/pokedex/${name}`
}

const clientLoggedIn = computed(() => {
  return userStore().isLoggedIn;
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

const patches = computed(() => {
  return userStore().patches
})

const allUsers = computed(() => {
  return userStore().allUsers
})

const latestPatch = computed(() => {
  return userStore().latestPatch
})

const latestPokemon = computed(() => {
  return userStore().latestPokemon
})

const pokemonHighlight = {
  filter: `drop-shadow(0px 0px 15px #${randomColourHex(0.0005 * (latestPokemon.value ? latestPokemon.value.id : 0))}) invert(75%)`
}

let latestPatchTab = ref(null);
onMounted(() => {
  userStore().refreshAllUsers()

  EventBus.on(events.CLIENT_LOGGED_IN, async () => {
    await userStore().refreshMyPatches();
    await userStore().refreshMyPokemon();
    if (userStore().pokemon) {
      selectedUsers.value.push(userStore().userData);
    }
  });
})
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

.pokemon-placeholder {
  margin-top: 60px;
  margin-bottom: 40px;
  filter: drop-shadow(0px 0px 15px red) invert(75%);
}

.chart-placeholder {
  margin-top: 60px;
  margin-bottom: 40px;
  filter: drop-shadow(0px 0px 15px red) invert(75%);
}

.pokemon-container {
  margin-top: 60px;
  margin-bottom: 40px;
}

.pokemon-highlight, .pokemon {
  grid-area: 1 / 1;
}
</style>