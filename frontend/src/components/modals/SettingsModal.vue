<template>
  <div 
    v-if="isOpen" 
    class="modal-overlay open"
    @click.self="close"
  >
    <div class="modal w-full max-w-md bg-white border border-gray-200 rounded-2xl p-6 flex flex-col gap-5 shadow-2xl max-h-[90vh] overflow-y-auto">
      <!-- Header -->
      <div class="flex items-center justify-between border-b border-gray-100 pb-4">
        <h3 class="text-sm font-bold text-slate-900 font-heading flex items-center gap-2">
          <i class="mdi mdi-cog-outline text-darkTeal text-lg"></i> Chatbot Settings
        </h3>
        <button class="text-xl text-slate-400 hover:text-slate-900 cursor-pointer" @click="close">&times;</button>
      </div>

      <!-- Chatbot ID -->
      <div class="flex flex-col gap-1.5">
        <label class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Your Unique Chatbot ID</label>
        <p class="text-[9px] text-slate-400 font-medium">Use this ID to embed the chatbot widget on your website.</p>
        <div class="flex items-center gap-2">
          <div class="relative flex-grow">
            <i class="mdi mdi-identifier absolute left-4 text-darkTeal text-base top-1/2 -translate-y-1/2"></i>
            <input 
              :value="chatbotId" 
              type="text" 
              readonly 
              class="w-full bg-slate-50 border border-gray-200 outline-none rounded-xl py-2.5 pl-11 pr-4 text-xs text-slate-600 cursor-not-allowed font-medium"
            >
          </div>
          <button
            class="shrink-0 px-3 py-2.5 text-[10px] font-bold rounded-xl bg-lightTeal/10 text-darkTeal hover:bg-lightTeal/20 transition-all border border-lightTeal/20 cursor-pointer flex items-center gap-1"
            title="Copy Chatbot ID"
            @click="copyChatbotId"
          >
            <i class="mdi" :class="copied ? 'mdi-check' : 'mdi-content-copy'"></i>
            {{ copied ? 'Copied!' : 'Copy' }}
          </button>
        </div>
      </div>

      <!-- RAG Matches Slider -->
      <div class="flex flex-col gap-1.5">
        <label class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Context Search Depth</label>
        <p class="text-[9px] text-slate-400 font-medium">How many document chunks to retrieve per question. Higher = more context, slightly slower.</p>
        <div class="flex items-center gap-3 mt-1">
          <input 
            v-model.number="inputRagLimit" 
            type="range" 
            min="2" 
            max="10" 
            class="flex-grow accent-darkTeal"
          >
          <span class="text-xs font-bold text-darkTeal min-w-[60px] text-right">{{ inputRagLimit }} Chunks</span>
        </div>
        <div class="flex justify-between text-[9px] text-slate-400 font-medium">
          <span>Faster (2)</span>
          <span>More Context (10)</span>
        </div>
      </div>

      <!-- AI Model Info Banner -->
      <div class="flex items-start gap-3 p-3 bg-lightTeal/5 border border-lightTeal/20 rounded-xl">
        <i class="mdi mdi-information-outline text-darkTeal text-base shrink-0 mt-0.5"></i>
        <div>
          <p class="text-[10px] font-bold text-slate-700 mb-0.5">AI Model is managed server-side</p>
          <p class="text-[9px] text-slate-500 font-medium leading-relaxed">
            The AI provider and model are configured by your administrator. Your chatbot uses the best available model automatically - no API key setup needed on your end.
          </p>
        </div>
      </div>

      <!-- Footer Actions -->
      <div class="flex justify-end gap-3 border-t border-gray-100 pt-4">
        <button 
          class="px-4 py-2 text-xs font-bold rounded-full text-slate-600 border border-gray-300 hover:bg-slate-50 transition-all cursor-pointer"
          @click="close"
        >
          Cancel
        </button>
        <button 
          class="px-5 py-2 text-xs font-bold rounded-full bg-darkTeal text-white shadow-md shadow-darkTeal/10 hover:bg-darkTeal/90 transition-all cursor-pointer"
          :disabled="saving"
          @click="handleSave"
        >
          {{ saving ? 'Saving...' : 'Save Settings' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuth } from '../../composables/useAuth'
import { useChat } from '../../composables/useChat'

const props = defineProps({
  isOpen: Boolean
})

const emit = defineEmits(['close'])

const { chatbotId } = useAuth()
const { ragLimit, setRagLimit } = useChat()

const inputRagLimit = ref(ragLimit.value || 4)
const saving = ref(false)
const copied = ref(false)

async function copyChatbotId() {
  try {
    await navigator.clipboard.writeText(chatbotId.value)
    copied.value = true
    setTimeout(() => { copied.value = false }, 2000)
  } catch {
    // fallback for older browsers
  }
}

function close() {
  emit('close')
}

function handleSave() {
  saving.value = true
  setRagLimit(inputRagLimit.value)
  saving.value = false
  close()
}
</script>
