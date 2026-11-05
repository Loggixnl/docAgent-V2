<template>
  <section class="py-16 md:py-24 px-6 md:px-12 max-w-7xl mx-auto border-t border-gray-300/40" id="features">
    <div class="text-center max-w-3xl mx-auto mb-16">
      <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-lightTeal/15 text-darkTeal text-[10px] font-extrabold uppercase tracking-widest mb-3">
        {{ $t('features.eyebrow') }}
      </div>
      <h2 class="text-3xl md:text-4xl font-extrabold font-heading text-slate-900 mb-4">
        {{ $t('features.titleLine1') }} <span class="text-darkTeal">{{ $t('features.titleLine2') }}</span>
      </h2>
      <p class="text-xs md:text-sm text-slate-500 leading-relaxed font-semibold">
        {{ $t('features.intro') }}
      </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- Feature 1: Session-Based Chat -->
      <div class="bg-white border border-gray-200/90 hover:border-lightTeal/60 rounded-2xl p-6 transition-all duration-300 group shadow-xs hover:shadow-md">
        <div class="w-12 h-12 rounded-xl bg-lightTeal/10 flex items-center justify-center text-2xl text-darkTeal mb-4 group-hover:bg-darkTeal group-hover:text-white transition-all shadow-inner">
          <i class="mdi mdi-forum-outline"></i>
        </div>
        <div class="flex items-center gap-2 mb-2">
          <h3 class="text-base font-bold text-slate-900 font-heading">{{ $t('features.card1Title') }}</h3>
          <span class="text-[9px] px-2 py-0.5 rounded-full bg-limeGreen/15 text-limeGreen font-extrabold uppercase">{{ $t('features.card1Badge') }}</span>
        </div>
        <p class="text-xs text-slate-500 leading-relaxed font-medium" v-html="$t('features.card1Body')"></p>
      </div>

      <!-- Feature 2: Dual Question Routing -->
      <div class="bg-white border border-gray-200/90 hover:border-lightTeal/60 rounded-2xl p-6 transition-all duration-300 group shadow-xs hover:shadow-md">
        <div class="w-12 h-12 rounded-xl bg-indigo-50 flex items-center justify-center text-2xl text-indigo-600 mb-4 group-hover:bg-indigo-600 group-hover:text-white transition-all shadow-inner">
          <i class="mdi mdi-vector-intersection"></i>
        </div>
        <div class="flex items-center gap-2 mb-2">
          <h3 class="text-base font-bold text-slate-900 font-heading">{{ $t('features.card2Title') }}</h3>
          <span class="text-[9px] px-2 py-0.5 rounded-full bg-indigo-100 text-indigo-700 font-extrabold uppercase">{{ $t('features.card2Badge') }}</span>
        </div>
        <p class="text-xs text-slate-500 leading-relaxed font-medium">{{ $t('features.card2Body') }}</p>
      </div>

      <!-- Feature 3: Question Lifecycle Management -->
      <div class="bg-white border border-gray-200/90 hover:border-lightTeal/60 rounded-2xl p-6 transition-all duration-300 group shadow-xs hover:shadow-md">
        <div class="w-12 h-12 rounded-xl bg-emerald-50 flex items-center justify-center text-2xl text-emerald-600 mb-4 group-hover:bg-emerald-600 group-hover:text-white transition-all shadow-inner">
          <i class="mdi mdi-progress-check"></i>
        </div>
        <div class="flex items-center gap-2 mb-2">
          <h3 class="text-base font-bold text-slate-900 font-heading">{{ $t('features.card3Title') }}</h3>
          <span class="text-[9px] px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 font-extrabold uppercase">{{ $t('features.card3Badge') }}</span>
        </div>
        <p class="text-xs text-slate-500 leading-relaxed font-medium" v-html="$t('features.card3Body')"></p>
      </div>

      <!-- Feature 4: Admin Review & Response Dashboard -->
      <div class="bg-white border border-gray-200/90 hover:border-lightTeal/60 rounded-2xl p-6 transition-all duration-300 group shadow-xs hover:shadow-md">
        <div class="w-12 h-12 rounded-xl bg-purple-50 flex items-center justify-center text-2xl text-purple-600 mb-4 group-hover:bg-purple-600 group-hover:text-white transition-all shadow-inner">
          <i class="mdi mdi-shield-account-outline"></i>
        </div>
        <div class="flex items-center gap-2 mb-2">
          <h3 class="text-base font-bold text-slate-900 font-heading">{{ $t('features.card4Title') }}</h3>
          <span class="text-[9px] px-2 py-0.5 rounded-full bg-purple-100 text-purple-700 font-extrabold uppercase">{{ $t('features.card4Badge') }}</span>
        </div>
        <p class="text-xs text-slate-500 leading-relaxed font-medium">{{ $t('features.card4Body') }}</p>
      </div>

      <!-- Feature 5: Real-time Analytics -->
      <div class="bg-white border border-gray-200/90 hover:border-lightTeal/60 rounded-2xl p-6 transition-all duration-300 group shadow-xs hover:shadow-md">
        <div class="w-12 h-12 rounded-xl bg-amber-50 flex items-center justify-center text-2xl text-amber-600 mb-4 group-hover:bg-amber-600 group-hover:text-white transition-all shadow-inner">
          <i class="mdi mdi-chart-box-outline"></i>
        </div>
        <h3 class="text-base font-bold text-slate-900 mb-2 font-heading">{{ $t('features.card5Title') }}</h3>
        <p class="text-xs text-slate-500 leading-relaxed font-medium">{{ $t('features.card5Body') }}</p>
      </div>

      <!-- Feature 6: Zero-Code Embed Widget -->
      <div class="bg-white border border-gray-200/90 hover:border-lightTeal/60 rounded-2xl p-6 transition-all duration-300 group shadow-xs hover:shadow-md">
        <div class="w-12 h-12 rounded-xl bg-lightTeal/10 flex items-center justify-center text-2xl text-darkTeal mb-4 group-hover:bg-darkTeal group-hover:text-white transition-all shadow-inner">
          <i class="mdi mdi-code-tags"></i>
        </div>
        <h3 class="text-base font-bold text-slate-900 mb-2 font-heading">{{ $t('features.card6Title') }}</h3>
        <p class="text-xs text-slate-500 leading-relaxed font-medium">{{ $t('features.card6Body') }}</p>
      </div>
    </div>
  </section>
</template>
