<script>
/**
 * Mixin that allows us to display notification mixins
 * from anywhere in the application
 */
import { snackBarStore } from '@/stores/snackbar'

export default {
  data() {
    return {}
  },

  methods: {
    showErrorSnackbar: function (text, time) {
      this._showSnackbar(text, 'red', time)
    },
    showInfoSnackbar: function (text, time) {
      this._showSnackbar(text, 'blue', time)
    },
    showSuccessSnackbar: function (text, time) {
      this._showSnackbar(text, 'green', time)
    },
    _showSnackbar: function (text, color, time) {
      snackBarStore().setSnackBar({ text: text, color: color, time: time })
    }
  }
}
</script>
