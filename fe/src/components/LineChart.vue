<template>
  <Line :data="chartData" :options="chartOptions" />
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
  LinearScale,
  CategoryScale, Chart
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, LinearScale, CategoryScale)

defineProps<{
  chartData: {
    type: Object,
    required: true
  }
}>()

let chartOptions = {
  responsive: true,
  scales: {
    x: {
      type: 'linear'
    }
  },
  plugins: {
    tooltip: {
      // Disable the default on-canvas tooltip
      enabled: true,
      position: 'nearest',
    }
  },
  onClick: function (evt, elements, chart) {
    const points = chart.getElementsAtEventForMode(evt, 'nearest', { intersect: true }, true);

    if (points.length) {
      const firstPoint = points[0];
      const name = chart.data.datasets[firstPoint.datasetIndex].label;
      const time = chart.data.labels[firstPoint.index];
      const value = chart.data.datasets[firstPoint.datasetIndex].data[firstPoint.index];
      alert(`${name} : ${time} : ${value}.`);

    }
  }
}
</script>
