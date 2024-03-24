import { apiURL } from '@/clients/core.client'

export function png_proxy(url: string) {
  return `${apiURL}cors-proxy/png/${url}`;
}