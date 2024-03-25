import { type AxiosResponse } from 'axios'
import CoreClient from './core.client'

export interface UserApi {
  getMe(): Promise<AxiosResponse<Responses.User>>
  getAllUsers(): Promise<AxiosResponse<Responses.User[]>>
  getMyPatches(): Promise<AxiosResponse<Responses.Patches>>
  getPatchesForUser(id: string): Promise<AxiosResponse<Responses.Patches>>
  getPokemon(id: number): Promise<AxiosResponse<Responses.Pokemon>>
  getManyPokemon(payload: Requests.GetPokemon): Promise<AxiosResponse<Responses.Pokemon[]>>
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

  interface Patches {
    patches: Patch[],
  }

  interface Flight {
    id: number,
    name: string,
    timestamp: Date
  }

  interface Patch {
    id: string,
    patch_number: number,
    flight: Flight,
    image: string
    thumbnail: string
  }

  interface Pokemon {
    id: number
    name: string
    sprite: string
    image: string
  }
}

export declare namespace Requests {
  interface GetPokemon {
    pokemon_ids: number[]
  }
}

class UserClient implements UserApi {
  async getMe(): Promise<AxiosResponse<Responses.User>> {
    return CoreClient.client.get<Responses.User>('/users/me')
  }

  async getAllUsers(): Promise<AxiosResponse<Responses.User[]>> {
    return CoreClient.client.get<Responses.User[]>('/users')
  }

  async getMyPatches(): Promise<AxiosResponse<Responses.Patches>> {
    return CoreClient.client.get<Responses.Patches>('/users/me/patches')
  }

  async getPatchesForUser(id: string): Promise<AxiosResponse<Responses.Patches>> {
    return CoreClient.client.get<Responses.Patches>(`/users/${id}/patches`)
  }

  async getPokemon(id: number): Promise<AxiosResponse<Responses.Pokemon>> {
    return CoreClient.client.get<Responses.Pokemon>(`/pokemon/${id}`)
  }

  async getManyPokemon(payload: Requests.GetPokemon): Promise<AxiosResponse<Responses.Pokemon[]>> {
    return CoreClient.client.post<Responses.Pokemon[]>('/pokemon', payload)
  }
}

export default new UserClient()
