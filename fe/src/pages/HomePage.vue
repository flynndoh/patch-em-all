<template>
  <v-container>
    <v-row no-gutters>
      <v-col cols="12" sm="4" md="4" lg="4" xl="3" style="display: flex; flex-direction: column;">
        <v-row no-gutters style="flex-direction: column;" class="pa-2">
          <v-sheet class="cool-sheet" rounded :elevation="5">
            <SearchPeople
              :people="['Matt Carroll', 'Flynn Doherty', 'Archie Porter']"
            />
          </v-sheet>
        </v-row>
        <v-row no-gutters style="flex-direction: column;" class="pa-2">
          <v-sheet class="cool-sheet helper-text" rounded :elevation="5">
            <PatchList />
          </v-sheet >
        </v-row>
      </v-col>

      <v-col cols="12" sm="8" md="8" lg="4" xl="6" style="flex-direction: column;" class="pa-2">
        <v-sheet class="cool-sheet" rounded :elevation="5">
          <v-container>
            <h3>PATCHES OVER TIME</h3>
            <v-divider class="mt-2 mb-5" />
            <LineChart :chart-data="chartData"/>
          </v-container>
        </v-sheet>
      </v-col>

      <v-col cols="12" sm="12" md="12" lg="4" xl="3" class="px-2 py-1">
        <v-row no-gutters style="flex-direction: column;">
          <v-sheet class="cool-sheet" rounded :elevation="5">
            <v-container>
              <h3>LATEST PATCH</h3>
              <v-divider class="mt-2 mb-5" />

              <v-tabs v-model="latestPatchTab" >
                <v-tab value="one">Pokemon</v-tab>
                <v-tab value="two" disabled>Movie</v-tab>
                <v-tab value="three" disabled>US Patent</v-tab>
              </v-tabs>

              <v-card-text>
                <v-window v-model="latestPatchTab">
                  <v-window-item value="one">
                    <div style="display: grid;" class="pokemon-container">
                      <v-img height="300" :style="pokemonHighlight" class="pokemon-highlight mt-0" :src="png_proxy(latestPokemon.image)"/>
                      <v-img height="300" class="pokemon" :src="png_proxy(latestPokemon.image)"/>
                      <div style="text-align: center; display: flex; align-items: center; justify-content: center;">
                        <a :href="pokedex(latestPokemon.name)" target="_blank"><h1 class="green">{{latestPokemon.name}}</h1></a>
                        <h3 class="ml-3" style="font-size: 16pt">#{{latestPokemon.id}}</h3>
                      </div>
                    </div>
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
import { computed, onMounted, ref } from 'vue'
import type { ChartData } from 'chart.js'
import SearchPeople from '@/components/SearchPeople.vue'
import PatchList from '@/components/PatchList.vue'
import LineChart from '@/components/LineChart.vue'
import { EventBus, events } from '@/event-bus'
import { userStore } from '@/stores/user'
import { png_proxy } from '@/mixins/cors-proxy'

function pokedex(name: string) {
  return `https://www.pokemon.com/us/pokedex/${name}`
}

const patches = computed(() => {
  return userStore().patches
})

const latestPatch = computed(() => {
  return userStore().latestPatch
})

const latestPokemon = computed(() => {
  return userStore().latestPokemon
})

let chartData: ChartData = {
  labels: patches.value.map((x) => x.flight.id),
  datasets: [
    {
      label: 'My Patches',
      data: patches.value.map((x) => x.patch_number),
      fill: false,
      borderColor: 'rgb(75, 192, 192)',
      tension: 0.1
    }
  ]
}

let pokemonColor = Math.floor((Math.abs(Math.sin(1 - (0.0005 * latestPokemon.value.id)) * 16777215))).toString(16);
const pokemonHighlight = {
  filter: `drop-shadow(0px 0px 15px #${pokemonColor}) invert(75%)`
}

let latestPatchTab = ref(null);
onMounted(() => {
  EventBus.on(events.CLIENT_LOGGED_IN, () => {
    userStore().refreshMyPatches()
    userStore().refreshMyPokemon()
  });
})
</script>

<style scoped lang="scss">
.cool-sheet {
  padding: 8px;
  height: 100%;
}
.pokemon-container {
  margin-top: 60px;
  margin-bottom: 40px;
}

.pokemon-highlight, .pokemon {
  grid-area: 1 / 1;
}
</style>