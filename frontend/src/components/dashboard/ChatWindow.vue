<template>
  <div ref="chatContainerRef" class="flex-grow overflow-y-auto p-3 sm:p-6 space-y-4 sm:space-y-6 bg-slate-50/10">
    <!-- Welcome Card (shown when chat is empty) -->
    <div v-if="chatHistory.length === 0" class="h-full flex items-center justify-center p-2">
      <div class="max-w-lg w-full bg-white border border-gray-200 rounded-2xl p-5 sm:p-7 text-center shadow-md">
        <div class="w-12 h-12 rounded-2xl bg-lightTeal/10 text-darkTeal flex items-center justify-center text-2xl mx-auto mb-3 shadow-inner">
          <i class="mdi mdi-robot-happy-outline"></i>
        </div>
        <h3 class="text-base font-black text-slate-900 mb-1.5 font-heading">DocAgent AI Question Assistant</h3>
        <p class="text-xs text-slate-500 leading-relaxed mb-4 font-medium">
          Ask questions about your uploaded <strong>knowledge base documents</strong>. Answers are generated strictly from the content of your uploaded files, complete with source citations.
        </p>

        <!-- Document Knowledge Base notice badge -->
        <div class="flex items-center justify-center gap-2 mb-5">
          <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-lightTeal/10 text-darkTeal text-[10px] font-bold">
            <i class="mdi mdi-file-document-check-outline"></i> Verified Document Knowledge Base
          </span>
          <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-slate-100 text-slate-600 text-[10px] font-bold">
            <i class="mdi mdi-shield-check-outline"></i> Strict Document-Only Answers
          </span>
        </div>

        <div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2.5 text-left">Try these example questions:</div>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
          <!-- Document Examples -->
          <button 
            class="text-left p-2.5 rounded-xl bg-slate-50 border border-gray-200 hover:border-lightTeal/50 hover:bg-lightTeal/5 text-xs text-slate-700 hover:text-darkTeal transition-all flex items-start gap-2 font-semibold cursor-pointer"
            @click="$emit('applySuggestion', 'Can you summarize the main points in the uploaded documents?')"
          >
            <i class="mdi mdi-file-check-outline text-darkTeal text-sm shrink-0 mt-0.5"></i> 
            <div class="min-w-0">
              <span class="block truncate">Document Overview</span>
              <span class="text-[9px] text-slate-400 font-normal">Summarizes uploaded content</span>
            </div>
          </button>

          <button 
            class="text-left p-2.5 rounded-xl bg-slate-50 border border-gray-200 hover:border-lightTeal/50 hover:bg-lightTeal/5 text-xs text-slate-700 hover:text-darkTeal transition-all flex items-start gap-2 font-semibold cursor-pointer"
            @click="$emit('applySuggestion', 'What are the main rules, guidelines, or instructions?')"
          >
            <i class="mdi mdi-format-list-checks text-darkTeal text-sm shrink-0 mt-0.5"></i> 
            <div class="min-w-0">
              <span class="block truncate">Rules & Guidelines</span>
              <span class="text-[9px] text-slate-400 font-normal">Searches guidelines & policies</span>
            </div>
          </button>

          <button 
            class="text-left p-2.5 rounded-xl bg-slate-50 border border-gray-200 hover:border-lightTeal/50 hover:bg-lightTeal/5 text-xs text-slate-700 hover:text-darkTeal transition-all flex items-start gap-2 font-semibold cursor-pointer"
            @click="$emit('applySuggestion', 'What are the step-by-step procedures described?')"
          >
            <i class="mdi mdi-stairs text-darkTeal text-sm shrink-0 mt-0.5"></i> 
            <div class="min-w-0">
              <span class="block truncate">Procedures & Steps</span>
              <span class="text-[9px] text-slate-400 font-normal">Searches processes & instructions</span>
            </div>
          </button>

          <button 
            class="text-left p-2.5 rounded-xl bg-slate-50 border border-gray-200 hover:border-lightTeal/50 hover:bg-lightTeal/5 text-xs text-slate-700 hover:text-darkTeal transition-all flex items-start gap-2 font-semibold cursor-pointer"
            @click="$emit('applySuggestion', 'What are the specific conditions, requirements, or criteria?')"
          >
            <i class="mdi mdi-clipboard-text-outline text-darkTeal text-sm shrink-0 mt-0.5"></i> 
            <div class="min-w-0">
              <span class="block truncate">Requirements & Criteria</span>
              <span class="text-[9px] text-slate-400 font-normal">Searches terms & requirements</span>
            </div>
          </button>
        </div>
      </div>
    </div>

    <!-- Message Bubbles -->
    <template v-else>
      <div 
        v-for="(msg, idx) in chatHistory" 
        :key="idx"
        class="flex gap-2.5 sm:gap-3.5 max-w-[95%] sm:max-w-[85%]"
        :class="msg.role === 'user' ? 'self-end flex-row-reverse ml-auto' : 'self-start mr-auto'"
      >
        <!-- Avatar -->
        <div 
          class="w-8 h-8 sm:w-9 sm:h-9 rounded-xl flex items-center justify-center shrink-0 text-sm shadow-sm"
          :class="msg.role === 'user' ? 'bg-slate-100 border border-slate-200 text-slate-500' : 'bg-lightTeal/15 text-darkTeal'"
        >
          <i :class="msg.role === 'user' ? 'mdi mdi-account' : 'mdi mdi-robot-outline'"></i>
        </div>

        <!-- Bubble Body -->
        <div 
          class="p-3.5 sm:p-4 rounded-2xl text-xs leading-relaxed shadow-sm min-w-0"
          :class="msg.role === 'user' 
            ? 'bg-slate-100 border border-slate-200 text-slate-800 rounded-tr-none' 
            : 'bg-white border border-slate-200/90 text-slate-800 rounded-tl-none'"
        >
          <!-- Metadata header for AI response -->
          <div v-if="msg.role === 'model'" class="flex flex-wrap items-center justify-between gap-1.5 mb-2.5 pb-2 border-b border-slate-100 text-[10px]">
            <!-- Question Type Badge -->
            <div class="flex items-center gap-1.5">
              <span 
                v-if="msg.questionType === 'document'" 
                class="px-2 py-0.5 rounded-full bg-lightTeal/15 text-darkTeal font-extrabold flex items-center gap-1"
              >
                <i class="mdi mdi-file-document-outline"></i> Document Knowledge
              </span>
              <span 
                v-else-if="msg.questionType === 'general'" 
                class="px-2 py-0.5 rounded-full bg-slate-100 text-slate-700 font-extrabold flex items-center gap-1"
              >
                <i class="mdi mdi-robot-outline"></i> Assistant Response
              </span>

              <!-- Status Badge -->
              <span 
                class="px-2 py-0.5 rounded-full font-bold uppercase tracking-wider text-[8px]"
                :class="getStatusClass(msg.status)"
              >
                {{ formatStatus(msg.status) }}
              </span>
            </div>

            <!-- Question ID (if available) -->
            <span v-if="msg.questionId" class="text-slate-400 font-mono text-[9px]">
              {{ msg.questionId }}
            </span>
          </div>

          <!-- User plain text or Agent Markdown -->
          <div v-if="msg.role === 'user'" class="break-words font-medium">{{ msg.text }}</div>
          <MarkdownContent v-else :content="msg.text" class="break-words" />

          <!-- OFFICIAL ADMIN RESPONSE (If reviewed/responded by admin) -->
          <div v-if="msg.adminResponse" class="mt-3.5 pt-3 border-t-2 border-emerald-200 bg-emerald-50/70 -mx-3.5 sm:-mx-4 -mb-3.5 sm:-mb-4 p-3 sm:p-3.5 rounded-b-2xl">
            <div class="flex items-center gap-1.5 text-[11px] font-black text-emerald-800 mb-1.5">
              <i class="mdi mdi-shield-check text-emerald-600 text-sm"></i>
              <span>Official HR Admin Response & Review</span>
            </div>
            <div class="text-xs text-emerald-950 font-medium whitespace-pre-wrap leading-relaxed">
              {{ msg.adminResponse }}
            </div>
          </div>

          <!-- Context Accordion (For document-based RAG answers) -->
          <div v-if="(msg.context && msg.context.length > 0) || msg.source" class="mt-3 pt-2.5 border-t border-slate-100">
            <button 
              class="flex items-center gap-1 text-[10px] font-bold text-darkTeal hover:text-slate-900 transition-colors cursor-pointer select-none"
              @click="toggleSources(idx)"
            >
              <i 
                class="mdi mdi-chevron-down text-xs transition-transform duration-200"
                :class="{ 'rotate-180': openSources[idx] }"
              ></i> 
              <span v-if="msg.context && msg.context.length > 0">
                Referenced {{ msg.context.length }} Document Source Chunk(s)
              </span>
              <span v-else>
                Source: {{ msg.source }}
              </span>
            </button>

            <!-- Detailed Chunks Preview -->
            <div v-if="openSources[idx] && msg.context && msg.context.length > 0" class="flex flex-col gap-2 mt-2">
              <div 
                v-for="(chunk, cIdx) in msg.context" 
                :key="cIdx"
                class="bg-slate-50 border border-slate-200/80 rounded-xl p-2.5 shadow-xs"
              >
                <div class="flex items-center justify-between text-[9px] font-bold text-slate-500 mb-1 gap-2">
                  <span class="truncate font-semibold text-slate-800">
                    [{{ cIdx + 1 }}] {{ chunk.filename }}
                  </span>
                  <span v-if="chunk.score" class="text-limeGreen font-bold shrink-0">
                    Match: {{ (chunk.score * 100).toFixed(0) }}%
                  </span>
                </div>
                <p class="text-[9px] text-slate-600 leading-normal italic font-medium">
                  "{{ chunk.text.substring(0, 150) }}..."
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Typing Indicator -->
      <div v-if="isTyping" class="flex gap-2.5 sm:gap-3.5 max-w-[95%] sm:max-w-[85%] self-start mr-auto">
        <div class="w-8 h-8 sm:w-9 sm:h-9 rounded-xl flex items-center justify-center shrink-0 text-sm bg-lightTeal/15 text-darkTeal shadow-sm">
          <i class="mdi mdi-robot-outline"></i>
        </div>
        <div class="p-3.5 rounded-2xl text-xs bg-white border border-slate-200 text-slate-800 rounded-tl-none shadow-sm flex items-center gap-2">
          <div class="typing-indicator">
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
          </div>
          <span class="text-[10px] text-slate-400 font-semibold">Analyzing query & generating answer...</span>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, watch, nextTick, reactive } from 'vue'
import MarkdownContent from '../common/MarkdownContent.vue'
import { useChat } from '../../composables/useChat'

defineEmits(['applySuggestion'])

const { chatHistory, isTyping } = useChat()

const chatContainerRef = ref(null)
const openSources = reactive({})

function toggleSources(idx) {
  openSources[idx] = !openSources[idx]
}

function getStatusClass(status) {
  switch (status) {
    case 'resolved':
      return 'bg-emerald-100 text-emerald-800'
    case 'admin_answered':
      return 'bg-purple-100 text-purple-800'
    case 'needs_review':
      return 'bg-amber-100 text-amber-800'
    case 'new':
      return 'bg-slate-200 text-slate-700'
    case 'ai_answered':
    default:
      return 'bg-blue-100 text-blue-800'
  }
}

function formatStatus(status) {
  switch (status) {
    case 'resolved': return 'Resolved'
    case 'admin_answered': return 'Admin Answered'
    case 'needs_review': return 'Needs Review'
    case 'new': return 'New'
    case 'ai_answered':
    default: return 'AI Answered'
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (chatContainerRef.value) {
      chatContainerRef.value.scrollTop = chatContainerRef.value.scrollHeight
    }
  })
}

watch(
  () => [chatHistory.value.length, isTyping.value],
  () => {
    scrollToBottom()
  }
)
</script>
