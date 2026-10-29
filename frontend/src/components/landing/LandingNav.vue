<template>
  <header class="w-full py-3.5 sm:py-4 px-4 sm:px-6 md:px-12 flex flex-col border-b border-gray-200/50 backdrop-blur-md sticky top-0 z-40 bg-white/90 shadow-sm transition-all">
    <div class="flex items-center justify-between w-full">
      <div class="flex items-center gap-2.5 sm:gap-3">
        <div class="w-9 h-9 sm:w-10 sm:h-10 rounded-xl flex items-center justify-center text-white bg-gradient-to-br from-lightTeal to-darkTeal shadow-md shadow-lightTeal/10 text-lg sm:text-xl">
          <i class="mdi mdi-shield-text-outline"></i>
        </div>
        <div>
          <h1 class="text-base sm:text-lg font-black font-heading text-slate-900 tracking-tight leading-none">DocAgent AI</h1>
          <span class="text-[8px] sm:text-[9px] text-darkTeal font-bold uppercase tracking-wider block mt-0.5">SaaS Chatbot Platform</span>
        </div>
      </div>

      <!-- Desktop Nav Links -->
      <nav class="hidden md:flex items-center gap-8">
        <a href="#features" class="text-sm text-slate-600 hover:text-darkTeal transition-colors font-semibold">Features</a>
        <a href="#how-it-works" class="text-sm text-slate-600 hover:text-darkTeal transition-colors font-semibold">How It Works</a>
        <a href="#pricing" class="text-sm text-slate-600 hover:text-darkTeal transition-colors font-semibold">Pricing</a>
      </nav>

      <!-- Desktop CTA Buttons -->
      <div class="hidden sm:flex items-center gap-2 sm:gap-3">
        <button 
          class="px-3.5 sm:px-4 py-2 text-xs sm:text-sm font-semibold rounded-full text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition-all cursor-pointer"
          @click="$emit('login')"
        >
          Log In
        </button>
        <button 
          class="px-4 sm:px-5 py-2 text-xs sm:text-sm font-semibold rounded-full bg-darkTeal text-white shadow-md shadow-darkTeal/20 hover:bg-darkTeal/90 hover:scale-[1.02] active:scale-[0.98] transition-all cursor-pointer"
          @click="$emit('register')"
        >
          Get Started
        </button>
      </div>

      <!-- Mobile Hamburger Button -->
      <div class="flex sm:hidden items-center gap-2">
        <button 
          class="px-3 py-1.5 text-xs font-semibold rounded-full bg-darkTeal text-white shadow-sm cursor-pointer"
          @click="$emit('register')"
        >
          Start Free
        </button>
        <button 
          class="w-8.5 h-8.5 rounded-xl flex items-center justify-center text-slate-700 hover:bg-slate-100 text-xl cursor-pointer"
          @click="isMobileMenuOpen = !isMobileMenuOpen"
          aria-label="Toggle navigation"
        >
          <i :class="isMobileMenuOpen ? 'mdi mdi-close' : 'mdi mdi-menu'"></i>
        </button>
      </div>
    </div>

    <!-- Mobile Dropdown Menu -->
    <div 
      v-if="isMobileMenuOpen" 
      class="md:hidden flex flex-col gap-3 pt-4 pb-2 border-t border-gray-100 mt-3 animate-fadeIn"
    >
      <a 
        href="#features" 
        class="text-sm text-slate-700 hover:text-darkTeal font-semibold py-1.5 px-2 rounded-lg hover:bg-slate-50 transition-colors"
        @click="isMobileMenuOpen = false"
      >
        Features
      </a>
      <a 
        href="#how-it-works" 
        class="text-sm text-slate-700 hover:text-darkTeal font-semibold py-1.5 px-2 rounded-lg hover:bg-slate-50 transition-colors"
        @click="isMobileMenuOpen = false"
      >
        How It Works
      </a>
      <a 
        href="#pricing" 
        class="text-sm text-slate-700 hover:text-darkTeal font-semibold py-1.5 px-2 rounded-lg hover:bg-slate-50 transition-colors"
        @click="isMobileMenuOpen = false"
      >
        Pricing
      </a>
      <div class="flex items-center gap-2 pt-2 border-t border-gray-100">
        <button 
          class="flex-1 py-2 text-xs font-bold rounded-full border border-gray-300 text-slate-700 hover:bg-slate-50"
          @click="$emit('login'); isMobileMenuOpen = false"
        >
          Log In
        </button>
        <button 
          class="flex-1 py-2 text-xs font-bold rounded-full bg-darkTeal text-white shadow"
          @click="$emit('register'); isMobileMenuOpen = false"
        >
          Get Started
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'

defineEmits(['login', 'register'])

const isMobileMenuOpen = ref(false)
</script>
