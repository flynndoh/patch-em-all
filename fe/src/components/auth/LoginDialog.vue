<template>
  <v-dialog :model-value="loginDialogOpen" width="500" persistent>
    <v-card style="border-radius:40px 10px;" class="pa-5">
      <v-card-title class="heading">
        <h2 class="pt-3">Login</h2>
        <v-btn @click="closeDialog" class="bg-red-lighten-1">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-card-subtitle class="pt-3">
        <h3>Welcome back</h3>
      </v-card-subtitle>

      <v-progress-linear
        indeterminate
        class="mt-5"
        color="happy"
        v-if="loginProcessing"
      ></v-progress-linear>

      <v-card-text class="mt-5">
        <v-form ref="form_login">
          <v-text-field
            ref="input_email"
            v-model="email"
            prepend-icon="mdi-account"
            label="Email"
            :rules="rules.email"
            v-on:keyup.enter="goToPasswordInput"
          ></v-text-field>
          <v-text-field
            ref="input_password"
            v-model="password"
            prepend-icon="mdi-lock"
            label="4 Digit Pin"
            :rules="rules.pinCode"
            type="password"
            v-on:keyup.enter="login"
          ></v-text-field>
        </v-form>
      </v-card-text>

      <v-alert icon="$error" :model-value="loginFailure" color="error">Incorrect login credentials.</v-alert>

      <v-divider></v-divider>

      <v-card-actions>
        <a class="btn-shine" @click="switchDialogCb">i'm new here</a>
        <v-spacer></v-spacer>
        <v-btn color="happy" class="btn-login" centered @click="login">
          Login <v-icon right color="happy">mdi-check</v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { userStore } from '@/stores/user'
import rules from '@/common/form-rules'
import { EventBus, events } from '@/event-bus'
import { ref } from 'vue'
import { VForm, VTextField } from 'vuetify/components'

defineProps({
  loginDialogOpen: { required: true },
  switchDialogCb: { required: true }
})

let loginFailure = ref(false)
let loginProcessing = ref(false)
const email = ref("");
const password = ref("");

const form_login = ref(VForm)
const input_password = ref(VTextField)

function closeDialog() {
  EventBus.emit(events.CLOSE_LOGIN_DIALOG)
}

async function login() {
  if (!form_login.value.isValid) {
    return
  }

  loginFailure.value = false
  loginProcessing.value = true
  await userStore()
    .login(email.value, password.value)
    .then(() => {
      email.value = ''
      password.value = ''
      form_login.value.resetValidation()
      EventBus.emit(events.CLIENT_LOGGED_IN)
      closeDialog();
    })
    .catch(() => (loginFailure.value = true))
    .finally(() => (loginProcessing.value = false))
}

function goToPasswordInput() {
  input_password.value.focus()
}
</script>

<style scoped lang="scss">
.heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.btn-login {
  margin-right: 10px;
}

.btn-shine {
  padding-left: 48px;
  margin-left: -48px; // negative margin to keep padding for animation
  background: linear-gradient(to right, gray 0, gold 10%, gray 20%) 0;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shine 3s infinite ease-in-out;
  animation-fill-mode: forwards;
  -webkit-text-size-adjust: none;
  font-weight: 600;
  font-size: 16px;
  text-decoration: none;
  white-space: nowrap;
  font-style: italic;
}

@keyframes shine {
  0% {
    background-position: 0;
  }
  50% {
    background-position: 150px;
  }
  100% {
    background-position: 0;
  }
}
</style>
