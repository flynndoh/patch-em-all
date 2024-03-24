<template>
  <v-footer class="footer" variant="outlined" color="transparent">
    <v-container class="py-0">
      <v-row align="center" justify="center">
        <v-divider class="py-3"/>
        <v-row align="center" justify="center">
          <v-col class="pa-0 ma-=0">
            <v-container class="py-0">
              <div class="logo-container">
                <img style="text-align: right" class="mr-2" height="100" alt="PATCH-EM-ALL Logo" src="../../assets/patchemall.png"/>
                <h1 style="text-align: left" class="ml-2" >PATCH 'EM ALL</h1 >
              </div>
            </v-container>
          </v-col>

          <v-spacer/>

          <v-btn
            v-for="link in links"
            :key="link.routeName"
            variant="plain"
            @click="goToRoute(link.routeName)"
          >{{ link.name }}</v-btn>
        </v-row>
      </v-row>
    </v-container>
  </v-footer>
</template>

<script setup lang="ts">
import { goToRoute } from "@/router"
import routes from '@/router/routes'

const links = [
  {name: 'About', routeName: routes.ABOUT},
  {name: 'Privacy Policy', routeName: routes.PRIVACY_POLICY},
];
</script>

<style scoped>
.footer {
  bottom: 0;
  position: absolute;
  width: 100%;
  margin-bottom: 40px;
}

.logo-container {
  display: flex;
  align-items: center;
}
</style>