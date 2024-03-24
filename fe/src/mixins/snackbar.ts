import { snackBarStore } from '@/stores/snackbar'

export function showErrorSnackbar(text: string, time?: number) {
  _showSnackbar(text, 'red', time)
}
export function showInfoSnackbar(text: string, time?: number) {
  _showSnackbar(text, 'blue', time)
}
export function showSuccessSnackbar(text: string, time?: number) {
  _showSnackbar(text, 'green', time)
}
export function _showSnackbar(text: string, color: string, time?: number) {
  snackBarStore().setSnackBar({ text: text, color: color, time: time })
}
