<template>
  <div class="min-h-screen flex flex-col font-sans text-slate-800 bg-bgBase antialiased">
    <!-- LANDING VIEW (When Unauthenticated) -->
    <div v-if="!isAuthenticated" class="flex-grow flex flex-col">
      <LandingNav 
        @login="openAuthModal('login')"
        @register="openAuthModal('register')"
      />
      
      <main class="flex-grow flex flex-col">
        <LandingHero @register="openAuthModal('register')" />
        <LandingFeatures />
        <LandingHowItWorks />
        <LandingPricing @selectPlan="openAuthModal('register')" />
      </main>

      <LandingFooter />
    </div>

    <!-- MAIN APP WORKSPACE VIEW (When Authenticated) -->
    <div v-else class="w-screen h-screen flex p-2 sm:p-4 gap-2 sm:gap-4 overflow-hidden text-slate-800 bg-bgBase relative">
      <!-- Mobile Drawer Backdrop Overlay -->
      <div 
        v-if="isMobileSidebarOpen"
        class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-40 lg:hidden transition-opacity"
        @click="isMobileSidebarOpen = false"
      ></div>

      <!-- Left Sidebar: Session & Document Manager (Off-canvas on mobile, fixed side-panel on lg+) -->
      <div 
        class="fixed inset-y-0 left-0 z-50 w-[300px] sm:w-[340px] p-2 sm:p-4 transform transition-transform duration-300 ease-in-out lg:static lg:transform-none lg:p-0 lg:z-auto lg:w-[320px] lg:shrink-0 h-full"
        :class="isMobileSidebarOpen ? 'translate-x-0 shadow-2xl' : '-translate-x-full lg:translate-x-0'"
      >
        <Sidebar 
          :is-dashboard-view="currentView === 'admin'"
          @viewAnalysis="handleViewAnalysis"
          @firstUploadComplete="handleFirstUpload"
          @openSettings="isSettingsModalOpen = true"
          @closeMobile="isMobileSidebarOpen = false"
          @toggleDashboard="handleToggleDashboard"
          @newChat="handleNewChat"
        />
      </div>

      <!-- Main Content Area: Chat Workspace or Admin Dashboard -->
      <main class="flex-grow flex flex-col bg-white border border-gray-200 rounded-2xl overflow-hidden shadow-sm h-full min-w-0">
        <!-- Global Top Header -->
        <ChatHeader 
          :is-dashboard-view="currentView === 'admin'"
          @openWidget="isWidgetModalOpen = true"
          @openSettings="isSettingsModalOpen = true"
          @logout="handleUserLogout"
          @toggleSidebar="isMobileSidebarOpen = !isMobileSidebarOpen"
          @toggleView="handleToggleDashboard"
          @newChat="handleNewChat"
        />

        <!-- CHAT VIEW -->
        <template v-if="currentView === 'chat'">
          <ChatWindow 
            @applySuggestion="handleApplySuggestion"
          />

          <ChatInput 
            ref="chatInputRef"
            @send="handleSendMessage"
          />
        </template>

        <!-- ADMIN DASHBOARD VIEW -->
        <template v-else>
          <AdminDashboard 
            @backToChat="currentView = 'chat'"
          />
        </template>
      </main>
    </div>

    <!-- MODALS -->
    <AuthModal 
      :is-open="isAuthModalOpen"
      @close="closeAuthModal"
      @success="handleAuthSuccess"
    />

    <SettingsModal 
      :is-open="isSettingsModalOpen"
      @close="isSettingsModalOpen = false"
    />

    <AnalysisModal 
      :is-open="analysisModal.isOpen"
      :filename="analysisModal.filename"
      :content="analysisModal.content"
      :is-loading="analysisModal.isLoading"
      @close="closeAnalysis"
    />

    <WidgetModal 
      :is-open="isWidgetModalOpen"
      @close="isWidgetModalOpen = false"
    />

    <!-- EMAIL VERIFICATION RESULT OVERLAY -->
    <div v-if="verifyResult" class="fixed inset-0 z-[100] bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
      <div class="bg-white rounded-3xl shadow-2xl max-w-md w-full p-8 text-center">
        <template v-if="verifyResult.loading">
          <i class="mdi mdi-loading mdi-spin text-4xl text-darkTeal"></i>
          <p class="mt-4 text-sm font-semibold text-slate-600">{{ $t('verify.processing') }}</p>
        </template>
        <template v-else>
          <div
            class="w-16 h-16 rounded-full mx-auto flex items-center justify-center text-4xl"
            :class="verifyResult.success ? 'bg-teal-50 text-teal-600' : 'bg-red-50 text-red-500'"
          >
            <i :class="verifyResult.success ? 'mdi mdi-email-check-outline' : 'mdi mdi-alert-circle-outline'"></i>
          </div>
          <h2 class="text-lg font-bold mt-4 text-slate-800">
            {{ verifyResult.success ? $t('verify.successHeading') : $t('verify.failureHeading') }}
          </h2>
          <p class="text-sm text-slate-600 mt-2">{{ verifyResult.message }}</p>
          <button
            v-if="verifyResult.success"
            class="mt-6 px-6 py-2.5 rounded-full bg-darkTeal text-white text-sm font-semibold hover:bg-opacity-90 transition"
            @click="closeVerifyResult(true)"
          >
            {{ $t('verify.goToLogin') }}
          </button>
          <button
            v-else
            class="mt-6 px-6 py-2.5 rounded-full border border-slate-300 text-slate-700 text-sm font-semibold hover:bg-slate-50 transition"
            @click="closeVerifyResult(false)"
          >
            {{ $t('common.close') }}
          </button>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import LandingNav from './components/landing/LandingNav.vue'
import LandingHero from './components/landing/LandingHero.vue'
import LandingFeatures from './components/landing/LandingFeatures.vue'
import LandingHowItWorks from './components/landing/LandingHowItWorks.vue'
import LandingPricing from './components/landing/LandingPricing.vue'
import LandingFooter from './components/landing/LandingFooter.vue'

import Sidebar from './components/dashboard/Sidebar.vue'
import ChatHeader from './components/dashboard/ChatHeader.vue'
import ChatWindow from './components/dashboard/ChatWindow.vue'
import ChatInput from './components/dashboard/ChatInput.vue'
import AdminDashboard from './components/dashboard/AdminDashboard.vue'

import AuthModal from './components/auth/AuthModal.vue'
import SettingsModal from './components/modals/SettingsModal.vue'
import AnalysisModal from './components/modals/AnalysisModal.vue'
import WidgetModal from './components/modals/WidgetModal.vue'

import { useAuth } from './composables/useAuth'
import { useDocuments } from './composables/useDocuments'
import { useChat } from './composables/useChat'
import { useI18n } from 'vue-i18n'
import { setLang, getLang } from './composables/useLanguage'
import { verifyEmail } from './api/client'

const { t } = useI18n()

const { 
  isAuthenticated, 
  isAuthModalOpen, 
  chatbotId, 
  apiKey,
  checkSession, 
  logout, 
  openAuthModal, 
  closeAuthModal 
} = useAuth()

const { 
  fetchStats, 
  fetchDocuments, 
  analysisModal, 
  openAnalysis, 
  closeAnalysis 
} = useDocuments()

const { 
  sendMessage, 
  addAgentMessage, 
  clearChat,
  startNewChat
} = useChat()

const currentView = ref('chat') // 'chat' or 'admin'
const chatInputRef = ref(null)
const isSettingsModalOpen = ref(false)
const isWidgetModalOpen = ref(false)
const isMobileSidebarOpen = ref(false)
const verifyResult = ref(null) // null | { loading: true } | { success, message }

onMounted(async () => {
  await handleVerificationLink()
  const hasSession = await checkSession()
  if (hasSession) {
    await Promise.all([
      fetchStats(), 
      fetchDocuments()
    ])
  }
})

// Handles /?verify_token=...&lang=... links from verification emails:
// applies the link language, consumes the token via the API, and shows the result overlay.
async function handleVerificationLink() {
  const params = new URLSearchParams(window.location.search)
  const token = params.get('verify_token')
  if (!token) return

  const vLang = params.get('lang')
  if (vLang) setLang(vLang)

  // Clean the URL immediately so a refresh does not re-consume the token
  window.history.replaceState({}, document.title, window.location.pathname)

  verifyResult.value = { loading: true }
  try {
    const data = await verifyEmail(token, getLang())
    verifyResult.value = {
      success: !!data.success,
      message: data.message || t('verify.failed')
    }
  } catch (e) {
    verifyResult.value = { success: false, message: t('verify.failed') }
  }
}

function closeVerifyResult(openLogin) {
  verifyResult.value = null
  if (openLogin) openAuthModal('login')
}

async function handleAuthSuccess() {
  await Promise.all([
    fetchStats(), 
    fetchDocuments()
  ])
}

async function handleUserLogout() {
  await logout()
  clearChat()
  currentView.value = 'chat'
  isMobileSidebarOpen.value = false
}

function handleToggleDashboard() {
  currentView.value = currentView.value === 'chat' ? 'admin' : 'chat'
  isMobileSidebarOpen.value = false
}

function handleNewChat() {
  currentView.value = 'chat'
  isMobileSidebarOpen.value = false
  startNewChat()
}

function handleFirstUpload(filename) {
  addAgentMessage(t('app.uploadBotMessage', { filename }))
}

function handleViewAnalysis(doc) {
  openAnalysis(doc)
  isMobileSidebarOpen.value = false
}

function handleApplySuggestion(text) {
  if (chatInputRef.value) {
    chatInputRef.value.setQuery(text)
  }
  handleSendMessage(text)
}

async function handleSendMessage(query) {
  await sendMessage(query, {
    chatbotId: chatbotId.value,
    apiKey: apiKey.value
  })
}
</script>
