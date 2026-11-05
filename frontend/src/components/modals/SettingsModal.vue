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
          <i class="mdi mdi-cog-outline text-darkTeal text-lg"></i> {{ $t('settings.heading') }}
        </h3>
        <button class="text-xl text-slate-400 hover:text-slate-900 cursor-pointer" @click="close">&times;</button>
      </div>

      <!-- Chatbot ID -->
      <div class="flex flex-col gap-1.5">
        <label class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">{{ $t('settings.chatbotIdLabel') }}</label>
        <p class="text-[9px] text-slate-400 font-medium">{{ $t('settings.chatbotIdHelp') }}</p>
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
            :title="$t('settings.copyChatbotId')"
            @click="copyChatbotId"
          >
            <i class="mdi" :class="copied ? 'mdi-check' : 'mdi-content-copy'"></i>
            {{ copied ? $t('common.copied') : $t('common.copy') }}
          </button>
        </div>
      </div>

      <!-- RAG Matches Slider -->
      <div class="flex flex-col gap-1.5">
        <label class="text-[10px] font-bold text-slate-500 uppercase tracking-wider">{{ $t('settings.depthLabel') }}</label>
        <p class="text-[9px] text-slate-400 font-medium">{{ $t('settings.depthHelp') }}</p>
        <div class="flex items-center gap-3 mt-1">
          <input
            v-model.number="inputRagLimit"
            type="range"
            min="2"
            max="10"
            class="flex-grow accent-darkTeal"
          >
          <span class="text-xs font-bold text-darkTeal min-w-[60px] text-right">{{ $t('settings.chunksValue', { n: inputRagLimit }) }}</span>
        </div>
        <div class="flex justify-between text-[9px] text-slate-400 font-medium">
          <span>{{ $t('settings.faster') }}</span>
          <span>{{ $t('settings.moreContext') }}</span>
        </div>
      </div>

      <!-- AI Model Info Banner -->
      <div class="flex items-start gap-3 p-3 bg-lightTeal/5 border border-lightTeal/20 rounded-xl">
        <i class="mdi mdi-information-outline text-darkTeal text-base shrink-0 mt-0.5"></i>
        <div>
          <p class="text-[10px] font-bold text-slate-700 mb-0.5">{{ $t('settings.managedServer') }}</p>
          <p class="text-[9px] text-slate-500 font-medium leading-relaxed">
            {{ $t('settings.managedBody') }}
          </p>
        </div>
      </div>

      <!-- Footer Actions -->
      <div class="flex justify-end gap-3 border-t border-gray-100 pt-4">
        <button 
          class="px-4 py-2 text-xs font-bold rounded-full text-slate-600 border border-gray-300 hover:bg-slate-50 transition-all cursor-pointer"
          @click="close"
        >
          {{ $t('common.cancel') }}
        </button>
        <button
          class="px-5 py-2 text-xs font-bold rounded-full bg-darkTeal text-white shadow-md shadow-darkTeal/10 hover:bg-darkTeal/90 transition-all cursor-pointer"
          :disabled="saving"
          @click="handleSave"
        >
          {{ saving ? $t('common.saving') : $t('settings.saveSettings') }}
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
