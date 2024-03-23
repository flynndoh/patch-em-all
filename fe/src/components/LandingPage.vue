<template>
  <v-container class="main-container">
    <v-row no-gutters>
      <v-col cols="12" sm="2">
        <v-card class="ma-2 pa-2">
          <SearchPeople :people="['Matt Carroll', 'Flynn Doherty', 'Archie Porter', 'Lara Collier']"/>
        </v-card>
      </v-col>
      <v-col cols="12" sm="7">
        <v-card class="ma-2 pa-2">
          <CustomTooltipLineChart :chart-data="chartData" />
        </v-card>
      </v-col>
      <v-col cols="12" sm="3">
        <v-card class="ma-2 pa-2">
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import type { ChartData } from 'chart.js'
import CustomTooltipLineChart from '@/components/LineChart.vue'
import SearchPeople from '@/components/SearchPeople.vue'

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