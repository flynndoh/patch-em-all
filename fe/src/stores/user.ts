import { defineStore } from 'pinia'
import AuthClient, { type Requests as AuthRequests } from '@/clients/auth.client'
import UserClient, { type Responses } from '@/clients/user.client'
import { isEmpty } from '@/utils'

export const userStore = defineStore('users', {
  state: () => ({
    userData: {} as Responses.User,
    patches: [] as Responses.Patch[],
    allUsers: [] as Responses.User[],
    pokemon: [] as Responses.Pokemon[],
  }),

  actions: {
    async login(email: string, password: string): Promise<Responses.User> {
      const request: AuthRequests.Login = {
        username: email,
        password: password
      }
      await AuthClient.login(request).catch((err) => {
        return Promise.reject(err.message);
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
      await AuthClient.register(request).catch((err) => {
        if (err.response.data.detail === 'REGISTER_USER_ALREADY_EXISTS') {
          return Promise.reject("User already exists with that email.");
        }
        return Promise.reject(err.message);
      })
      return await this.login(email, password).catch((err) => {
        return Promise.reject(err.message);
      })
    },
    async refreshMe(): Promise<Responses.User | undefined> {
      return await UserClient.getMe().then((userResponse) => {
        if (userResponse.status === 200) {
          this.userData = userResponse.data;
          return Promise.resolve(this.userData);
        }
      }).catch((err) => {
          // Resolving promise rather than rejecting as I am using basic auth with no access to header only cookie.
          this.userData = {} as Responses.User;
          return Promise.resolve(err);
        }
      );
    },
    async refreshMyPatches(): Promise<Responses.Patch[] | undefined> {
      return await UserClient.getMyPatches().then((patchesResponse) => {
        if (patchesResponse.status === 200) {
          this.patches = patchesResponse.data.patches;
          return Promise.resolve(this.patches);
        }
      }).catch((err) => {
          this.patches = [] as Responses.Patch[];
          return Promise.reject(err);
        }
      );
    },
    async refreshAllUsers(): Promise<Responses.User[] | undefined> {
      return await UserClient.getAllUsers().then((allUsersResponse) => {
        if (allUsersResponse.status === 200) {
          this.allUsers = allUsersResponse.data;
          return Promise.resolve(this.allUsers);
        }
      }).catch((err) => {
          this.allUsers = [] as Responses.User[];
          return Promise.reject(err);
        }
      );
    },
    async refreshMyPokemon(): Promise<Responses.Pokemon[] | undefined> {
      return await UserClient.getManyPokemon({pokemon_ids: this.patches.map((x) => x.patch_number)}).then((pokemonResponse) => {
        if (pokemonResponse.status === 200) {
          this.pokemon = pokemonResponse.data;
          return Promise.resolve(this.pokemon);
        }
      }).catch((err) => {
          this.pokemon = [] as Responses.Pokemon[];
          return Promise.reject(err);
        }
      );
    },
    async getPatchesForUser(id: string): Promise<Responses.Patch[] | undefined> {
      return await UserClient.getPatchesForUser(id).then((patchesResponse) => {
        if (patchesResponse.status === 200) {
          return Promise.resolve(patchesResponse.data.patches);
        }
      }).catch((err) => {
          return Promise.reject(err);
        }
      );
    },
    async getPokemon(ids: number[]): Promise<Responses.Pokemon[] | undefined> {
      return await UserClient.getManyPokemon({pokemon_ids: ids}).then((pokemonResponse) => {
        if (pokemonResponse.status === 200) {
          return Promise.resolve(pokemonResponse.data);
        }
      }).catch((err) => {
          return Promise.reject(err);
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
    latestPatch: (state) => state.patches.length > 0 ? state.patches.reduce((a, b) => a.patch_number < b.patch_number ? a : b) : undefined,
    latestPokemon: (state) => state.pokemon.length > 0 ? state.pokemon.reduce((a, b) => a.id < b.id ? a : b) : undefined,
    // currentPatent: (state) => ,
  }
})
