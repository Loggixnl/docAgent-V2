<template>
  <footer class="py-2.5 sm:py-4 px-3 sm:px-6 border-t border-gray-200 bg-slate-50/50 shrink-0">
    <div class="flex items-center gap-2 sm:gap-3 bg-white border border-gray-300 rounded-2xl p-1.5 sm:p-2 focus-within:border-darkTeal/80 focus-within:ring-1 focus-within:ring-darkTeal/20 transition-all shadow-sm">
      <textarea 
        ref="textareaRef"
        v-model="inputText"
        placeholder="Ask a question about uploaded documents..." 
        rows="1" 
        class="flex-grow bg-transparent border-none outline-none text-xs text-slate-900 placeholder-gray-400 resize-none max-h-24 py-1 sm:py-1.5 pl-2 sm:pl-3 font-medium"
        @input="handleInput"
        @keydown="handleKeydown"
      ></textarea>
      
      <button 
        class="w-8 h-8 sm:w-8.5 sm:h-8.5 rounded-xl flex items-center justify-center bg-darkTeal text-white shadow-md shadow-darkTeal/10 cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed hover:bg-darkTeal/90 hover:scale-105 active:scale-95 transition-all text-sm shrink-0"
        :disabled="!canSend"
        @click="send"
      >
        <i class="mdi mdi-send"></i>
      </button>
    </div>
    
    <div class="flex items-center gap-1.5 text-[8px] sm:text-[9px] text-slate-400 font-semibold mt-2 ml-1">
      <i class="mdi mdi-information-outline text-darkTeal"></i> Relying strictly on uploaded document sources for answers.
    </div>
  </footer>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import { useChat } from '../../composables/useChat'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'send'])

const { isTyping } = useChat()
const inputText = ref(props.modelValue)
const textareaRef = ref(null)

const canSend = computed(() => {
  return inputText.value.trim().length > 0 && !isTyping.value
})

function handleInput() {
  resizeTextarea()
  emit('update:modelValue', inputText.value)
}

function handleKeydown(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    send()
  }
}

function resizeTextarea() {
  const el = textareaRef.value
  if (!el) return
  el.style.height = 'auto'
  el.style.height = `${Math.min(el.scrollHeight, 120)}px`
}

function setQuery(text) {
  inputText.value = text
  nextTick(() => {
    resizeTextarea()
  })
}

function send() {
  if (!canSend.value) return
  const text = inputText.value.trim()
  inputText.value = ''
  nextTick(() => {
    resizeTextarea()
  })
  emit('send', text)
}

defineExpose({
  setQuery
})
</script>
