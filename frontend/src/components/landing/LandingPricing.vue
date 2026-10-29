<template>
  <section class="py-20 px-6 md:px-12 max-w-7xl mx-auto" id="pricing">
    <h2 class="text-3xl md:text-4xl font-extrabold font-heading text-center text-slate-900 mb-3">
      Flexible <span class="text-limeGreen">SaaS Plans</span>
    </h2>
    <p class="text-xs md:text-sm text-slate-500 text-center max-w-xl mx-auto mb-16 leading-relaxed font-semibold">
      Choose the package that works best for your team's document intelligence needs.
    </p>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
      <!-- Free Plan -->
      <div class="bg-white border border-gray-200 rounded-2xl p-8 flex flex-col relative group transition-all duration-300 hover:shadow-lg">
        <div class="text-sm font-bold text-slate-400 uppercase tracking-widest mb-2 font-heading">Free Plan</div>
        <div class="text-4xl font-extrabold text-slate-900 font-heading mb-6 flex items-baseline gap-1">
          $0<span class="text-xs text-slate-500 font-normal">/month</span>
        </div>
        <ul class="space-y-3 mb-8 flex-grow">
          <li class="flex items-center gap-2.5 text-xs md:text-sm text-slate-600 font-medium">
            <i class="mdi mdi-check text-limeGreen"></i> 1 Active Chatbot ID
          </li>
          <li class="flex items-center gap-2.5 text-xs md:text-sm text-slate-600 font-medium">
            <i class="mdi mdi-check text-limeGreen"></i> Up to 5 PDF/TXT Files
          </li>
          <li class="flex items-center gap-2.5 text-xs md:text-sm text-slate-600 font-medium">
            <i class="mdi mdi-check text-limeGreen"></i> Advanced AI Models
          </li>
          <li class="flex items-center gap-2.5 text-xs md:text-sm text-slate-600 font-medium">
            <i class="mdi mdi-check text-limeGreen"></i> Basic Chatbot Widget
          </li>
        </ul>
        <button 
          class="w-full py-3 text-xs font-bold rounded-full border border-gray-300 text-slate-700 hover:bg-slate-50 hover:border-gray-500 transition-all cursor-pointer"
          @click="$emit('selectPlan', 'free')"
        >
          Get Started Free
        </button>
      </div>

      <!-- Pro Plan -->
      <div class="bg-white border-2 border-darkTeal rounded-2xl p-8 flex flex-col relative shadow-xl shadow-darkTeal/5 transition-all duration-300 hover:scale-[1.01]">
        <div class="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-0.5 rounded-full bg-coralOrange text-white text-[9px] font-extrabold uppercase tracking-wider">Popular</div>
        <div class="text-sm font-bold text-darkTeal uppercase tracking-widest mb-2 font-heading">Pro Plan</div>
        <div class="text-4xl font-extrabold text-slate-900 font-heading mb-6 flex items-baseline gap-1">
          $49<span class="text-xs text-slate-500 font-normal">/month</span>
        </div>
        <ul class="space-y-3 mb-8 flex-grow">
          <li class="flex items-center gap-2.5 text-xs md:text-sm text-slate-700 font-bold">
            <i class="mdi mdi-check text-limeGreen"></i> Unlimited Uploads
          </li>
          <li class="flex items-center gap-2.5 text-xs md:text-sm text-slate-600 font-medium">
            <i class="mdi mdi-check text-limeGreen"></i> Pro & Standard AI Models
          </li>
          <li class="flex items-center gap-2.5 text-xs md:text-sm text-slate-600 font-medium">
            <i class="mdi mdi-check text-limeGreen"></i> Custom Theme Widgets
          </li>
          <li class="flex items-center gap-2.5 text-xs md:text-sm text-slate-600 font-medium">
            <i class="mdi mdi-check text-limeGreen"></i> Analytics Dashboard
          </li>
          <li class="flex items-center gap-2.5 text-xs md:text-sm text-slate-600 font-medium">
            <i class="mdi mdi-check text-limeGreen"></i> Priority API Access
          </li>
        </ul>
        <button 
          class="w-full py-3 text-xs font-bold rounded-full bg-darkTeal text-white shadow-md shadow-darkTeal/20 hover:bg-darkTeal/90 hover:scale-[1.02] transition-all cursor-pointer"
          @click="$emit('selectPlan', 'pro')"
        >
          Upgrade to Pro
        </button>
      </div>

      <!-- Enterprise -->
      <div class="bg-white border border-gray-200 rounded-2xl p-8 flex flex-col relative group transition-all duration-300 hover:shadow-lg">
        <div class="text-sm font-bold text-slate-400 uppercase tracking-widest mb-2 font-heading">Enterprise</div>
        <div class="text-4xl font-extrabold text-slate-900 font-heading mb-6 flex items-baseline gap-1">
          Custom
        </div>
        <ul class="space-y-3 mb-8 flex-grow">
          <li class="flex items-center gap-2.5 text-xs md:text-sm text-slate-600 font-medium">
            <i class="mdi mdi-check text-limeGreen"></i> Isolated DB Instance
          </li>
          <li class="flex items-center gap-2.5 text-xs md:text-sm text-slate-600 font-medium">
            <i class="mdi mdi-check text-limeGreen"></i> Dedicated SLA Support
          </li>
          <li class="flex items-center gap-2.5 text-xs md:text-sm text-slate-600 font-medium">
            <i class="mdi mdi-check text-limeGreen"></i> Custom Fine-Tuning
          </li>
          <li class="flex items-center gap-2.5 text-xs md:text-sm text-slate-600 font-medium">
            <i class="mdi mdi-check text-limeGreen"></i> Custom Domain Embeds
          </li>
        </ul>
        <button 
          class="w-full py-3 text-xs font-bold rounded-full border border-gray-300 text-slate-700 hover:bg-slate-50 hover:border-gray-500 transition-all cursor-pointer"
          @click="$emit('selectPlan', 'enterprise')"
        >
          Contact Sales
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
defineEmits(['selectPlan'])
</script>
