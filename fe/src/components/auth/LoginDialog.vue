<template>
  <v-dialog :model-value="loginDialogOpen" width="500" persistent>
    <v-card shaped>
      <v-card-title class="secondary-inverted">
        <h2>Login</h2>
        <v-spacer />
        <v-btn @click="closeDialog">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-card-subtitle class="secondary-inverted pt-3">
        <h3>Welcome back</h3>
      </v-card-subtitle>

      <v-progress-linear
        indeterminate
        color="yellow darken-2"
        v-if="loginProcessing"
      ></v-progress-linear>

      <v-card-text class="mt-5">
        <v-form ref="form_login">
          <v-text-field
            ref="input_email"
            v-model="email"
            prepend-icon="mdi-account"
            label="Email"
            :rules="rules.required"
            v-on:keyup.enter="goToPasswordInput"
          ></v-text-field>
          <v-text-field
            ref="input_password"
            v-model="password"
            prepend-icon="mdi-lock"
            label="Password"
            :rules="rules.required"
            type="password"
            v-on:keyup.enter="login"
          ></v-text-field>
        </v-form>
      </v-card-text>

      <v-alert :value="loginAlert" color="error">Incorrect login credentials.</v-alert>

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

let loginAlert: boolean = false
let loginProcessing: boolean = false
const email = ref("");
const password = ref("");

const form_login = ref(VForm)
const input_password = ref(VTextField)

function closeDialog() {
  EventBus.emit(events.CLOSE_LOGIN_DIALOG)
}

function login() {
  if (!form_login.value.validate()) {
    return
  }

  loginAlert = false
  loginProcessing = true
  userStore()
    .login(email.value, password.value)
    .then(() => {
      email.value = ''
      password.value = ''
      form_login.value.resetValidation()
      EventBus.emit(events.CLIENT_LOGGED_IN)
      closeDialog();
    })
    .catch(() => (loginAlert = true))
    .finally(() => (loginProcessing = false))
}

function goToPasswordInput() {
  input_password.value.focus()
}
</script>

<style scoped lang="scss">
.btn-login {
  margin-right: 10px;
}

.btn-shine {
  padding: 0 48px;
  margin: -28px; // negative margin to keep padding for animation
  background: linear-gradient(to right, gray 0, gold 10%, gray 20%) 0;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shine 3s infinite linear;
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
  60% {
    background-position: 180px;
  }
  100% {
    background-position: 180px;
  }
}
</style>
