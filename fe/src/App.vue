<template>
  <VApp>
    <VMain>
      <AuthHandler />
      <RouterView v-slot="{ Component }">
        <Transition
          :name="transition"
          :mode="transitionMode"
          :enter-active-class="transitionEnterActiveClass"
        >
          <component :is="Component" />
        </Transition>
      </RouterView>
      <SnackBar />
    </VMain>
  </VApp>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import AuthHandler from '@/components/auth/AuthHandler.vue'
import SnackBar from '@/components/general/SnackBar.vue'

import { onMounted } from 'vue'
import router from '@/router'

let transition: string
let transitionMode: string = 'out-in'
let transitionEnterActiveClass: string = ''

onMounted(() => {
  router.beforeEach((to, from, next) => {
    transition = to.meta.transition || from.meta.transition || 'fade'

    if (transition === 'slide') {
      const toDepth = to.path.split('/').length
      const fromDepth = from.path.split('/').length
      transition = toDepth < fromDepth ? 'slide-right' : 'slide-left'
    }

    transitionEnterActiveClass = `${transition}-enter-active`

    if (to.meta.transition === 'zoom') {
      transitionMode = 'in-out'
      transitionEnterActiveClass = 'zoom-enter-active'
      document.body.style.overflow = 'hidden'
    }

    if (from.meta.transition === 'zoom') {
      transitionMode = ''
      transitionEnterActiveClass = ''
      document.body.style.overflow = ''
    }
    next()
  })
})
</script>

<style lang="scss">
@import url('https://fonts.googleapis.com/css2?family=Overpass+Mono:wght@300;400;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Overpass:ital,wght@0,100;0,200;0,300;0,400;0,600;0,700;1,100;1,200;1,300;1,400;1,600&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&display=swap');
$body-font: 'Overpass';
$title-font: 'Space Grotesk';

.v-application {
  font-family: $body-font, sans-serif !important;
  .title {
    font-family: $title-font, monospace !important;
  }

  @media (min-width: 960px) {
    .container {
      max-width: 1000px;
    }
  }

  @media (min-width: 1264px) {
    .container {
      max-width: 1100px;
    }
  }

  @media (min-width: 1904px) {
    .container {
      max-width: 1200px;
    }
  }

  h1 {
    font-family: $title-font, monospace !important;
    font-size: 1.8em;
  }

  h2 {
    font-family: $title-font, monospace !important;
    font-size: 1.4em;
    font-weight: 800;
  }

  p {
    font-size: 0.8em;
  }

  .number-text-style {
    font-family: $title-font, monospace !important;
  }

  .symbol-text-style {
    font-family: $title-font, monospace !important;
  }

  .small-font {
    font-size: 12px;
  }
  .happy-text {
    color: var(--v-happy-base);
  }
  .sad-text {
    color: var(--v-sad-base);
  }
}

.fade-enter-active,
.fade-leave-active {
  transition-duration: 0.3s;
  transition-property: height, opacity;
  transition-timing-function: ease;
  overflow: hidden;
}

.fade-enter,
.fade-leave-active {
  opacity: 0;
}

.slide-left-enter-active,
.slide-left-leave-active,
.slide-right-enter-active,
.slide-right-leave-active {
  transition-duration: 0.5s;
  transition-property: height, opacity, transform;
  transition-timing-function: cubic-bezier(0.55, 0, 0.1, 1);
  overflow: hidden;
}

.slide-left-enter,
.slide-right-leave-active {
  opacity: 0;
  transform: translate(2em, 0);
}

.slide-left-leave-active,
.slide-right-enter {
  opacity: 0;
  transform: translate(-2em, 0);
}

.zoom-enter-active,
.zoom-leave-active {
  animation-duration: 0.5s;
  animation-fill-mode: both;
  animation-name: zoom;
}

.zoom-leave-active {
  animation-direction: reverse;
}

@keyframes zoom {
  from {
    opacity: 0;
    transform: scale3d(0.3, 0.3, 0.3);
  }

  100% {
    opacity: 1;
  }
}
</style>
