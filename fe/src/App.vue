<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import LandingView from '@/components/LandingPage.vue'
</script>

<template>
  <!--  <header>-->
  <!--    <div class="wrapper">-->
  <!--      <LandingView />-->

  <!--            <nav>-->
  <!--              <RouterLink to="/">Home</RouterLink>-->
  <!--              <RouterLink to="/about">About</RouterLink>-->
  <!--            </nav>-->
  <!--    </div>-->
  <!--  </header>-->

  <RouterView />
</template>