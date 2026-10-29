<template>
  <div 
    v-if="isOpen" 
    class="modal-overlay open"
    @click.self="close"
  >
    <div class="modal w-full max-w-3xl bg-white border border-gray-200 rounded-2xl p-6 flex flex-col gap-5 shadow-2xl max-h-[85vh]">
      <div class="flex items-center justify-between border-b border-gray-100 pb-4">
        <h3 class="text-sm font-bold text-slate-900 font-heading truncate max-w-[80%]">
          Analysis: {{ filename }}
        </h3>
        <button class="text-xl text-slate-400 hover:text-slate-900 cursor-pointer" @click="close">&times;</button>
      </div>

      <div class="flex-grow overflow-y-auto pr-1 text-xs md:text-sm text-slate-700">
        <!-- Loading State -->
        <div v-if="isLoading" class="flex flex-col items-center justify-center py-16 text-slate-400 gap-3">
          <i class="mdi mdi-loading mdi-spin text-3xl text-darkTeal"></i>
          <p class="text-xs font-semibold">Generating summary report...</p>
        </div>

        <!-- Rendered Report -->
        <MarkdownContent v-else :content="content" />
      </div>

      <div class="flex justify-end border-t border-gray-100 pt-4">
        <button 
          class="px-5 py-2 text-xs font-bold rounded-full bg-darkTeal text-white shadow-md hover:bg-darkTeal/90 transition-all cursor-pointer"
          @click="close"
        >
          Close Report
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import MarkdownContent from '../common/MarkdownContent.vue'

defineProps({
  isOpen: Boolean,
  filename: {
    type: String,
    default: ''
  },
  content: {
    type: String,
    default: ''
  },
  isLoading: Boolean
})

const emit = defineEmits(['close'])

function close() {
  emit('close')
}
</script>
