const rules = {
  required: [
    (v: string) => v != '' || 'Required',
    (v: string) => v != undefined || 'Required'
  ],
  email: [
    (v: string) => v != '' || 'Required',
    (v: string) => v != undefined || 'Required',
    (v: string) => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || 'Invalid email address'
  ],
  pinCode: [
    (v: string) => v != '' || 'Required',
    (v: string) => v != undefined || 'Required',
    (v: string) => /^\d{4}$/.test(v) || 'Invalid 4 digit pin code'
  ]
}

export default rules
