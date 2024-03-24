<template>
  <v-app-bar flat>
    <v-container>
      <v-row style="align-items:center; justify-content:space-between">
        <v-col class="nav-container" cols="12" sm="4" md="4">
          <span v-for="nav in navRoutes" :key="nav.id" class="mr-5">
            <a @click="goToRoute(nav.routeName)" :class="nav.routeName == currentRouteName ? 'nav-route selected' : 'nav-route'">
              {{ nav.name }}
            </a>
          </span>
        </v-col>

        <v-col cols="12" sm="4" md="4" style="display: flex; justify-content: center;">
          <a @click="goToRoute(routes.HOME)">
            <div class="logo-container">
              <img style="text-align: right" class="mr-2" height="60" alt="PATCH-EM-ALL Logo" src="../../assets/patchemall.png"/>
              <h1 style="text-align: left" class="ml-2" >PATCH 'EM ALL</h1 >
            </div>
          </a>
        </v-col>

        <v-col class="actions-container" cols="12" sm="4" md="4">
          <v-btn icon="" class="mr-3">
            <v-icon>mdi-cog</v-icon>
            <v-menu activator="parent" :close-on-content-click="false" location="bottom">
              <v-card>
                <v-list>
                  <v-list-item>
                    <v-btn v-if="!theme.global.current.value.dark" dark x-small fab @click="toggleTheme">
                      <v-icon class="mr-3" light>mdi-moon-waxing-crescent</v-icon> Lights Off
                    </v-btn>
                    <v-btn v-else light x-small fab @click="toggleTheme">
                      <v-icon class="mr-3" dark>mdi-white-balance-sunny</v-icon> Lights On
                    </v-btn>
                  </v-list-item>
                </v-list>
              </v-card>
            </v-menu>
          </v-btn>

          <v-btn v-if="showLoginButton" centered @click="openLoginDialog">
            Login <v-icon class="ml-2 mb-1" right color="happy">mdi-login</v-icon>
          </v-btn>
          <span v-else>
            <v-btn @click="goToRoute(routes.PROFILE)">
              <v-icon>mdi-account-tie</v-icon>
            </v-btn>
          </span>
        </v-col>
      </v-row>
    </v-container>
  </v-app-bar>
</template>

<script setup lang="ts">
  import {EventBus, events} from "@/event-bus";
  import {goToRoute} from "@/router"
  import { computed } from 'vue'
  import { userStore } from '@/stores/user'
  import { useRoute } from 'vue-router'
  import routes from '@/router/routes'
  import { useTheme } from 'vuetify'
  import IconBase from '@/components/general/Icons/IconBase.vue'
  import LogoIcon from '@/components/general/Icons/IconLogo.vue'
  import { persistenceStore } from '@/stores/persistence'
  import { showInfoSnackbar } from '@/mixins/snackbar'

  const theme = useTheme();

  const navRoutes = [
    { id: 1, name: "HOME", routeName: routes.HOME },
    { id: 2, name: "PROFILE", routeName: routes.PROFILE }
  ]

  const showLoginButton = computed(() => {
    return !userStore().isLoggedIn;
  })

  const route = useRoute()
  const currentRouteName = computed(() => route.name)

  function openLoginDialog () {
    EventBus.emit(events.OPEN_LOGIN_DIALOG)
  }

  function toggleTheme() {
    theme.global.name.value = theme.global.current.value.dark ? 'light' : 'dark'
    persistenceStore().updateSettings({'theme': theme.global.name.value})
  }
</script>

<style scoped lang="scss">
.logo-text {
  white-space: nowrap;
  width: 100%;
  margin: auto;
  text-align: center;
  color: white;
}

.logo-container {
  display: flex;
  align-items: center;
  flex-wrap: nowrap;
  flex-direction: row;
}

li a {
  text-decoration: none;
  color: inherit;
}

.nav-container {
  text-align: left;
}

.actions-container {
  text-align: right;
}

.nav-route {
  color: darkgray;
  letter-spacing: 1px;
  font-weight: 500;
  font-size: 18px;
  font-family: "Space Grotesk", sans-serif;
}

.nav-route:hover {
  color: gray;
}

.selected {
  color: inherit;
  font-weight: 800;
}

.selected:hover {
  color: inherit;
}

.icon-container {
  text-align: right;
}
</style>