import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import routes from '@/router/routes'

const routeRecords: RouteRecordRaw[] = [
  {
    path: '/',
    name: routes.HOME,
    component: HomeView,
    meta: { transition: 'slide-left' }
  }
  // {
  //   path: '/about',
  //   name: 'about',
  //   component: HomeView,
  //   meta: { transition: 'slide-left' },
  // }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routeRecords
})

function getRoutePathFromName(routeName: string): string | null {
  const matchingRecords: RouteRecordRaw[] = routeRecords.filter((route) => route.name === routeName)
  if (matchingRecords.length != 1) return null
  return matchingRecords[0].path
}

const goToRoute = (routeName: string) => {
  const route: string | null = getRoutePathFromName(routeName)
  if (route == null) {
    throw new Error(`No official route for navigation request: '${routeName}'`)
  }

  if (router.currentRoute.value.fullPath !== route) {
    return router.push(route)
  }
}

export { goToRoute }

export default router
