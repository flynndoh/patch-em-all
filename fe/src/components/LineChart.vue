<template>
  <v-container>
    <h3>PATCHES OVER TIME</h3>
    <v-divider class="mt-2 mb-5" />
    /* tslint:disable */
    <v-btn @click="chart?.chart.resetZoom()">Reset</v-btn>
    /* tslint:enable */
    <Line ref="chart" v-if="chartData.datasets" :data="chartData" :options="chartOptions"/>
    <v-container v-else class="px-5">
      <v-img src="../../../line-chart.svg" class="chart-placeholder" height="120" contain/>
      <p v-if="users" class="helper-text">no patches found for selected users :(</p>
      <p v-else class="helper-text">select a user to see their patch history</p>
    </v-container>
  </v-container>
</template>

<script setup lang="ts">
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  LinearScale, type ChartData, type ChartDataset, Colors
} from 'chart.js'
import 'chartjs-adapter-moment';
import { userStore } from '@/stores/user'
import { type Responses } from '@/clients/user.client'
import { computedAsync } from '@vueuse/core'
import zoomPlugin from 'chartjs-plugin-zoom';
import { ref } from 'vue'

ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, LinearScale, Colors, zoomPlugin)

const props = defineProps<{
  users: Responses.User[]
}>()

const chart = ref(null);

const chartData = computedAsync(async () => {
  let data = {
    labels: [] as number[],
    datasets: [] as ChartDataset[]
  } as ChartData

  for (const user of props.users) {
    let patches = await userStore().getPatchesForUser(user.id);
    if (patches) {
      let patchPoints = [] as (HTMLImageElement|string)[];
      let pokemon = await userStore().getPokemon(patches.map(p => p.patch_number));
      if (pokemon) {
        for (const poke of pokemon) {
          let image = new Image(70, 70);
          image.src = poke.sprite;
          patchPoints.push(image)
        }
      } else {
        patchPoints.push('circle')
      }

      data.datasets.push({
        label: [user.first_name, user.last_name].join(" "),
        data: patches.map(patch => ({x: patch.flight.id, y: patch.patch_number})),
        fill: false,
        tension: 0.1,
        pointStyle: patchPoints,
        pointRadius: 15,
        pointHoverRadius: 30,
      });
    }
  }
  return Promise.resolve(data);
},
{
  labels: [] as number[],
  datasets: [] as ChartDataset[]
} as ChartData);

let chartOptions = {
  responsive: true,
  maintainAspectRatio: true,
  scales: {
    x: {
      type: 'linear'
    }
  },
  plugins: {
    tooltip: {
      enabled: true,
      position: 'nearest'
    },
    colors: {
      forceOverride: true
    },
    zoom: {
      animation: {
        duration: 1000,
        easing: 'easeOutCubic'
      },
      limits: {
        x: {
          min: -10,
        },
        y: {
          min: -10,
        }
      },
      pan: {
        enabled: true,
      },
      zoom: {
        wheel: {
          enabled: true,
        },
        pinch: {
          enabled: true
        },
        mode: 'xy',
      }
    }
  },
  onClick: function (evt, elements, chart) {
    const points = chart.getElementsAtEventForMode(evt, 'nearest', { intersect: true }, true)

    if (points.length) {
      const firstPoint = points[0]
      const name = chart.data.datasets[firstPoint.datasetIndex].label
      const time = chart.data.labels[firstPoint.index]
      const value = chart.data.datasets[firstPoint.datasetIndex].data[firstPoint.index]
      alert(`${name} : ${time} : ${value}.`)
    }
  }
}
</script>