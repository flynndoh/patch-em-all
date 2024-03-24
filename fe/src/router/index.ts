import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import HomePage from '@/pages/HomePage.vue'
import routes from '@/router/routes'
import { userStore } from '@/stores/user'
import AboutPage from '@/pages/AboutPage.vue'
import PrivacyPolicyPage from '@/pages/PrivacyPolicyPage.vue'
import ProfilePage from '@/pages/ProfilePage.vue'
import NotFoundPage from '@/pages/NotFoundPage.vue'

const tryToFetchMe = async (to, from, next: Function) => {
  try {
    if (!userStore().isLoggedIn) {
      await userStore().refreshMe().catch(() => {
        return next();
      })
    }
    if (userStore().isLoggedIn) {
      await userStore().refreshMyPatches()
      await userStore().refreshMyPokemon()
    }

  } catch (e) {
    await userStore().logout()
  }
  return next();
};

const routeRecords: RouteRecordRaw[] = [
  {
    path: '/',
    name: routes.HOME,
    component: HomePage,
    meta: { transition: 'slide-right' },
    beforeEnter: tryToFetchMe,
  },
  {
    path: '/profile',
    name: routes.PROFILE,
    component: ProfilePage,
    meta: { transition: 'slide-left' },
  },
  {
    path: '/about',
    name: routes.ABOUT,
    component: AboutPage,
    meta: { transition: 'slide-left' },
  },
  {
    path: '/privacy-policy',
    name: routes.PRIVACY_POLICY,
    component: PrivacyPolicyPage,
    meta: { transition: 'slide-left' },
  },
  // Default route, after checking all other routes
  {
    path: '/:pathMatch(.*)*',
    name: routes.NOT_FOUND,
    component: NotFoundPage,
    meta: { transition: 'fade' },
  },
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
