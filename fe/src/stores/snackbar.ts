import { defineStore } from 'pinia'

export const snackBarStore = defineStore('snackBar', {
  state: () => ({
    text: '' as string,
    color: 'green' as string,
    time: 3500 as number,
  }),

  actions: {
    resetSnackBar() {
      this.text = '';
      this.color = 'green';
      this.time = 3500;
    },

    setSnackBar(snack: { [name: string]: any }) {
      this.text = snack.text
      this.color = snack.color
      this.time = snack.time
    }
  },
  getters: {
    snackbarColor: (state) => state.color,
    snackbarText: (state) => state.text,
    snackbarTime: (state) => state.time
  }
})
