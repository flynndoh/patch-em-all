import { defineStore } from 'pinia'

export const persistenceStore = defineStore('persistence', {
  state: () => ({
    settings: {
      theme: 'dark',
    },
  }),
  actions: {
    updateSettings(partialSettings) {
      this.settings = {
        ...this.settings,
        ...partialSettings,
      }
    },
  },
  persist: true,
})
