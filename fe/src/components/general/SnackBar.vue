<template>
  <v-snackbar :color="color" v-model="show" :timeout="timeout" right bottom>
    {{ message }}
    <v-btn text color="white" v-on:click="show = false">Close</v-btn>
  </v-snackbar>
</template>

<style></style>

<script>
import { snackBarStore } from '@/stores/snackbar'

export default {
  data() {
    return {
      show: false,
      message: 'If you can see this message something broke!',
      color: 'red',
      timeout: 3500 // Use this to change global snackbar display time
    }
  },
  /**
   * Watch for changes in the Index Store to update SNACKBAR.
   */
  created: function () {
    snackBarStore().$subscribe((mutation, state) => {
      if (state.text !== '') {
        this.message = state.text
        this.color = state.color
        this.timeout = state.time
        this.show = true
        snackBarStore().resetSnackBar()
      }
    })
  }
}
</script>
