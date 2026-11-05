<template>
  <div
    v-if="isOpen"
    class="fixed inset-0 z-50 bg-[#0F1424]/40 backdrop-blur-md flex items-center justify-center p-4 overflow-y-auto"
    @click.self="close"
  >
    <div class="w-full max-w-4xl bg-white border border-gray-200 rounded-3xl overflow-hidden shadow-2xl flex flex-col md:grid md:grid-cols-2 relative">
      <button
        class="absolute top-4 right-4 text-slate-400 hover:text-slate-800 text-2xl transition-all cursor-pointer z-50 w-8 h-8 flex items-center justify-center bg-slate-100 rounded-full hover:bg-slate-200"
        :title="$t('auth.closeTitle')"
        @click="close"
      >
        &times;
      </button>

      <!-- Left Panel: Branding & Features -->
      <div class="p-8 md:p-12 bg-gradient-to-br from-lightTeal/20 to-bgBase/40 border-r border-gray-200/80 flex flex-col justify-between">
        <div class="flex items-center justify-between gap-3">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl flex items-center justify-center text-white bg-gradient-to-br from-lightTeal to-darkTeal shadow-md text-xl shrink-0">
              <i class="mdi mdi-shield-text-outline"></i>
            </div>
            <div>
              <h2 class="text-base font-black font-heading text-slate-900 tracking-tight leading-none">{{ $t('brand') }}</h2>
              <span class="text-[9px] text-darkTeal font-bold uppercase tracking-wider block mt-0.5">{{ $t('auth.brandTagline') }}</span>
            </div>
          </div>
          <LanguageSwitcher />
        </div>

        <div class="my-8 md:my-12">
          <h3 class="text-2xl md:text-3xl font-extrabold font-heading text-slate-900 leading-tight mb-4">
            {{ $t('auth.brandHeadlineBefore') }} <span class="text-darkTeal">{{ $t('auth.brandHeadlineHighlight') }}</span> {{ $t('auth.brandHeadlineAfter') }}
          </h3>
          <p class="text-xs text-slate-600 leading-relaxed mb-6 font-medium">
            {{ $t('auth.brandBody') }}
          </p>

          <div class="space-y-6">
            <div class="flex gap-4">
              <div class="w-9 h-9 rounded-xl bg-lightTeal/10 text-darkTeal flex items-center justify-center text-lg shrink-0">
                <i class="mdi mdi-account-key-outline"></i>
              </div>
              <div>
                <h4 class="text-xs font-bold text-slate-900">{{ $t('auth.bullet1Title') }}</h4>
                <p class="text-[10px] text-slate-500 mt-0.5 font-medium">{{ $t('auth.bullet1Body') }}</p>
              </div>
            </div>
            <div class="flex gap-4">
              <div class="w-9 h-9 rounded-xl bg-lightTeal/10 text-darkTeal flex items-center justify-center text-lg shrink-0">
                <i class="mdi mdi-cloud-upload-outline"></i>
              </div>
              <div>
                <h4 class="text-xs font-bold text-slate-900">{{ $t('auth.bullet2Title') }}</h4>
                <p class="text-[10px] text-slate-500 mt-0.5 font-medium">{{ $t('auth.bullet2Body') }}</p>
              </div>
            </div>
            <div class="flex gap-4">
              <div class="w-9 h-9 rounded-xl bg-lightTeal/10 text-darkTeal flex items-center justify-center text-lg shrink-0">
                <i class="mdi mdi-code-tags"></i>
              </div>
              <div>
                <h4 class="text-xs font-bold text-slate-900">{{ $t('auth.bullet3Title') }}</h4>
                <p class="text-[10px] text-slate-500 mt-0.5 font-medium">{{ $t('auth.bullet3Body') }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="text-[10px] text-slate-400 font-semibold">
          {{ $t('auth.secureNote') }}
        </div>
      </div>

      <!-- Right Panel: Login / Signup Form -->
      <div class="p-8 md:p-12 flex items-center bg-slate-50/40">
        <div class="w-full">
          <!-- Post-registration: Email verification notice -->
          <div v-if="verificationSent" class="text-center py-4">
            <div class="w-16 h-16 rounded-full bg-lightTeal/20 text-darkTeal flex items-center justify-center text-4xl mx-auto mb-5">
              <i class="mdi mdi-email-check-outline"></i>
            </div>
            <h3 class="text-xl font-bold text-slate-900 font-heading mb-2">{{ $t('auth.checkEmail') }}</h3>
            <p class="text-xs text-slate-600 leading-relaxed font-medium mb-2">
              {{ $t('auth.sentTo') }}
            </p>
            <p class="text-sm font-bold text-darkTeal mb-4">{{ pendingEmail }}</p>
            <p class="text-xs text-slate-500 font-medium mb-6">
              {{ $t('auth.verifyHint') }}
            </p>

            <div v-if="resendMessage" class="p-2.5 rounded-xl bg-green-50 border border-green-200 text-green-700 text-xs font-medium mb-4">
              {{ resendMessage }}
            </div>
            <div v-if="errorMessage" class="p-2.5 rounded-xl bg-red-50 border border-red-200 text-red-600 text-xs font-medium mb-4">
              {{ errorMessage }}
            </div>

            <button
              type="button"
              :disabled="resendLoading"
              class="text-darkTeal hover:underline text-xs font-bold cursor-pointer disabled:opacity-50 mb-6"
              @click="handleResend"
            >
              <i v-if="resendLoading" class="mdi mdi-loading mdi-spin"></i>
              {{ resendLoading ? $t('auth.sending') : $t('auth.resendBtn') }}
            </button>

            <div class="text-xs text-slate-600">
              <button
                type="button"
                class="text-darkTeal hover:underline font-bold cursor-pointer"
                @click="backToLogin"
              >
                {{ $t('auth.backToLogin') }}
              </button>
            </div>
          </div>

          <template v-else>
          <div class="mb-6">
            <h3 class="text-xl font-bold text-slate-900 font-heading">
              {{ isRegister ? $t('auth.createHeading') : $t('auth.loginHeading') }}
            </h3>
            <p class="text-xs text-slate-500 mt-1 font-medium">
              {{ isRegister ? $t('auth.registerSubtitle') : $t('auth.loginSubtitle') }}
            </p>
          </div>

          <form @submit.prevent="handleSubmit" class="space-y-4">
            <div v-if="errorMessage" class="p-2.5 rounded-xl bg-red-50 border border-red-200 text-red-600 text-xs font-medium">
              {{ errorMessage }}
              <button
                v-if="showResendOnLoginError"
                type="button"
                class="block mt-1.5 text-darkTeal hover:underline font-bold cursor-pointer"
                :disabled="resendLoading"
                @click="handleResendFromLogin"
              >
                <i v-if="resendLoading" class="mdi mdi-loading mdi-spin"></i>
                {{ resendLoading ? $t('auth.sending') : $t('auth.resendBtn') }}
              </button>
            </div>

            <div v-if="resendMessage" class="p-2.5 rounded-xl bg-green-50 border border-green-200 text-green-700 text-xs font-medium">
              {{ resendMessage }}
            </div>

            <div v-if="isRegister" class="flex flex-col gap-1.5">
              <label class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">{{ $t('auth.firstName') }}</label>
              <div class="relative flex items-center">
                <i class="mdi mdi-account-outline absolute left-4 text-darkTeal text-base"></i>
                <input
                  v-model="firstName"
                  type="text"
                  :placeholder="$t('auth.firstNamePlaceholder')"
                  class="w-full bg-white border border-gray-300 focus:border-darkTeal focus:ring-1 focus:ring-darkTeal/20 outline-none rounded-xl py-2.5 pl-11 pr-4 text-xs text-slate-900 placeholder-gray-400 transition-all font-medium"
                  :required="isRegister"
                >
              </div>
            </div>

            <div class="flex flex-col gap-1.5">
              <label class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">{{ $t('auth.emailLabel') }}</label>
              <div class="relative flex items-center">
                <i class="mdi mdi-email-outline absolute left-4 text-darkTeal text-base"></i>
                <input
                  v-model="email"
                  type="email"
                  :placeholder="$t('auth.emailPlaceholder')"
                  class="w-full bg-white border border-gray-300 focus:border-darkTeal focus:ring-1 focus:ring-darkTeal/20 outline-none rounded-xl py-2.5 pl-11 pr-4 text-xs text-slate-900 placeholder-gray-400 transition-all font-medium"
                  required
                >
              </div>
            </div>

            <div class="flex flex-col gap-1.5">
              <label class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">{{ $t('auth.password') }}</label>
              <div class="relative flex items-center">
                <i class="mdi mdi-lock-outline absolute left-4 text-darkTeal text-base"></i>
                <input
                  v-model="password"
                  type="password"
                  placeholder="••••••••"
                  class="w-full bg-white border border-gray-300 focus:border-darkTeal focus:ring-1 focus:ring-darkTeal/20 outline-none rounded-xl py-2.5 pl-11 pr-4 text-xs text-slate-900 placeholder-gray-400 transition-all font-medium"
                  required
                >
              </div>
            </div>

            <div v-if="isRegister" class="flex flex-col gap-1.5">
              <label class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">{{ $t('auth.confirmPassword') }}</label>
              <div class="relative flex items-center">
                <i class="mdi mdi-lock-check-outline absolute left-4 text-darkTeal text-base"></i>
                <input
                  v-model="confirmPassword"
                  type="password"
                  placeholder="••••••••"
                  class="w-full bg-white border border-gray-300 focus:border-darkTeal focus:ring-1 focus:ring-darkTeal/20 outline-none rounded-xl py-2.5 pl-11 pr-4 text-xs text-slate-900 placeholder-gray-400 transition-all font-medium"
                  :required="isRegister"
                >
              </div>
            </div>

            <button
              type="submit"
              :disabled="loading"
              class="w-full py-3 rounded-full bg-darkTeal text-white font-bold text-xs shadow-md shadow-darkTeal/20 hover:bg-darkTeal/90 hover:scale-[1.01] active:scale-[0.99] transition-all flex items-center justify-center gap-2 mt-6 cursor-pointer disabled:opacity-50"
            >
              <i v-if="loading" class="mdi mdi-loading mdi-spin"></i>
              <span>{{ loading ? $t('auth.processing') : (isRegister ? $t('auth.submitRegister') : $t('auth.submitLogin')) }}</span>
              <i v-if="!loading" class="mdi mdi-arrow-right text-xs"></i>
            </button>
          </form>

          <div class="mt-6 text-center text-xs text-slate-600">
            <span>{{ isRegister ? $t('auth.haveAccount') : $t('auth.noAccount') }}</span>
            <button
              type="button"
              class="text-darkTeal hover:underline ml-1 font-bold cursor-pointer"
              @click="toggleMode"
            >
              {{ isRegister ? $t('auth.loginLink') : $t('auth.registerLink') }}
            </button>
          </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuth } from '../../composables/useAuth'
import { useI18n } from 'vue-i18n'
import LanguageSwitcher from '../common/LanguageSwitcher.vue'

const { t } = useI18n()

const props = defineProps({
  isOpen: Boolean,
  initialMode: {
    type: String,
    default: 'login'
  }
})

const emit = defineEmits(['close', 'success'])

const { login, register, resendVerification, authMode } = useAuth()

const isRegister = computed(() => authMode.value === 'register')
const email = ref('')
const firstName = ref('')
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const errorMessage = ref('')

// Email verification state
const verificationSent = ref(false)
const pendingEmail = ref('')
const resendLoading = ref(false)
const resendMessage = ref('')
const showResendOnLoginError = ref(false)

function toggleMode() {
  authMode.value = authMode.value === 'login' ? 'register' : 'login'
  errorMessage.value = ''
  resendMessage.value = ''
  showResendOnLoginError.value = false
}

function close() {
  errorMessage.value = ''
  resendMessage.value = ''
  showResendOnLoginError.value = false
  verificationSent.value = false
  emit('close')
}

function backToLogin() {
  verificationSent.value = false
  resendMessage.value = ''
  errorMessage.value = ''
  authMode.value = 'login'
}

async function handleSubmit() {
  errorMessage.value = ''
  resendMessage.value = ''
  showResendOnLoginError.value = false
  const trimmedEmail = email.value.trim().toLowerCase()

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(trimmedEmail)) {
    errorMessage.value = t('auth.errInvalidEmail')
    return
  }

  if (isRegister.value) {
    if (!firstName.value.trim()) {
      errorMessage.value = t('auth.errFirstName')
      return
    }
    if (password.value !== confirmPassword.value) {
      errorMessage.value = t('auth.errMismatch')
      return
    }
    if (password.value.length < 4) {
      errorMessage.value = t('auth.errPasswordShort')
      return
    }
  }

  loading.value = true
  try {
    if (isRegister.value) {
      await register(firstName.value.trim(), trimmedEmail, password.value, confirmPassword.value)
      // Show the "check your email" screen instead of logging in
      pendingEmail.value = trimmedEmail
      verificationSent.value = true
    } else {
      await login(trimmedEmail, password.value)
      emit('success')
    }
  } catch (err) {
    errorMessage.value = err.message || t('auth.errAuthFailed')
    // 403 from the login endpoint means the email is not verified yet
    if (err.status === 403) {
      showResendOnLoginError.value = true
    }
  } finally {
    loading.value = false
  }
}

async function handleResend() {
  resendMessage.value = ''
  errorMessage.value = ''
  resendLoading.value = true
  try {
    const data = await resendVerification(pendingEmail.value)
    resendMessage.value = data.message || t('auth.resendSuccess')
  } catch (err) {
    errorMessage.value = err.message || t('auth.errResendFailed')
  } finally {
    resendLoading.value = false
  }
}

async function handleResendFromLogin() {
  resendMessage.value = ''
  errorMessage.value = ''
  resendLoading.value = true
  try {
    const data = await resendVerification(email.value.trim().toLowerCase())
    resendMessage.value = data.message || t('auth.resendSuccess')
  } catch (err) {
    errorMessage.value = err.message || t('auth.errResendFailed')
  } finally {
    resendLoading.value = false
  }
}
</script>
