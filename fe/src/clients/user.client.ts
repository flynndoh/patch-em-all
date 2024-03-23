import { type AxiosResponse } from 'axios'
import CoreClient from './core.client'

export interface UserApi {
  getMe(): Promise<AxiosResponse<Responses.User>>
}

export declare namespace Responses {
  interface User {
    id: string
    email: string
    is_active: boolean
    is_superuser: boolean
    is_verified: boolean
    first_name: string
    last_name: string
    created: Date
  }
}

export declare namespace Requests {}

class UserClient implements UserApi {
  async getMe(): Promise<AxiosResponse<Responses.User>> {
    return CoreClient.client.post<Responses.User>('/users/me')
  }
}

export default new UserClient()
