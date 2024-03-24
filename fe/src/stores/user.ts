import { defineStore } from 'pinia'
import AuthClient, { type Requests } from '@/clients/auth.client'
import UserClient, { type Responses } from '@/clients/user.client'
import { isEmpty } from '@/utils'

export const userStore = defineStore('users', {
  state: () => ({
    userData: {} as Responses.User,
  }),

  actions: {
    async login(email: string, password: string) {
      try {
        const request: Requests.Login = {
          username: email,
          password: password
        }
        await AuthClient.login(request)
        this.userData = (await UserClient.getMe()).data
      } catch (error) {
        // let the form component display the error
        return error
      }
    },
    async registerAndLogin(firstName: string, lastName: string, email: string, password: string) {
      try {
        const request: Requests.Register = {
          first_name: firstName,
          last_name: lastName,
          email: email,
          password: password
        }
        await AuthClient.register(request)
        await this.login(email, password)
      } catch (error) {
        // let the form component display the error
        return error
      }
    },
    async refreshMe(): Promise<Responses.User | undefined> {
      return await UserClient.getMe().then((userResponse) => {
        if (userResponse.status === 200) {
          this.userData = userResponse.data;
          return Promise.resolve(userResponse.data);
        }
      }).catch(() => {
          // Resolving promise rather than rejecting as I am using basic auth with no access to header only cookie.
          this.userData = {} as Responses.User;
          return Promise.resolve({} as Responses.User);
        }
      );
    },
    async logout() {
      this.userData = {} as Responses.User;
      await AuthClient.logout();
    }
  },
  getters: {
    isLoggedIn: (state) => !isEmpty(state.userData),
  }
})
