<template>
  <v-container>
    <h3>PATCHES OVER TIME</h3>
    <v-divider class="mt-2 mb-5" />
    <v-btn @click="chart?.chart.resetZoom()" class="float-end">Reset</v-btn>
    <Line ref="chart" v-if="chartData.datasets.length > 0" :data="chartData" :options="chartOptions"/>
    <v-container v-else class="px-5">
      <v-img src="../../../line-chart.svg" class="chart-placeholder" height="120" contain/>
      <p v-if="users.length > 0" class="helper-text">No patches found for selected users :(</p>
      <p v-else class="helper-text">Select a user to see their patch history.</p>
    </v-container>
  </v-container>
</template>

<script setup lang="ts">
import { Line } from "vue-chartjs"
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
        patchPoints.push("circle")
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

const getOrCreateTooltip = (chart) => {
  let tooltipEl = chart.canvas.parentNode.querySelector("div");

  if (!tooltipEl) {
    tooltipEl = document.createElement("div");
    tooltipEl.style.background = "rgba(0, 0, 0, 0.7)";
    tooltipEl.style.borderRadius = "3px";
    tooltipEl.style.color = "white";
    tooltipEl.style.opacity = 1;
    tooltipEl.style.pointerEvents = "none";
    tooltipEl.style.position = "absolute";
    tooltipEl.style.transform = "translate(-50%, 0)";
    tooltipEl.style.transition = "all .1s ease";

    const table = document.createElement("table");
    table.style.margin = "0px";

    tooltipEl.appendChild(table);
    chart.canvas.parentNode.appendChild(tooltipEl);
  }

  return tooltipEl;
};

const externalTooltipHandler = (context) => {
  // Tooltip Element
  const {chart, tooltip} = context;
  const tooltipEl = getOrCreateTooltip(chart);

  // Hide if no tooltip
  if (tooltip.opacity === 0) {
    tooltipEl.style.opacity = 0;
    return;
  }

  // Set Text
  if (tooltip.body) {
    const bodyLines = tooltip.body.map(b => b.lines);
    const tableHeader = document.createElement("thead");
    const tableBody = document.createElement("tbody");
    bodyLines.forEach((body, i) => {
      const colors = tooltip.labelColors[i];

      // Create header
      const header = document.createElement("th");
      header.style.borderWidth = "0";

      const headerTimeseriesColor = document.createElement("span");
      headerTimeseriesColor.style.background = colors.backgroundColor;
      headerTimeseriesColor.style.borderColor = colors.borderColor;
      headerTimeseriesColor.style.borderWidth = "2px";
      headerTimeseriesColor.style.marginRight = "10px";
      headerTimeseriesColor.style.height = "10px";
      headerTimeseriesColor.style.width = "10px";
      headerTimeseriesColor.style.display = "inline-block";
      header.appendChild(headerTimeseriesColor);

      const seriesName = tooltip.dataPoints[i].dataset.label;
      const headerText = document.createTextNode(seriesName);
      header.appendChild(headerText);

      const headerRow1 = document.createElement("tr");
      headerRow1.style.borderWidth = "0";
      headerRow1.appendChild(header);
      tableHeader.appendChild(headerRow1);

      // Create body
      const bodyRow1 = document.createElement("tr");
      bodyRow1.style.backgroundColor = "inherit";
      bodyRow1.style.borderWidth = "0";

      const image = document.createElement("img");
      image.setAttribute('width', '150px');
      image.setAttribute('height', '150px');
      image.src = tooltip.labelPointStyles[i].pointStyle.src;
      bodyRow1.appendChild(image);
      tableBody.appendChild(bodyRow1);

      const bodyRow2 = document.createElement("tr");
      bodyRow2.style.backgroundColor = "inherit";
      bodyRow2.style.borderWidth = "0";
      bodyRow2.style.textAlign = "center";

      const patchNumber = document.createElement('h3');
      patchNumber.textContent = `#${tooltip.dataPoints[0].formattedValue}`;
      patchNumber.style.fontSize = '16pt';
      bodyRow2.appendChild(patchNumber);
      tableBody.appendChild(bodyRow2);

      const bodyRow3 = document.createElement("tr");
      bodyRow3.style.backgroundColor = "inherit";
      bodyRow3.style.borderWidth = "0";
      bodyRow3.style.textAlign = "center";

      const flightText = document.createElement('p');
      flightText.textContent = `Flight: ${tooltip.title[i]}`;
      flightText.style.fontSize = '12pt';
      flightText.style.color = 'gray';

      bodyRow3.appendChild(flightText);
      tableBody.appendChild(bodyRow3);
    });

    const tableRoot = tooltipEl.querySelector("table");

    // Remove old children
    while (tableRoot.firstChild) {
      tableRoot.firstChild.remove();
    }

    // Add new children
    tableRoot.appendChild(tableHeader);
    tableRoot.appendChild(tableBody);
  }

  const {offsetLeft: positionX, offsetTop: positionY} = chart.canvas;

  // Display, position, and set styles for font
  tooltipEl.style.opacity = 1;
  tooltipEl.style.left = positionX + tooltip.caretX + "px";
  tooltipEl.style.top = positionY + tooltip.caretY + "px";
  tooltipEl.style.font = tooltip.options.bodyFont.string;
  tooltipEl.style.padding = tooltip.options.padding + "px " + tooltip.options.padding + "px";
};

let chartOptions = {
  responsive: true,
  maintainAspectRatio: true,
  scales: {
    x: {
      type: "linear",
      title: {
        display: true,
        text: "Flight Number",
        color: "#00BD7EFF"
      }
    }
  },
  plugins: {
    tooltip: {
      enabled: false,
      position: "nearest",
      external: externalTooltipHandler
    },
    colors: {
      forceOverride: true
    },
    zoom: {
      animation: {
        duration: 1000,
        easing: "easeOutCubic"
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
        mode: "xy",
      }
    }
  },
  // onClick: function (evt, elements, chart) {
  //   const points = chart.getElementsAtEventForMode(evt, "nearest", { intersect: true }, true)
  //
  //   if (points.length) {
  //     const firstPoint = points[0]
  //     const name = chart.data.datasets[firstPoint.datasetIndex].label
  //     const time = chart.data.labels[firstPoint.index]
  //     const value = chart.data.datasets[firstPoint.datasetIndex].data[firstPoint.index]
  //     alert(`${name} : ${time} : ${value}.`)
  //   }
  // }
}
</script>

<style scoped>
.chart-placeholder {
  margin-top: 120px;
  margin-bottom: 40px;
  filter: drop-shadow(0px 0px 15px red) invert(75%);
}
</style>