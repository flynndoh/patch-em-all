<template>
  <main>
    <LandingPage />
  </main>
</template>

<script setup lang="ts">
import LandingPage from '@/components/LandingPage.vue'

import { persistenceStore } from '@/stores/persistence'
import { useTheme } from 'vuetify'
import { showInfoSnackbar } from '@/mixins/snackbar'
const theme = useTheme()


function toggleTheme() {
  theme.global.name.value = theme.global.current.value.dark ? 'light' : 'dark'
  persistenceStore().updateSettings({'theme': theme.global.name.value})

  if (!theme.global.current.value.dark) {
    showInfoSnackbar("🙄")
  }
}
</script>
