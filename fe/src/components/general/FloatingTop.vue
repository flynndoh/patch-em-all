<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <v-app-bar app flat dense>
    <v-container>
      <v-row style="align-items:center; justify-content:space-between">
        <v-col class="nav-container" cols="7" sm="6" md="5">
          <span v-for="nav in navRoutes" :key="nav.id" class="mr-5">
            <a @click="goToRoute(nav.routeName)" :class="nav.routeName == currentRouteName ? 'nav-route selected' : 'nav-route'">
              {{ nav.name }}
            </a>
          </span>
        </v-col>

        <v-col class="logo-container" cols="1" sm="1" md="2">
          <a @click="goToRoute(routes.HOME)">
            <v-container pa-0 ma-0 text-center>
              <img v-if="$vuetify.theme.dark" style="height: 25px" alt="STOCKSLIP Logo" src="../../assets/stockslip-alt-white.png">
              <img v-else style="height: 25px" alt="STOCKSLIP Logo" src="../../assets/stockslip-alt-black.png">
            </v-container>
          </a>
        </v-col>

        <v-col class="icon-container pa-0" cols="3" sm="5" md="5">
          <span>
            <v-menu :close-on-content-click="false" :nudge-width="100" offset-y>
              <template v-slot:activator="{ on, attrs }">
                <v-btn v-bind="attrs" v-on="on">
                  <v-icon>mdi-cog</v-icon>
                </v-btn>
              </template>

              <v-card>
                <v-list>
                  <v-list-item>
                    <v-btn circle v-if="!theme.global.current.value.dark" dark x-small fab @click="toggleTheme">
                      <v-icon class="mr-1" light>mdi-moon-waxing-crescent</v-icon>
                    </v-btn>
                    <v-btn circle v-else light x-small fab @click="toggleTheme">
                      <v-icon dark>mdi-white-balance-sunny</v-icon>
                    </v-btn>
                  </v-list-item>
                </v-list>
              </v-card>
            </v-menu>

            <v-btn v-if="showLoginButton" centered @click="openLoginDialog">
              Login <v-icon right color="happy">mdi-login</v-icon>
            </v-btn>

            <span v-else>
              <v-btn @click="goToRoute(routes.PROFILE)">
                <v-icon>mdi-account-tie</v-icon>
              </v-btn>
            </span>
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
</script>

<style scoped>
  li a {
    text-decoration: none;
    color: inherit;
  }

  .nav-container {
    text-align: left;
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

  .logo-container {
    text-align: center;
    align-self: flex-end;
    padding-top: 20px;
  }

  .icon-container {
    text-align: right;
  }
</style>