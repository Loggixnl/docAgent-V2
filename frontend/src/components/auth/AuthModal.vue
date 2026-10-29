<template>
  <div 
    v-if="isOpen"
    class="fixed inset-0 z-50 bg-[#0F1424]/40 backdrop-blur-md flex items-center justify-center p-4 overflow-y-auto"
    @click.self="close"
  >
    <div class="w-full max-w-4xl bg-white border border-gray-200 rounded-3xl overflow-hidden shadow-2xl flex flex-col md:grid md:grid-cols-2 relative">
      <button 
        class="absolute top-4 right-4 text-slate-400 hover:text-slate-800 text-2xl transition-all cursor-pointer z-50 w-8 h-8 flex items-center justify-center bg-slate-100 rounded-full hover:bg-slate-200"
        title="Close Modal"
        @click="close"
      >
        &times;
      </button>

      <!-- Left Panel: Branding & Features -->
      <div class="p-8 md:p-12 bg-gradient-to-br from-lightTeal/20 to-bgBase/40 border-r border-gray-200/80 flex flex-col justify-between">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl flex items-center justify-center text-white bg-gradient-to-br from-lightTeal to-darkTeal shadow-md text-xl shrink-0">
            <i class="mdi mdi-shield-text-outline"></i>
          </div>
          <div>
            <h2 class="text-base font-black font-heading text-slate-900 tracking-tight leading-none">DocAgent AI</h2>
            <span class="text-[9px] text-darkTeal font-bold uppercase tracking-wider block mt-0.5">AI SaaS Chatbot Platform</span>
          </div>
        </div>

        <div class="my-8 md:my-12">
          <h3 class="text-2xl md:text-3xl font-extrabold font-heading text-slate-900 leading-tight mb-4">
            Launch your custom <span class="text-darkTeal">AI Chatbot</span> in minutes.
          </h3>
          <p class="text-xs text-slate-600 leading-relaxed mb-6 font-medium">
            Upload your company documents, train your custom agent, and integrate it into your internal portals or public websites with ease.
          </p>

          <div class="space-y-6">
            <div class="flex gap-4">
              <div class="w-9 h-9 rounded-xl bg-lightTeal/10 text-darkTeal flex items-center justify-center text-lg shrink-0">
                <i class="mdi mdi-account-key-outline"></i>
              </div>
              <div>
                <h4 class="text-xs font-bold text-slate-900">Unique Chatbot ID</h4>
                <p class="text-[10px] text-slate-500 mt-0.5 font-medium">Every account gets its own isolated knowledge base and widget integration.</p>
              </div>
            </div>
            <div class="flex gap-4">
              <div class="w-9 h-9 rounded-xl bg-lightTeal/10 text-darkTeal flex items-center justify-center text-lg shrink-0">
                <i class="mdi mdi-cloud-upload-outline"></i>
              </div>
              <div>
                <h4 class="text-xs font-bold text-slate-900">Document Indexer</h4>
                <p class="text-[10px] text-slate-500 mt-0.5 font-medium">Upload PDF, Markdown, and TXT. Retrieve answers directly from the source.</p>
              </div>
            </div>
            <div class="flex gap-4">
              <div class="w-9 h-9 rounded-xl bg-lightTeal/10 text-darkTeal flex items-center justify-center text-lg shrink-0">
                <i class="mdi mdi-code-tags"></i>
              </div>
              <div>
                <h4 class="text-xs font-bold text-slate-900">Zero-Code Embed</h4>
                <p class="text-[10px] text-slate-500 mt-0.5 font-medium">Copy-paste a single script tag to integrate the chatbot anywhere.</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="text-[10px] text-slate-400 font-semibold">
          Secure workspace powered by advanced AI models.
        </div>
      </div>

      <!-- Right Panel: Login / Signup Form -->
      <div class="p-8 md:p-12 flex items-center bg-slate-50/40">
        <div class="w-full">
          <div class="mb-6">
            <h3 class="text-xl font-bold text-slate-900 font-heading">
              {{ isRegister ? "Create an account." : "Let's start a conversation." }}
            </h3>
            <p class="text-xs text-slate-500 mt-1 font-medium">
              {{ isRegister ? "Sign up below to launch your own custom AI chatbot." : "Enter your details below to log in to your dashboard." }}
            </p>
          </div>

          <form @submit.prevent="handleSubmit" class="space-y-4">
            <div v-if="errorMessage" class="p-2.5 rounded-xl bg-red-50 border border-red-200 text-red-600 text-xs font-medium">
              {{ errorMessage }}
            </div>

            <div class="flex flex-col gap-1.5">
              <label class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Email Address</label>
              <div class="relative flex items-center">
                <i class="mdi mdi-email-outline absolute left-4 text-darkTeal text-base"></i>
                <input 
                  v-model="email" 
                  type="email" 
                  placeholder="you@example.com" 
                  class="w-full bg-white border border-gray-300 focus:border-darkTeal focus:ring-1 focus:ring-darkTeal/20 outline-none rounded-xl py-2.5 pl-11 pr-4 text-xs text-slate-900 placeholder-gray-400 transition-all font-medium" 
                  required
                >
              </div>
            </div>

            <div class="flex flex-col gap-1.5">
              <label class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Password</label>
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
              <label class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Confirm Password</label>
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
              <span>{{ loading ? "Processing..." : (isRegister ? "Create Account" : "Login to Dashboard") }}</span>
              <i v-if="!loading" class="mdi mdi-arrow-right text-xs"></i>
            </button>
          </form>

          <div class="mt-6 text-center text-xs text-slate-600">
            <span>{{ isRegister ? "Already have an account?" : "Don't have an account?" }}</span>
            <button 
              type="button" 
              class="text-darkTeal hover:underline ml-1 font-bold cursor-pointer"
              @click="toggleMode"
            >
              {{ isRegister ? "Log in here" : "Create an account" }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuth } from '../../composables/useAuth'

const props = defineProps({
  isOpen: Boolean,
  initialMode: {
    type: String,
    default: 'login'
  }
})

const emit = defineEmits(['close', 'success'])

const { login, register, authMode } = useAuth()

const isRegister = computed(() => authMode.value === 'register')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const errorMessage = ref('')

function toggleMode() {
  authMode.value = authMode.value === 'login' ? 'register' : 'login'
  errorMessage.value = ''
}

function close() {
  errorMessage.value = ''
  emit('close')
}

async function handleSubmit() {
  errorMessage.value = ''
  const trimmedEmail = email.value.trim().toLowerCase()

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(trimmedEmail)) {
    errorMessage.value = 'Please enter a valid email address.'
    return
  }

  if (isRegister.value) {
    if (password.value !== confirmPassword.value) {
      errorMessage.value = 'Passwords do not match!'
      return
    }
    if (password.value.length < 4) {
      errorMessage.value = 'Password must be at least 4 characters long.'
      return
    }
  }

  loading.value = true
  try {
    if (isRegister.value) {
      await register(trimmedEmail, password.value, confirmPassword.value)
    } else {
      await login(trimmedEmail, password.value)
    }
    emit('success')
  } catch (err) {
    errorMessage.value = err.message || 'Authentication failed. Check your inputs.'
  } finally {
    loading.value = false
  }
}
</script>
