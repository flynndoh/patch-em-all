import { apiURL } from '@/clients/core.client'

export function pngProxy(url: string) {
  return `${apiURL}cors-proxy/png/${url}`;
}