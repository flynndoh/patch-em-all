import { defineStore } from 'pinia'

export const snackBarStore = defineStore('snackBar', {
  state: () => ({
    text: 'Default Text' as string,
    color: 'green' as string,
    time: 3500 as number
  }),

  actions: {
    setSnackBar(snack: { [name: string]: any }) {
      this.text = snack.text
      this.color = snack.color
      this.time = snack.time
    },

    removeSnackBar() {
      this.text = ''
    },

    resetSnackBar() {
      return
    }
  },
  getters: {
    snackbarColor: (state) => state.color,
    snackbarText: (state) => state.text,
    snackbarTime: (state) => state.time
  }
})
