<template>
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
            <p v-else class="helper-text"><a @click="openAddPatchDialog">Add a patch</a> to see what your pokemon is.<br /></p>
          </v-container>
        </v-window-item>

        <v-window-item value="two"/>
        <v-window-item value="three"/>
      </v-window>
    </v-card-text>
  </v-container>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { userStore } from '@/stores/user'
import { EventBus, events } from '@/event-bus'
import { pngProxy } from '@/mixins/cors-proxy'
import { randomColourHex } from '@/mixins/visuals'

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

function pokedex(name: string) {
  return `https://www.pokemon.com/us/pokedex/${name}`
}

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
  });
})
</script>

<style scoped>
.pokemon-placeholder {
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
