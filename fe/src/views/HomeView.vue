<template>
  <main>
    <v-btn circle v-if="!theme.global.current.value.dark" dark x-small fab @click="toggleTheme">
      <v-icon class="mr-1" light>mdi-moon-waxing-crescent</v-icon>
    </v-btn>
    <v-btn circle v-else light x-small fab @click="toggleTheme">
      <v-icon dark>mdi-white-balance-sunny</v-icon>
    </v-btn>

    <LandingPage />
  </main>
</template>

<script setup lang="ts">
import LandingPage from '@/components/LandingPage.vue'

import { useTheme } from 'vuetify'

const theme = useTheme()

function toggleTheme() {
  theme.global.name.value = theme.global.current.value.dark ? 'light' : 'dark'
  //showInfoSnackbar("Yeet")
}
</script>
