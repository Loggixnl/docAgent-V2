import { ref, watch } from 'vue'
import { 
  sendChatMessage, 
  getChatSessions, 
  getChatSession, 
  createChatSession, 
  deleteChatSession as apiDeleteChatSession 
} from '../api/client'
import { useAuth } from './useAuth'

const sessions = ref([])
const activeSessionId = ref(null)
const activeSessionTitle = ref('New Chat')
const chatHistory = ref([])
const isTyping = ref(false)
const isLoadingSessions = ref(false)
const isLoadingSession = ref(false)

// Get the active provider and apiKey from auth (reactive, shared state)
const { defaultProvider, apiKey: authApiKey, settings: authSettings } = useAuth()

const PROVIDER_DEFAULT_MODELS = {
  gemini: 'models/gemini-2.0-flash',
  openai: 'gpt-4o-mini',
  claude: 'claude-3-5-haiku-20241022',
  generic: 'llama-3.3-70b-versatile',
  groq: 'llama-3.3-70b-versatile',
  openrouter: 'meta-llama/llama-3.3-70b-instruct'
}

const selectedProvider = ref(defaultProvider.value || 'gemini')
const selectedModel = ref(PROVIDER_DEFAULT_MODELS[defaultProvider.value] || 'models/gemini-2.0-flash')

// Keep selectedProvider in sync when backend settings load
watch(defaultProvider, (newProv) => {
  if (newProv && newProv !== selectedProvider.value) {
    selectedProvider.value = newProv
    if (PROVIDER_DEFAULT_MODELS[newProv]) {
      selectedModel.value = PROVIDER_DEFAULT_MODELS[newProv]
    }
  }
})

const ragLimit = ref(parseInt(localStorage.getItem('docagent_rag_limit')) || 4)

function setProvider(provider) {
  selectedProvider.value = provider
  if (PROVIDER_DEFAULT_MODELS[provider]) {
    selectedModel.value = PROVIDER_DEFAULT_MODELS[provider]
  }
}


function setRagLimit(limit) {
  ragLimit.value = limit
  localStorage.setItem('docagent_rag_limit', limit)
}

function clearChat() {
  sessions.value = []
  activeSessionId.value = null
  activeSessionTitle.value = 'New Chat'
  chatHistory.value = []
}

/**
 * Fetch all chat sessions for the authenticated user
 */
async function fetchSessions() {
  isLoadingSessions.value = true
  try {
    const list = await getChatSessions()
    sessions.value = list || []
    
    // If we don't have an active session, or the current active session is not in the list,
    // pick the first one or start a fresh one
    if (sessions.value.length > 0) {
      if (!activeSessionId.value || !sessions.value.some(s => s.id === activeSessionId.value)) {
        await selectSession(sessions.value[0].id)
      }
    } else {
      activeSessionId.value = null
      activeSessionTitle.value = 'New Chat'
      chatHistory.value = []
    }
  } catch (err) {
    console.error("Failed to load chat sessions:", err)
  } finally {
    isLoadingSessions.value = false
  }
}

/**
 * Start a brand-new chat session
 * For admin-side chats, simply resets the chat window in memory.
 */
function startNewChat() {
  chatHistory.value = []
  activeSessionId.value = null
  activeSessionTitle.value = 'New Chat'
}

/**
 * Select and load a chat session with all previous questions & answers
 */
async function selectSession(sessionId) {
  if (!sessionId) return
  isLoadingSession.value = true
  activeSessionId.value = sessionId

  try {
    const data = await getChatSession(sessionId)
    if (data && data.session) {
      activeSessionTitle.value = data.session.title || 'Chat'
      
      // Map questions into chronological chat history bubbles
      const messages = []
      if (data.questions && data.questions.length > 0) {
        for (const q of data.questions) {
          // User's question
          messages.push({
            role: 'user',
            text: q.question,
            questionId: q.id,
            sessionId: q.session_id,
            questionType: q.question_type,
            status: q.status,
            timestamp: q.created_at
          })

          // AI / Admin response
          messages.push({
            role: 'model',
            text: q.ai_response || (q.status === 'new' ? 'Waiting for response...' : 'No response generated.'),
            adminResponse: q.admin_response || '',
            questionId: q.id,
            sessionId: q.session_id,
            questionType: q.question_type,
            source: q.source || '',
            status: q.status || 'ai_answered',
            context: [], // Stored source document metadata is in q.source
            timestamp: q.updated_at || q.created_at
          })
        }
      }
      chatHistory.value = messages
    }
  } catch (err) {
    console.error("Failed to load session:", err)
    chatHistory.value = []
  } finally {
    isLoadingSession.value = false
  }
}

/**
 * Delete a chat session
 */
async function removeSession(sessionId) {
  try {
    await apiDeleteChatSession(sessionId)
    sessions.value = sessions.value.filter(s => s.id !== sessionId)
    
    if (activeSessionId.value === sessionId) {
      if (sessions.value.length > 0) {
        await selectSession(sessions.value[0].id)
      } else {
        await startNewChat()
      }
    }
  } catch (err) {
    console.error("Failed to delete session:", err)
    alert(`Could not delete chat session: ${err.message}`)
  }
}

/**
 * Send a message within the current session
 */
async function sendMessage(query, { chatbotId, apiKey }) {
  if (!query || isTyping.value) return

  // Optimistically add user query to UI
  const tempUserMsg = {
    role: 'user',
    text: query,
    timestamp: new Date().toISOString()
  }
  chatHistory.value.push(tempUserMsg)

  isTyping.value = true

  try {
    const data = await sendChatMessage({
      query,
      chatHistory: chatHistory.value.map(h => ({ role: h.role, text: h.text })),
      model: selectedModel.value,
      provider: selectedProvider.value,
      chatbotId,
      apiKey,
      sessionId: null,
      saveSession: false // Admin side test chats are not saved to DB
    })

    // Add model answer
    chatHistory.value.push({
      role: 'model',
      text: data.answer,
      context: data.context || [],
      questionId: data.question_id || null,
      sessionId: null,
      questionType: data.question_type,
      status: 'ai_answered',
      source: data.context ? data.context.map(c => c.filename).filter(Boolean).join(', ') : '',
      timestamp: new Date().toISOString()
    })
  } catch (err) {
    chatHistory.value.push({
      role: 'model',
      text: `⚠️ **Error:** ${err.message || "An internal error occurred."}`,
      context: [],
      timestamp: new Date().toISOString()
    })
  } finally {
    isTyping.value = false
  }
}

function addAgentMessage(text, context = []) {
  chatHistory.value.push({
    role: 'model',
    text,
    context,
    timestamp: new Date().toISOString()
  })
}

export function useChat() {
  return {
    sessions,
    activeSessionId,
    activeSessionTitle,
    chatHistory,
    isTyping,
    isLoadingSessions,
    isLoadingSession,
    selectedModel,
    selectedProvider,
    setProvider,
    PROVIDER_DEFAULT_MODELS,
    ragLimit,
    setRagLimit,
    fetchSessions,
    startNewChat,
    selectSession,
    removeSession,
    sendMessage,
    addAgentMessage,
    clearChat
  }
}

