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

// 1, "It's a Test", 25 May 2017 04:20
// 2, "Still Testing", 21 January 2018 01:43
// 3, "It's Business Time", 11 November 2018 03:50
// 4, "This One's For Pickering", 16 December 2018 06:33
// 5, "Two Thumbs Up", 28 March 2019 23:27
// 6, "That's a Funny Looking Cactus", 5 May 2019 06:00
// 7, "Make it Rain", 29 June 2019 04:30
// 8, "Look Ma, No Hands", 19 August 2019 12:12
// 9, "As the Crow Flies", 17 October 2019 01:22
// 10, "Running Out Of Fingers", 6 December 2019 08:18
// 11, "Birds of a Feather", 31 January 2020 02:56
// 12, "Don't Stop Me Now", 13 June 2020 05:12:12
// 13, "Pics Or It Didn't Happen" 4 July 2020 21:19:36
// 14, "I Can't Believe It's Not Optical", 31 August 2020 03:05:47
// 15, "In Focus", 28 October 2020 21:21:27
// 16, "Return To Sender", 20 November 2020 02:20:01
// 17, "The Owl's Night Begins", 15 December 2020 10:09:27
// 18, "Another One Leaves The Crust", 20 January 2021 07:26:00
// 19, "They Go Up So Fast", 22 March 2021 22:30
// 20, "Running Out Of Toes", 15 May 2021 11:11
// 21, "It's A Little Chile Up Here", 29 July 2021 06:00
// 22, "Love At First Insight", 18 November 2021 01:38:13
// 23, "A Data With Destiny", 9 December 2021 00:02
// 24, "The Owl's Night Continues", 28 February 2022 20:37
// 25, "Without Mission A Beat", 2 April 2022 12:41
// 26, "There And Back Again", 2 May 2022 22:49
// 27, "CAPSTONE", 28 June 2022 09:55
// 28, "Wise One Looks Ahead". 13 July 2022 06:30
// 29, "Antipodean Adventure", 4 August 2022 05:00
// 30, "The Owl Spreads Its Wings", 15 September 2022 20:38
// 31, "It Argos Up From Here", 7 October 2022 17:09
// 32, "Catch Me If You Can", 4 November 2022 17:27
// 33, "Virginia Is For Launch Lovers", 24 January 2023 23:00
// 34, "Stronger Together", 16 March 2023 22:39
// 35, "The Beat Goes On", 24 March 2023 09:14
// 36, "Rocket Like A Hurricane", 8 May 2023 01:00
// 37, "Coming to a Storm Near You", 26 May 2023 03:46
// 38, "Baby Come Back", 18 July 2023 01:27
// 39, "We Love The Nightlife", 23 August 2023 23:45
// 40, "We Will Never Desert You", 19 September 2023 06:55
// 41, "The Moon God Awakens", 15 December 2023 04:05
// 42, "Four Of A Kind", 31 January 2024 06:34
// 43, "On Closer Inspection", 18 February 2024 14:52
// 44, "Owl Night Long", 12 March 2024 15:03
// 45, "Live and Let Fly", 21 March 2024 15:03


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