import { defineStore } from 'pinia'
import AuthClient, { type Requests as AuthRequests } from '@/clients/auth.client'
import UserClient, { type Responses } from '@/clients/user.client'
import { isEmpty } from '@/utils'

export const userStore = defineStore('users', {
  state: () => ({
    userData: {} as Responses.User,
    patches: [] as Responses.Patch[],
    pokemon: [] as Responses.Pokemon[],
  }),

  actions: {
    async login(email: string, password: string): Promise<Responses.User> {
      const request: AuthRequests.Login = {
        username: email,
        password: password
      }
      await AuthClient.login(request).catch((error) => {
        return Promise.reject(error);
      })

      this.userData = (await UserClient.getMe()).data
      return this.userData;
    },
    async registerAndLogin(firstName: string, lastName: string, email: string, password: string): Promise<Responses.User> {
      const request: AuthRequests.Register = {
        first_name: firstName,
        last_name: lastName,
        email: email,
        password: password
      }
      await AuthClient.register(request).catch((error) => {
        return Promise.reject(error);
      })
      return await this.login(email, password).catch((error) => {
        return Promise.reject(error);
      })
    },
    async refreshMe(): Promise<Responses.User | undefined> {
      return await UserClient.getMe().then((userResponse) => {
        if (userResponse.status === 200) {
          this.userData = userResponse.data;
          return Promise.resolve(this.userData);
        }
      }).catch(() => {
          // Resolving promise rather than rejecting as I am using basic auth with no access to header only cookie.
          this.userData = {} as Responses.User;
          return Promise.resolve(this.userData);
        }
      );
    },
    async refreshMyPatches(): Promise<Responses.Patch[] | undefined> {
      return await UserClient.getMyPatches().then((patchesResponse) => {
        if (patchesResponse.status === 200) {
          this.patches = patchesResponse.data.patches;
          return Promise.resolve(this.patches);
        }
      }).catch(() => {
          this.patches = [] as Responses.Patch[];
          return Promise.reject(this.patches);
        }
      );
    },
    async refreshMyPokemon(): Promise<Responses.Pokemon[] | undefined> {
      return await UserClient.getManyPokemon({pokemon_ids: this.patches.map((x) => x.patch_number)}).then((pokemonResponse) => {
        if (pokemonResponse.status === 200) {
          this.pokemon = pokemonResponse.data;
          return Promise.resolve(this.pokemon);
        }
      }).catch(() => {
          this.pokemon = [] as Responses.Pokemon[];
          return Promise.reject(this.pokemon);
        }
      );
    },
    async logout() {
      this.userData = {} as Responses.User;
      this.patches = [] as Responses.Patch[];
      this.pokemon = [] as Responses.Pokemon[];
      await AuthClient.logout();
    }
  },
  getters: {
    isLoggedIn: (state) => !isEmpty(state.userData),
    latestPatch: (state) => state.patches.reduce((a, b) => a.patch_number < b.patch_number ? a : b),
    latestPokemon: (state) => state.pokemon.reduce((a, b) => a.id < b.id ? a : b),
    // currentPatent: (state) => ,
  }
})
