import { defineStore } from 'pinia'
import AuthClient, { type Requests } from '@/clients/auth.client'
import UserClient, { type Responses } from '@/clients/user.client'

export const userStore = defineStore('users', {
  state: () => ({
    userData: {} as Responses.User,
    isLoggedIn: false as boolean
  }),

  actions: {
    async loginUser(email: string, password: string) {
      try {
        const request: Requests.Login = {
          username: email,
          password: password
        }
        await AuthClient.login(request)
        this.userData = (await UserClient.getMe()).data
        this.isLoggedIn = true
      } catch (error) {
        // let the form component display the error
        return error
      }
    },
    async registerUser(firstName: string, lastName: string, email: string, password: string) {
      try {
        const request: Requests.Register = {
          first_name: firstName,
          last_name: lastName,
          email: email,
          password: password
        }
        await AuthClient.register(request)
        await this.loginUser(email, password)
      } catch (error) {
        // let the form component display the error
        return error
      }
    }
  }
})
