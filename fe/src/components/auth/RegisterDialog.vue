<template>
  <v-dialog :model-value="registerDialogOpen" width="500" persistent>
    <v-card style="border-radius:40px 10px;" class="pa-5">
      <v-card-title class="heading">
        <h2 class="pt-3">Register</h2>
        <v-btn @click="closeDialog" class="bg-red-lighten-1">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>

      <v-card-subtitle class="pt-3">
        <h3>
          Let's get you started
        </h3>
      </v-card-subtitle>

      <v-progress-linear
        indeterminate
        class="mt-5"
        color="happy"
        v-if="registerProcessing"
      ></v-progress-linear>

      <v-card-text class="mt-5">
        <v-form ref="form_register">
          <v-row>
            <v-col>
              <v-text-field
                ref="input_first_name"
                v-model="firstName"
                prepend-icon="mdi-account"
                label="First Name"
                :rules="rules.required"
                v-on:keyup.enter="goToLastNameInput"
              ></v-text-field>
            </v-col>
            <v-col>
              <v-text-field
                ref="input_last_name"
                v-model="lastName"
                label="Last Name"
                :rules="rules.required"
                v-on:keyup.enter="goToEmailInput"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-text-field
            ref="input_email"
            v-model="email"
            prepend-icon="mdi-email"
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
            v-on:keyup.enter="register"
          ></v-text-field>
        </v-form>
      </v-card-text>

      <v-alert icon="$error" :model-value="registerFailureMessage.length > 0" color="error">Registration failed.
        {{ registerFailureMessage }}</v-alert>

      <v-divider></v-divider>

      <v-card-actions>
        <a class="btn-shine" @click="switchDialogCb">i'm not new here</a>
        <v-spacer></v-spacer>
        <v-btn color="happy" class="btn-register" centered @click="register">
          Register <v-icon right color="happy">mdi-check</v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import rules from "@/common/form-rules";
import {EventBus, events} from "@/event-bus";
import { userStore } from '@/stores/user'
import { ref } from 'vue'
import { VForm, VTextField } from 'vuetify/components'

defineProps({
  registerDialogOpen: {required: true},
  switchDialogCb: {required: true}
});

const registerFailureMessage = ref("");
const registerProcessing = ref(false);
const firstName = ref("");
const lastName = ref("");
const email = ref("");
const password = ref("");

const form_register = ref(VForm)
const input_last_name = ref(VTextField)
const input_email = ref(VTextField)
const input_password = ref(VTextField)

function closeDialog() {
  EventBus.emit(events.CLOSE_REGISTER_DIALOG);
}

async function register() {
  if (!form_register.value.isValid) {
    return
  }

  registerFailureMessage.value = '';
  registerProcessing.value = true;
  await userStore().registerAndLogin(firstName.value, lastName.value, email.value, password.value)
    .then(() => {
      firstName.value = "";
      lastName.value = "";
      email.value = "";
      password.value = "";
      form_register.value.resetValidation();
      EventBus.emit(events.CLIENT_LOGGED_IN);
      closeDialog();
    })
    .catch((err) => {
      registerFailureMessage.value = err;
    })
    .finally(() => registerProcessing.value = false);
}
function goToLastNameInput() {
  input_last_name.value.focus();
}
function goToEmailInput() {
  input_email.value.focus();
}
function goToPasswordInput() {
  input_password.value.focus();
}
</script>

<style scoped lang="scss">
.heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.btn-register {
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
