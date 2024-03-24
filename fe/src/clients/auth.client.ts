import { type AxiosResponse } from 'axios'
import CoreClient from './core.client'
import UserClient from './user.client'

export interface AuthApi {
  login(payload: Requests.Login): Promise<void>
  register(payload: Requests.Register): Promise<AxiosResponse<Responses.Register>>
  logout(): Promise<void>
  forgotPassword(payload: Requests.ForgotPassword): Promise<void>
  resetPassword(payload: Requests.ResetPassword): Promise<void>
}

export declare namespace Responses {
  interface Register {
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

export declare namespace Requests {
  interface Register {
    first_name: string
    last_name: string
    email: string
    password: string
  }

  interface Login {
    username: string
    password: string
    // grant_type: string
    // scope: string
    // client_id: string
    // client_secret: string
  }

  interface ForgotPassword {
    email: string
  }

  interface ResetPassword {
    token: string
    password: string
  }
}

class AuthClient implements AuthApi {
  async login(payload: Requests.Login): Promise<void> {
    console.log(payload)
    return CoreClient.client.postForm('/auth/login', payload)
  }

  async register(payload: Requests.Register): Promise<AxiosResponse<Responses.Register>> {
    return CoreClient.client.post<Responses.Register>('/auth/register', payload)
  }

  async logout(): Promise<void> {
    return CoreClient.client.post('/auth/logout')
  }

  async forgotPassword(payload: Requests.ForgotPassword): Promise<void> {
    return CoreClient.client.post('/auth/forgot-password', payload)
  }

  async resetPassword(payload: Requests.ResetPassword): Promise<void> {
    return CoreClient.client.post('/auth/reset-password', payload)
  }
}

export default new AuthClient()
