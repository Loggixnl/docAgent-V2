<template>
  <div
    class="inline-flex items-center rounded-full border border-slate-200 bg-white/90 p-0.5 shadow-xs"
    role="group"
    aria-label="Language"
  >
    <button
      v-for="option in options"
      :key="option.code"
      type="button"
      class="px-2.5 py-1 text-[11px] font-bold rounded-full transition-all cursor-pointer"
      :class="lang === option.code
        ? 'bg-darkTeal text-white shadow-sm'
        : 'text-slate-500 hover:text-slate-800 hover:bg-slate-100'"
      :aria-pressed="lang === option.code"
      @click="setLang(option.code)"
    >
      {{ option.label }}
    </button>
  </div>
</template>

<script setup>
import { useLanguage } from '../../composables/useLanguage'

const { lang, setLang } = useLanguage()

const options = [
  { code: 'en', label: 'EN' },
  { code: 'nl', label: 'NL' }
]
</script>
