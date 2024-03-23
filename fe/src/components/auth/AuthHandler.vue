<template>
  <div>
    <LoginDialog :loginDialogOpen="loginDialogOpen" :switchDialogCb="switchDialog" />
    <RegisterDialog :registerDialogOpen="registerDialogOpen" :switchDialogCb="switchDialog"
    />
  </div>
</template>

<script setup lang="ts">
import { EventBus, events } from '@/event-bus';
import RegisterDialog from '@/components/auth/RegisterDialog.vue';
import LoginDialog from '@/components/auth/LoginDialog.vue';
import { onMounted, ref } from 'vue';

const loginDialogOpen = ref(false);
const registerDialogOpen = ref(false);

onMounted(() => {
  EventBus.on(events.OPEN_LOGIN_DIALOG, openLoginDialog);
  EventBus.on(events.CLOSE_LOGIN_DIALOG, closeLoginDialog);
  EventBus.on(events.OPEN_REGISTER_DIALOG, openRegisterDialog);
  EventBus.on(events.CLOSE_REGISTER_DIALOG, closeRegisterDialog);
})

function openLoginDialog() {
  loginDialogOpen.value = true;
}

function closeLoginDialog() {
  loginDialogOpen.value = false;
}

function openRegisterDialog() {
  registerDialogOpen.value = true;
}

function closeRegisterDialog() {
  registerDialogOpen.value = false;
}

function switchDialog() {
  loginDialogOpen.value = !loginDialogOpen.value;
  registerDialogOpen.value = !registerDialogOpen.value;
}
</script>

<style scoped></style>
