import axios, { type AxiosInstance } from 'axios'
axios.defaults.withCredentials = true

const protocol = 'http'
const host = 'localhost'
const port = ':3000'
const apiURL = `${protocol}://${host}${port}/api/v1/`

class CoreClient {
  client: AxiosInstance = axios.create({
    baseURL: apiURL,
    withCredentials: true
  })
}

export default new CoreClient()
