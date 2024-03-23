const rules = {
  required: [(v: string) => v != '' || 'Required', (v: string) => v != undefined || 'Required'],
  email: [
    (v: string) => v != '' || 'Required',
    (v: string) => v != undefined || 'Required',
    (v: string) =>
      !v || /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || 'Invalid email address'
  ]
}

export default rules
