<template>
  <v-container class="main-container">
    <v-row no-gutters>
      <v-col cols="12" sm="2">
        <v-row no-gutters>
          <v-card class="ma-2 pa-2">
            <SearchPeople
              :people="['Matt Carroll', 'Flynn Doherty', 'Archie Porter', 'Lara Collier']"
            />
          </v-card>
        </v-row>
        <v-row no-gutters>
          <v-card class="ma-2 pa-2">
            <v-container v-if="clientLoggedIn">
              <p>you don't have any patches :(<br /><a @click="goToAddPatches">add some!</a></p>
            </v-container>

            <v-container v-else class="px-5">
              <p class="helper-text">
                <a @click="openLoginDialog">Login</a> or
                <a @click="openRegisterDialog">register</a> to start tracking your patches
              </p>
            </v-container>
          </v-card>
        </v-row>
      </v-col>
      <v-col cols="12" sm="7">
        <v-card class="ma-2 pa-2">
          <CustomTooltipLineChart :chart-data="chartData" />
        </v-card>
      </v-col>
      <v-col cols="12" sm="3">
        <v-card class="ma-2 pa-2"> </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import type { ChartData } from 'chart.js'
import CustomTooltipLineChart from '@/components/LineChart.vue'
import SearchPeople from '@/components/SearchPeople.vue'
import { userStore } from '@/stores/user'
import { EventBus, events } from '@/event-bus'
import { goToRoute } from '@/router'
import routes from '@/router/routes'

let loaded = false

let chartData: ChartData = {
  labels: ['1', '3', '4', '6', '12', '32', '43'],
  datasets: [
    {
      label: 'My First Dataset',
      data: [65, 59, 80, 81, 56, 55, 40],
      fill: false,
      borderColor: 'rgb(75, 192, 192)',
      tension: 0.1
    }
  ]
}

const clientLoggedIn = computed(() => {
  return userStore().isLoggedIn
})

function openLoginDialog() {
  console.log('here')
  EventBus.emit(events.OPEN_LOGIN_DIALOG)
}

function openRegisterDialog() {
  EventBus.emit(events.OPEN_REGISTER_DIALOG)
}

function goToAddPatches() {
  goToRoute(routes.ADD_PATCHES)
}

onMounted(() => {
  try {
    // const { userlist } = await fetch('/api/userlist')
    // this.chartdata = userlist

    loaded = true
  } catch (e) {
    console.error(e)
  }
})
</script>

<style scoped>
.main-container {
  height: 100%;
}
</style>
