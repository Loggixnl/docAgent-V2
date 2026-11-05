<template>
  <section class="py-20 px-6 md:px-12 max-w-7xl mx-auto" id="pricing">
    <h2 class="text-3xl md:text-4xl font-extrabold font-heading text-center text-slate-900 mb-3">
      {{ $t('pricing.titleLine1') }} <span class="text-limeGreen">{{ $t('pricing.titleLine2') }}</span>
    </h2>
    <p class="text-xs md:text-sm text-slate-500 text-center max-w-xl mx-auto mb-16 leading-relaxed font-semibold">
      {{ $t('pricing.intro') }}
    </p>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
      <!-- Free Plan -->
      <div class="bg-white border border-gray-200 rounded-2xl p-8 flex flex-col relative group transition-all duration-300 hover:shadow-lg">
        <div class="text-sm font-bold text-slate-400 uppercase tracking-widest mb-2 font-heading">{{ $t('pricing.freeName') }}</div>
        <div class="text-4xl font-extrabold text-slate-900 font-heading mb-6 flex items-baseline gap-1">
          {{ $t('pricing.price0') }}<span class="text-xs text-slate-500 font-normal">{{ $t('pricing.perMonth') }}</span>
        </div>
        <ul class="space-y-3 mb-8 flex-grow">
          <li class="flex items-center gap-2.5 text-xs md:text-sm text-slate-600 font-medium">
            <i class="mdi mdi-check text-limeGreen"></i> {{ $t('pricing.freeF1') }}
          </li>
          <li class="flex items-center gap-2.5 text-xs md:text-sm text-slate-600 font-medium">
            <i class="mdi mdi-check text-limeGreen"></i> {{ $t('pricing.freeF2') }}
          </li>
          <li class="flex items-center gap-2.5 text-xs md:text-sm text-slate-600 font-medium">
            <i class="mdi mdi-check text-limeGreen"></i> {{ $t('pricing.freeF3') }}
          </li>
          <li class="flex items-center gap-2.5 text-xs md:text-sm text-slate-600 font-medium">
            <i class="mdi mdi-check text-limeGreen"></i> {{ $t('pricing.freeF4') }}
          </li>
        </ul>
        <button
          class="w-full py-3 text-xs font-bold rounded-full border border-gray-300 text-slate-700 hover:bg-slate-50 hover:border-gray-500 transition-all cursor-pointer"
          @click="$emit('selectPlan', 'free')"
        >
          {{ $t('pricing.freeCta') }}
        </button>
      </div>

      <!-- Pro Plan -->
      <div class="bg-white border-2 border-darkTeal rounded-2xl p-8 flex flex-col relative shadow-xl shadow-darkTeal/5 transition-all duration-300 hover:scale-[1.01]">
        <div class="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-0.5 rounded-full bg-coralOrange text-white text-[9px] font-extrabold uppercase tracking-wider">{{ $t('pricing.popular') }}</div>
        <div class="text-sm font-bold text-darkTeal uppercase tracking-widest mb-2 font-heading">{{ $t('pricing.proName') }}</div>
        <div class="text-4xl font-extrabold text-slate-900 font-heading mb-6 flex items-baseline gap-1">
          {{ $t('pricing.price49') }}<span class="text-xs text-slate-500 font-normal">{{ $t('pricing.perMonth') }}</span>
        </div>
        <ul class="space-y-3 mb-8 flex-grow">
          <li class="flex items-center gap-2.5 text-xs md:text-sm text-slate-700 font-bold">
            <i class="mdi mdi-check text-limeGreen"></i> {{ $t('pricing.proF1') }}
          </li>
          <li class="flex items-center gap-2.5 text-xs md:text-sm text-slate-600 font-medium">
            <i class="mdi mdi-check text-limeGreen"></i> {{ $t('pricing.proF2') }}
          </li>
          <li class="flex items-center gap-2.5 text-xs md:text-sm text-slate-600 font-medium">
            <i class="mdi mdi-check text-limeGreen"></i> {{ $t('pricing.proF3') }}
          </li>
          <li class="flex items-center gap-2.5 text-xs md:text-sm text-slate-600 font-medium">
            <i class="mdi mdi-check text-limeGreen"></i> {{ $t('pricing.proF4') }}
          </li>
          <li class="flex items-center gap-2.5 text-xs md:text-sm text-slate-600 font-medium">
            <i class="mdi mdi-check text-limeGreen"></i> {{ $t('pricing.proF5') }}
          </li>
        </ul>
        <button
          class="w-full py-3 text-xs font-bold rounded-full bg-darkTeal text-white shadow-md shadow-darkTeal/20 hover:bg-darkTeal/90 hover:scale-[1.02] transition-all cursor-pointer"
          @click="$emit('selectPlan', 'pro')"
        >
          {{ $t('pricing.proCta') }}
        </button>
      </div>

      <!-- Enterprise -->
      <div class="bg-white border border-gray-200 rounded-2xl p-8 flex flex-col relative group transition-all duration-300 hover:shadow-lg">
        <div class="text-sm font-bold text-slate-400 uppercase tracking-widest mb-2 font-heading">{{ $t('pricing.entName') }}</div>
        <div class="text-4xl font-extrabold text-slate-900 font-heading mb-6 flex items-baseline gap-1">
          {{ $t('pricing.customPrice') }}
        </div>
        <ul class="space-y-3 mb-8 flex-grow">
          <li class="flex items-center gap-2.5 text-xs md:text-sm text-slate-600 font-medium">
            <i class="mdi mdi-check text-limeGreen"></i> {{ $t('pricing.entF1') }}
          </li>
          <li class="flex items-center gap-2.5 text-xs md:text-sm text-slate-600 font-medium">
            <i class="mdi mdi-check text-limeGreen"></i> {{ $t('pricing.entF2') }}
          </li>
          <li class="flex items-center gap-2.5 text-xs md:text-sm text-slate-600 font-medium">
            <i class="mdi mdi-check text-limeGreen"></i> {{ $t('pricing.entF3') }}
          </li>
          <li class="flex items-center gap-2.5 text-xs md:text-sm text-slate-600 font-medium">
            <i class="mdi mdi-check text-limeGreen"></i> {{ $t('pricing.entF4') }}
          </li>
        </ul>
        <button
          class="w-full py-3 text-xs font-bold rounded-full border border-gray-300 text-slate-700 hover:bg-slate-50 hover:border-gray-500 transition-all cursor-pointer"
          @click="$emit('selectPlan', 'enterprise')"
        >
          {{ $t('pricing.entCta') }}
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
defineEmits(['selectPlan'])
</script>
