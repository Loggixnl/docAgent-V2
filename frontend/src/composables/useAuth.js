import { ref, reactive, computed } from 'vue'
import {
  setSessionToken,
  getSessionToken,
  loginUser,
  registerUser,
  getMe,
  logoutUser,
  getSettings,
  saveSettings,
  setOnUnauthorized
} from '../api/client'

const sessionToken = ref(getSessionToken())
const email = ref('')
const chatbotId = ref('')
const apiKey = ref('')
const hasGlobalKey = ref(false)
const defaultProvider = ref('gemini')
const isAuthenticated = computed(() => !!sessionToken.value)

const username = computed(() => {
  if (!email.value) return 'Guest'
  return email.value.split('@')[0]
})

const isAuthModalOpen = ref(false)
const authMode = ref('login') // 'login' | 'register'

// Initialize onUnauthorized handler
setOnUnauthorized(() => {
  handleLogout()
})

async function checkSession() {
  if (!sessionToken.value) return false

  try {
    const data = await getMe()
    email.value = data.email || ''
    chatbotId.value = data.chatbot_id || ''
    await loadSettings()
    return true
  } catch (e) {
    console.error("Auth session check failed:", e)
    handleLogout()
    return false
  }
}

async function handleLogin(userEmail, password) {
  const data = await loginUser(userEmail, password)
  sessionToken.value = data.token
  setSessionToken(data.token)
  email.value = data.email
  chatbotId.value = data.chatbot_id
  await loadSettings()
  isAuthModalOpen.value = false
  return data
}

async function handleRegister(userEmail, password, confirmPassword) {
  const data = await registerUser(userEmail, password, confirmPassword)
  sessionToken.value = data.token
  setSessionToken(data.token)
  email.value = data.email
  chatbotId.value = data.chatbot_id
  await loadSettings()
  isAuthModalOpen.value = false
  return data
}

async function handleLogout() {
  try {
    await logoutUser()
  } catch (e) {
    console.error("Logout failed:", e)
  }
  sessionToken.value = ''
  setSessionToken('')
  email.value = ''
  chatbotId.value = ''
  apiKey.value = ''
  settings.value = {}
}

const settings = ref({})
const globalKeysAvailable = ref({})
const supportedProviders = ref(['gemini', 'openai', 'claude', 'generic', 'groq', 'openrouter'])
const defaultModels = ref({})

async function loadSettings() {
  if (!sessionToken.value) return
  try {
    const data = await getSettings()
    apiKey.value = data.api_key || ''
    settings.value = data.settings || {}
    chatbotId.value = data.chatbot_id || chatbotId.value
    hasGlobalKey.value = !!data.has_global_key
    globalKeysAvailable.value = data.global_keys_available || {}
    if (data.supported_providers) supportedProviders.value = data.supported_providers
    if (data.default_models) defaultModels.value = data.default_models
    if (data.default_provider) defaultProvider.value = data.default_provider
    return data
  } catch (e) {
    console.error("Failed to load settings:", e)
  }
}

async function updateSettings(newSettings) {
  await saveSettings(newSettings)
  if (typeof newSettings === 'string') {
    apiKey.value = newSettings
  } else if (newSettings && typeof newSettings === 'object') {
    apiKey.value = newSettings.api_key || newSettings.gemini_key || apiKey.value
    settings.value = { ...settings.value, ...newSettings }
    // Update defaultProvider if provider was explicitly changed
    if (newSettings.provider) defaultProvider.value = newSettings.provider
  }
  await loadSettings()
}

function openAuthModal(mode = 'login') {
  authMode.value = mode
  isAuthModalOpen.value = true
}

function closeAuthModal() {
  isAuthModalOpen.value = false
}

export function useAuth() {
  return {
    sessionToken,
    email,
    username,
    chatbotId,
    apiKey,
    defaultProvider,
    settings,
    globalKeysAvailable,
    supportedProviders,
    defaultModels,
    hasGlobalKey,
    isAuthenticated,
    isAuthModalOpen,
    authMode,
    checkSession,
    login: handleLogin,
    register: handleRegister,
    logout: handleLogout,
    loadSettings,
    updateSettings,
    openAuthModal,
    closeAuthModal
  }
}

