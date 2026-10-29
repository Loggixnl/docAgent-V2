<template>
  <header class="py-2.5 sm:py-3 px-3 sm:px-6 border-b border-gray-200 flex items-center justify-between bg-slate-50/50 gap-2 shrink-0">
    <div class="flex items-center gap-2 sm:gap-3 min-w-0">
      <!-- Mobile Sidebar Toggle Button -->
      <button 
        class="lg:hidden w-8.5 h-8.5 rounded-xl flex items-center justify-center bg-slate-100 border border-gray-200 text-slate-700 hover:bg-slate-200 text-base shrink-0 cursor-pointer"
        title="Open drawer"
        @click="$emit('toggleSidebar')"
      >
        <i class="mdi mdi-menu text-darkTeal"></i>
      </button>

      <div class="w-9 h-9 sm:w-10 sm:h-10 rounded-xl bg-lightTeal/10 flex items-center justify-center text-darkTeal text-base sm:text-lg relative shrink-0">
        <i class="mdi mdi-robot-outline"></i>
        <span class="absolute bottom-0 right-0 w-2 sm:w-2.5 h-2 sm:h-2.5 rounded-full bg-limeGreen ring-2 ring-white"></span>
      </div>

      <div class="min-w-0">
        <div class="flex items-center gap-2">
          <h2 class="text-xs sm:text-sm font-bold text-slate-900 truncate">
            {{ isDashboardView ? 'Admin Management Dashboard' : (activeSessionTitle || 'New Chat') }}
          </h2>
          <!-- New Chat quick button in header -->
          <button 
            v-if="!isDashboardView"
            class="hidden sm:inline-flex items-center gap-1 px-2 py-0.5 rounded-lg bg-lightTeal/10 hover:bg-lightTeal/20 text-darkTeal text-[10px] font-bold transition-colors cursor-pointer"
            title="Start a new chat session"
            @click="$emit('newChat')"
          >
            <i class="mdi mdi-plus text-xs"></i>
            <span>New Chat</span>
          </button>
        </div>

        <div class="flex items-center gap-1.5 mt-0.5">
          <span 
            v-if="!isDashboardView" 
            class="text-[8px] sm:text-[9px] text-limeGreen bg-limeGreen/10 px-1.5 sm:px-2 py-0.2 rounded-full font-extrabold uppercase tracking-wider"
          >
            Session Active
          </span>
          <span 
            v-else
            class="text-[8px] sm:text-[9px] text-darkTeal bg-lightTeal/15 px-1.5 sm:px-2 py-0.2 rounded-full font-extrabold uppercase tracking-wider"
          >
            Analytics & Reviews
          </span>
        </div>
      </div>
    </div>

    <!-- Right Actions -->
    <div class="flex items-center gap-1.5 sm:gap-2.5 shrink-0">
      <!-- Admin Dashboard / Chat Toggle Button -->
      <button 
        class="py-1.5 px-2.5 sm:px-3 rounded-xl border text-xs font-bold transition-all flex items-center gap-1.5 cursor-pointer shadow-sm"
        :class="isDashboardView 
          ? 'bg-gradient-to-r from-lightTeal to-darkTeal text-white border-transparent hover:opacity-95' 
          : 'bg-white border-slate-300 text-slate-700 hover:text-darkTeal hover:border-darkTeal/40'"
        :title="isDashboardView ? 'Switch to Chat Assistant' : 'Switch to Admin Question Management Dashboard'"
        @click="$emit('toggleView')"
      >
        <i :class="isDashboardView ? 'mdi mdi-chat-outline' : 'mdi mdi-view-dashboard-outline'"></i>
        <span class="hidden sm:inline">{{ isDashboardView ? 'Back to Chat' : 'Admin Dashboard' }}</span>
      </button>

      <!-- User Profile Badge (hidden on mobile, visible from md) -->
      <div class="hidden md:flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl bg-slate-100 border border-gray-200 text-xs text-slate-700 font-bold max-w-[130px] truncate">
        <i class="mdi mdi-account-circle-outline text-sm text-darkTeal shrink-0"></i>
        <span class="truncate">{{ username }}</span>
      </div>



      <!-- Action Buttons -->
      <button 
        class="w-8 h-8 rounded-xl flex items-center justify-center bg-slate-100 border border-gray-200 text-slate-600 hover:text-slate-900 hover:bg-slate-200 hover:border-gray-400 transition-all text-sm cursor-pointer shrink-0"
        title="Integrate Chatbot Widget"
        @click="$emit('openWidget')"
      >
        <i class="mdi mdi-code-tags"></i>
      </button>

      <button 
        class="w-8 h-8 rounded-xl flex items-center justify-center bg-slate-100 border border-gray-200 text-slate-600 hover:text-slate-900 hover:bg-slate-200 hover:border-gray-400 transition-all text-sm cursor-pointer shrink-0"
        title="Settings"
        @click="$emit('openSettings')"
      >
        <i class="mdi mdi-cog-outline"></i>
      </button>

      <button 
        class="w-8 h-8 rounded-xl flex items-center justify-center bg-slate-100 border border-gray-200 text-slate-600 hover:text-coralOrange hover:bg-coralOrange/10 hover:border-coralOrange/30 transition-all text-sm cursor-pointer shrink-0"
        title="Sign Out"
        @click="$emit('logout')"
      >
        <i class="mdi mdi-logout"></i>
      </button>
    </div>
  </header>
</template>

<script setup>
import { useAuth } from '../../composables/useAuth'
import { useChat } from '../../composables/useChat'

defineProps({
  isDashboardView: {
    type: Boolean,
    default: false
  }
})

defineEmits(['openWidget', 'openSettings', 'logout', 'toggleSidebar', 'toggleView', 'newChat'])

const { username } = useAuth()
const { activeSessionTitle } = useChat()
</script>

