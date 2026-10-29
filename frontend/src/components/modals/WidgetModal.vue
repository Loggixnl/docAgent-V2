<template>
  <div 
    v-if="isOpen" 
    class="modal-overlay open"
    @click.self="close"
  >
    <div class="modal w-full max-w-4xl bg-white border border-gray-200 rounded-2xl p-6 flex flex-col gap-5 shadow-2xl max-h-[90vh]">
      <div class="flex items-center justify-between border-b border-gray-100 pb-4">
        <h3 class="text-sm font-bold text-slate-900 font-heading flex items-center gap-2">
          <i class="mdi mdi-code-tags text-darkTeal text-lg"></i> Integrate Chatbot Widget
        </h3>
        <button class="text-xl text-slate-400 hover:text-slate-900 cursor-pointer" @click="close">&times;</button>
      </div>

      <div class="overflow-y-auto pr-1 flex flex-col gap-6 max-h-[60vh]">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <!-- Left: Customization Settings -->
          <div class="flex flex-col gap-4">
            <h4 class="text-xs font-bold text-slate-400 uppercase tracking-widest border-b border-gray-100 pb-2">
              Customize Your Chatbot
            </h4>

            <div class="flex flex-col gap-1.5">
              <label class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Chatbot ID</label>
              <div class="relative flex items-center">
                <i class="mdi mdi-identifier absolute left-4 text-darkTeal text-base"></i>
                <input 
                  :value="activeChatbotId" 
                  type="text" 
                  readonly 
                  class="w-full bg-slate-50 border border-gray-200 outline-none rounded-xl py-2 pl-11 pr-4 text-xs text-slate-600 opacity-85 cursor-not-allowed font-medium"
                >
              </div>
              <span class="text-[9px] text-slate-500 font-semibold">Unique ID for your chatbot instance.</span>
            </div>

            <div class="flex flex-col gap-1.5">
              <label class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Chatbot Name</label>
              <div class="relative flex items-center">
                <i class="mdi mdi-robot-outline absolute left-4 text-darkTeal text-base"></i>
                <input 
                  v-model="botName" 
                  type="text" 
                  class="w-full bg-white border border-gray-300 focus:border-darkTeal focus:ring-1 focus:ring-darkTeal/20 outline-none rounded-xl py-2 pl-11 pr-4 text-xs text-slate-900 placeholder-gray-400 transition-all font-medium"
                >
              </div>
            </div>

            <div class="flex flex-col gap-1.5">
              <label class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Theme Color</label>
              <div class="flex items-center gap-3 bg-slate-50 border border-gray-200 py-1.5 px-3 rounded-xl">
                <input 
                  v-model="themeColor" 
                  type="color" 
                  class="w-8 h-7 bg-transparent border-none outline-none cursor-pointer rounded"
                >
                <span class="text-xs font-bold text-slate-700 uppercase tracking-wider font-heading">
                  {{ themeColor }}
                </span>
              </div>
            </div>

            <div class="flex flex-col gap-1.5">
              <label class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Initial Greeting Message</label>
              <textarea 
                v-model="greeting" 
                rows="2" 
                class="w-full bg-white border border-gray-300 focus:border-darkTeal focus:ring-1 focus:ring-darkTeal/20 outline-none rounded-xl py-2 px-3 text-xs text-slate-900 placeholder-gray-400 transition-all font-medium"
              ></textarea>
            </div>

            <div class="flex flex-col gap-1.5">
              <label class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Launcher Image URL (Optional)</label>
              <div class="relative flex items-center">
                <i class="mdi mdi-image absolute left-4 text-darkTeal text-base"></i>
                <input 
                  v-model="launcherImage" 
                  type="url" 
                  placeholder="https://example.com/your-image.png"
                  class="w-full bg-white border border-gray-300 focus:border-darkTeal focus:ring-1 focus:ring-darkTeal/20 outline-none rounded-xl py-2 pl-11 pr-4 text-xs text-slate-900 placeholder-gray-400 transition-all font-medium"
                >
              </div>
              <span class="text-[9px] text-slate-500 font-semibold">Optional. A direct image URL shown on the floating chat button instead of the default chat icon. Falls back to the icon if the image fails to load.</span>
            </div>

            <div class="flex flex-col gap-1.5">
              <label class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Backend API URL</label>
              <div class="relative flex items-center">
                <i class="mdi mdi-web absolute left-4 text-darkTeal text-base"></i>
                <input 
                  v-model="apiUrl" 
                  type="text" 
                  placeholder="https://docagent-ai-production-f51e.up.railway.app" 
                  class="w-full bg-white border border-gray-300 focus:border-darkTeal focus:ring-1 focus:ring-darkTeal/20 outline-none rounded-xl py-2 pl-11 pr-4 text-xs text-slate-900 placeholder-gray-400 transition-all font-medium"
                >
              </div>
              <span class="text-[9px] text-slate-500 font-semibold">Override this if your FastAPI backend is running on a different domain or server.</span>
            </div>
          </div>

          <!-- Right: Live Preview -->
          <div class="flex flex-col gap-4">
            <h4 class="text-xs font-bold text-slate-400 uppercase tracking-widest border-b border-gray-100 pb-2">
              Live Preview
            </h4>
            <div class="border border-gray-200 rounded-2xl overflow-hidden bg-slate-100/70 h-[450px] relative flex flex-col shadow-inner">
              <div class="flex items-center justify-center pt-8 text-[11px] text-slate-400 font-bold tracking-wider uppercase">
                Target Website / Portal Preview
              </div>
              
              <!-- Injected interactive widget mock -->
              <div class="absolute inset-0 p-4 pointer-events-none flex flex-col justify-end items-end">
                <div 
                  v-show="mockWidgetOpen"
                  class="w-[320px] sm:w-[340px] h-[360px] sm:h-[380px] bg-white border border-gray-200 rounded-2xl shadow-2xl flex flex-col overflow-hidden mock-widget-panel"
                  :class="{ open: mockWidgetOpen, 'pointer-events-auto': mockWidgetOpen, 'pointer-events-none': !mockWidgetOpen }"
                >
                  <!-- Header -->
                  <div 
                    class="py-3 px-4 flex items-center justify-between text-white shrink-0 shadow-md"
                    :style="{ backgroundColor: themeColor }"
                  >
                    <div class="flex items-center gap-2.5">
                      <div class="w-7 h-7 rounded-lg bg-white/20 flex items-center justify-center text-sm text-white">
                        <i class="mdi mdi-robot-outline"></i>
                      </div>
                      <div class="flex flex-col leading-none">
                        <span class="text-xs font-bold">{{ botName }}</span>
                        <span class="text-[9px] text-white/90 mt-0.5 font-medium flex items-center gap-1">
                          <span class="w-1.5 h-1.5 rounded-full bg-limeGreen inline-block"></span> Active Assistant
                        </span>
                      </div>
                    </div>
                    <button 
                      class="text-white/80 hover:text-white cursor-pointer text-lg font-semibold w-6 h-6 flex items-center justify-center rounded-md hover:bg-white/20 transition-all"
                      @click="mockWidgetOpen = false"
                    >
                      &times;
                    </button>
                  </div>

                  <!-- Chat Body -->
                  <div v-if="!previewInquiryOpen" class="flex-grow overflow-y-auto p-4 flex flex-col gap-2.5 bg-slate-50/60">
                    <div class="max-w-[88%] text-xs p-3 rounded-2xl bg-white border border-gray-200 text-slate-800 self-start leading-relaxed rounded-tl-none shadow-sm font-medium">
                      <p>{{ greeting }}</p>
                    </div>
                  </div>

                  <!-- Mock Inquiry View -->
                  <div v-else class="flex-grow overflow-y-auto p-3 flex flex-col gap-2 bg-slate-50 text-slate-800">
                    <div class="bg-white border border-gray-200 rounded-xl p-2.5 shadow-xs">
                      <span class="text-[9px] font-extrabold uppercase tracking-wider text-darkTeal flex items-center gap-1">
                        <i class="mdi mdi-email-alert-outline"></i> Direct HR Inquiry
                      </span>
                      <h5 class="text-xs font-bold text-slate-900 mt-0.5">Contact HR / Admin Support</h5>
                      <p class="text-[10px] text-slate-500">Preview of the direct inquiry interface.</p>
                    </div>
                    <div class="bg-white border border-gray-200 rounded-xl p-2.5 space-y-2 text-[10px]">
                      <div>
                        <label class="block font-bold text-slate-600 mb-0.5">Email Address</label>
                        <input type="text" placeholder="name@company.com" disabled class="w-full bg-slate-50 border border-slate-200 rounded-lg p-1.5 text-[10px] text-slate-400" />
                      </div>
                      <div>
                        <label class="block font-bold text-slate-600 mb-0.5">Subject / Title</label>
                        <input type="text" placeholder="Leave policy exception" disabled class="w-full bg-slate-50 border border-slate-200 rounded-lg p-1.5 text-[10px] text-slate-400" />
                      </div>
                      <div>
                        <label class="block font-bold text-slate-600 mb-0.5">Description</label>
                        <textarea rows="2" placeholder="Details for the HR admin..." disabled class="w-full bg-slate-50 border border-slate-200 rounded-lg p-1.5 text-[10px] text-slate-400"></textarea>
                      </div>
                      <div class="flex items-center justify-end gap-1.5 pt-1">
                        <button type="button" class="px-2.5 py-1 rounded-lg border border-slate-200 text-slate-600 font-bold text-[10px] cursor-pointer" @click="previewInquiryOpen = false">Back</button>
                        <button type="button" class="px-2.5 py-1 rounded-lg text-white font-bold text-[10px] cursor-pointer" :style="{ backgroundColor: themeColor }" @click="previewInquiryOpen = false">Send to Admin</button>
                      </div>
                    </div>
                  </div>

                  <!-- Footer Input -->
                  <div v-if="!previewInquiryOpen" class="p-3 border-t border-gray-200 flex flex-col gap-1.5 shrink-0 bg-white">
                    <div class="flex items-center justify-start pb-0.5">
                      <button 
                        type="button"
                        class="text-[10px] font-bold py-1 px-2.5 rounded-full border border-slate-200 bg-slate-100 text-slate-700 hover:text-white transition-all flex items-center gap-1.5 cursor-pointer"
                        :style="{ backgroundColor: '#F1F5F9' }"
                        @click="previewInquiryOpen = true"
                      >
                        <i class="mdi mdi-email-alert-outline text-xs"></i>
                        <span>Contact HR / Admin</span>
                      </button>
                    </div>
                    <div class="flex items-center gap-2 bg-slate-50 border border-gray-200 rounded-xl p-1.5 pl-3">
                      <input 
                        type="text" 
                        placeholder="Type a message..." 
                        disabled 
                        class="flex-grow bg-transparent border-none outline-none text-xs text-slate-500 cursor-not-allowed"
                      >
                      <button 
                        class="w-7 h-7 rounded-lg flex items-center justify-center text-white shrink-0 text-xs shadow"
                        :style="{ backgroundColor: themeColor }"
                      >
                        <i class="mdi mdi-send"></i>
                      </button>
                    </div>
                    <span class="text-[8px] text-slate-400 text-center font-medium">Powered by DocAgent AI</span>
                  </div>
                </div>

                <button 
                  class="w-14 h-14 rounded-full flex items-center justify-center shadow-xl text-xl text-white hover:scale-105 transition-all cursor-pointer pointer-events-auto mt-3 overflow-hidden"
                  :style="launcherImage.trim() ? {} : { backgroundColor: themeColor }"
                  @click="mockWidgetOpen = !mockWidgetOpen"
                >
                  <img 
                    v-if="launcherImage.trim()" 
                    :src="launcherImage.trim()" 
                    alt="" 
                    class="w-full h-full object-cover rounded-full"
                  >
                  <i v-else :class="mockWidgetOpen ? 'mdi mdi-close' : 'mdi mdi-comment-text-multiple-outline'"></i>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Bottom: Deployment Code Snippets -->
        <div class="border-t border-gray-100 pt-4 flex flex-col gap-4">
          <h4 class="text-xs font-bold text-slate-400 uppercase tracking-widest pb-1">
            Deployment & Testing Options
          </h4>
          <p class="text-[11px] text-slate-500 font-semibold">
            Choose how you want to use or preview the chatbot widget on your website.
          </p>

          <div class="space-y-4">
            <!-- Option 1: Standard Script Tag -->
            <div class="bg-slate-50 border border-gray-200 rounded-xl p-4">
              <h5 class="text-xs font-bold text-slate-900 flex items-center gap-1.5 mb-1.5">
                <i class="mdi mdi-xml text-darkTeal"></i> Option 1: HTML Script Tag (For Production)
              </h5>
              <p class="text-[10px] text-slate-500 mb-3 font-medium">
                Paste this script tag into the <code>&lt;head&gt;</code> or <code>&lt;body&gt;</code> of your website HTML files.
              </p>
              <div class="flex items-center gap-3 bg-white border border-gray-200 rounded-lg p-2.5 overflow-x-auto justify-between shadow-inner">
                <pre class="text-[10px] text-darkTeal font-mono flex-grow max-w-[80%] overflow-x-auto whitespace-pre-wrap"><code>{{ embedCodeSnippet }}</code></pre>
                <button 
                  class="px-3.5 py-1.5 rounded-full text-white font-bold text-[10px] cursor-pointer shadow transition-all shrink-0 flex items-center gap-1"
                  :class="copiedEmbed ? 'bg-limeGreen' : 'bg-darkTeal hover:bg-darkTeal/90'"
                  @click="copySnippet('embed')"
                >
                  <i :class="copiedEmbed ? 'mdi mdi-check' : 'mdi mdi-content-copy'"></i>
                  {{ copiedEmbed ? 'Copied!' : 'Copy' }}
                </button>
              </div>
            </div>

            <!-- Option 2: Console Snippet -->
            <div class="bg-slate-50 border border-gray-200 rounded-xl p-4">
              <h5 class="text-xs font-bold text-slate-900 flex items-center gap-1.5 mb-1.5">
                <i class="mdi mdi-console text-limeGreen"></i> Option 2: Browser Console Code (For Instant Testing)
              </h5>
              <p class="text-[10px] text-slate-500 mb-3 font-medium">
                Open your target website, press <strong>F12</strong> to open Developer Tools, go to the <strong>Console</strong> tab, paste the code below, and press <strong>Enter</strong> to instantly preview the chatbot.
              </p>
              <div class="flex items-center gap-3 bg-white border border-gray-200 rounded-lg p-2.5 overflow-x-auto justify-between shadow-inner">
                <pre class="text-[10px] text-limeGreen font-mono flex-grow max-w-[80%] overflow-x-auto whitespace-pre-wrap"><code>{{ consoleCodeSnippet }}</code></pre>
                <button 
                  class="px-3.5 py-1.5 rounded-full font-bold text-[10px] cursor-pointer transition-all shrink-0 flex items-center gap-1"
                  :class="copiedConsole ? 'bg-limeGreen text-white' : 'bg-limeGreen/10 border border-limeGreen/30 text-limeGreen hover:bg-limeGreen/20'"
                  @click="copySnippet('console')"
                >
                  <i :class="copiedConsole ? 'mdi mdi-check' : 'mdi mdi-content-copy'"></i>
                  {{ copiedConsole ? 'Copied!' : 'Copy' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="flex justify-end border-t border-gray-100 pt-4">
        <button 
          class="px-4 py-2 text-xs font-bold rounded-full text-slate-600 border border-gray-300 hover:bg-slate-50 transition-all cursor-pointer"
          @click="close"
        >
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuth } from '../../composables/useAuth'

defineProps({
  isOpen: Boolean
})

const emit = defineEmits(['close'])

const { chatbotId } = useAuth()

const botName = ref('DocAgent AI')
const themeColor = ref('#D946EF')
const greeting = ref('Hello! How can I help you with our company policies today?')
const launcherImage = ref('https://5t61ut5p19.ucarecd.net/f327ad9c-bcf0-4175-9ff9-9d09db984074/')
const DEFAULT_BACKEND_URL = (import.meta.env.VITE_API_BASE_URL || 'https://docagent-ai-production-f51e.up.railway.app').replace(/\/+$/, '')
const apiUrl = ref(DEFAULT_BACKEND_URL)
const mockWidgetOpen = ref(false)
const previewInquiryOpen = ref(false)

const activeChatbotId = computed(() => chatbotId.value || 'cb_d778e9e0b662')

const copiedEmbed = ref(false)
const copiedConsole = ref(false)

const WIDGET_VERSION = '1.1.3'

const escapeAttr = (value) => (value || '').replace(/&/g, '&amp;').replace(/"/g, '&quot;')

const embedCodeSnippet = computed(() => {
  const url = (apiUrl.value || DEFAULT_BACKEND_URL).trim().replace(/\/+$/, '')
  const currentChatbotId = activeChatbotId.value
  const image = launcherImage.value.trim()
  const imageAttr = image ? `\n  data-launcher-image="${escapeAttr(image)}"` : ''
  return `<script\n  src="${url}/widget.js?v=${WIDGET_VERSION}"\n  data-api-url="${url}"\n  data-chatbot-id="${currentChatbotId}"\n  data-bot-name="${escapeAttr(botName.value)}"\n  data-color="${themeColor.value}"\n  data-greeting="${escapeAttr(greeting.value)}"${imageAttr}\n  defer\n><\/script>`
})

const consoleCodeSnippet = computed(() => {
  const url = (apiUrl.value || DEFAULT_BACKEND_URL).trim().replace(/\/+$/, '')
  const currentChatbotId = activeChatbotId.value
  const escName = (botName.value || '').replace(/"/g, '\\"')
  const escGreeting = (greeting.value || '').replace(/"/g, '\\"')
  const image = launcherImage.value.trim()
  const imageLine = image ? `script.setAttribute('data-launcher-image', ${JSON.stringify(image)});\n` : ''
  return `const script = document.createElement('script');\n` +
    `script.src = "${url}/widget.js?v=${WIDGET_VERSION}";\n` +
    `script.setAttribute('data-api-url', "${url}");\n` +
    `script.setAttribute('data-chatbot-id', "${currentChatbotId}");\n` +
    `script.setAttribute('data-bot-name', "${escName}");\n` +
    `script.setAttribute('data-color', "${themeColor.value}");\n` +
    `script.setAttribute('data-greeting', "${escGreeting}");\n` +
    imageLine +
    `script.defer = true;\n` +
    `document.body.appendChild(script);`
})

async function copySnippet(type) {
  const text = type === 'embed' ? embedCodeSnippet.value : consoleCodeSnippet.value
  try {
    await navigator.clipboard.writeText(text)
    if (type === 'embed') {
      copiedEmbed.value = true
      setTimeout(() => { copiedEmbed.value = false }, 2000)
    } else {
      copiedConsole.value = true
      setTimeout(() => { copiedConsole.value = false }, 2000)
    }
  } catch (err) {
    alert('Failed to copy snippet. Please select and copy manually.')
  }
}

function close() {
  emit('close')
}
</script>
