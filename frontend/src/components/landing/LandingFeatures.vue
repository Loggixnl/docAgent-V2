<template>
  <section class="py-16 md:py-24 px-6 md:px-12 max-w-7xl mx-auto border-t border-gray-300/40" id="features">
    <div class="text-center max-w-3xl mx-auto mb-16">
      <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-lightTeal/15 text-darkTeal text-[10px] font-extrabold uppercase tracking-widest mb-3">
        Next-Generation Enterprise AI
      </div>
      <h2 class="text-3xl md:text-4xl font-extrabold font-heading text-slate-900 mb-4">
        Complete AI Question & <span class="text-darkTeal">Session Management</span>
      </h2>
      <p class="text-xs md:text-sm text-slate-500 leading-relaxed font-semibold">
        Go beyond simple answers. Turn company policies into a fully auditable, session-tracked question management system with administrative oversight and resolution workflows.
      </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- Feature 1: Session-Based Chat -->
      <div class="bg-white border border-gray-200/90 hover:border-lightTeal/60 rounded-2xl p-6 transition-all duration-300 group shadow-xs hover:shadow-md">
        <div class="w-12 h-12 rounded-xl bg-lightTeal/10 flex items-center justify-center text-2xl text-darkTeal mb-4 group-hover:bg-darkTeal group-hover:text-white transition-all shadow-inner">
          <i class="mdi mdi-forum-outline"></i>
        </div>
        <div class="flex items-center gap-2 mb-2">
          <h3 class="text-base font-bold text-slate-900 font-heading">Multi-Session Chats</h3>
          <span class="text-[9px] px-2 py-0.5 rounded-full bg-limeGreen/15 text-limeGreen font-extrabold uppercase">New</span>
        </div>
        <p class="text-xs text-slate-500 leading-relaxed font-medium">
          Start distinct conversations with <strong>+ New Chat</strong>. Each conversation receives a unique <strong>Session ID</strong>, allowing users to browse, switch, and resume past chats seamlessly.
        </p>
      </div>

      <!-- Feature 2: Dual Question Routing -->
      <div class="bg-white border border-gray-200/90 hover:border-lightTeal/60 rounded-2xl p-6 transition-all duration-300 group shadow-xs hover:shadow-md">
        <div class="w-12 h-12 rounded-xl bg-indigo-50 flex items-center justify-center text-2xl text-indigo-600 mb-4 group-hover:bg-indigo-600 group-hover:text-white transition-all shadow-inner">
          <i class="mdi mdi-vector-intersection"></i>
        </div>
        <div class="flex items-center gap-2 mb-2">
          <h3 class="text-base font-bold text-slate-900 font-heading">Document & General Q&A</h3>
          <span class="text-[9px] px-2 py-0.5 rounded-full bg-indigo-100 text-indigo-700 font-extrabold uppercase">Dual AI</span>
        </div>
        <p class="text-xs text-slate-500 leading-relaxed font-medium">
          Automatically classifies incoming queries. Answers policy-specific questions directly from uploaded handbooks or provides intelligent general HR & workplace advice.
        </p>
      </div>

      <!-- Feature 3: Question Lifecycle Management -->
      <div class="bg-white border border-gray-200/90 hover:border-lightTeal/60 rounded-2xl p-6 transition-all duration-300 group shadow-xs hover:shadow-md">
        <div class="w-12 h-12 rounded-xl bg-emerald-50 flex items-center justify-center text-2xl text-emerald-600 mb-4 group-hover:bg-emerald-600 group-hover:text-white transition-all shadow-inner">
          <i class="mdi mdi-progress-check"></i>
        </div>
        <div class="flex items-center gap-2 mb-2">
          <h3 class="text-base font-bold text-slate-900 font-heading">Question Lifecycle</h3>
          <span class="text-[9px] px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 font-extrabold uppercase">Full Audit</span>
        </div>
        <p class="text-xs text-slate-500 leading-relaxed font-medium">
          Every query logs Question ID, Session ID, User, Type, AI Response, Sources, and Lifecycle Status: <strong>New, AI Answered, Needs Review, Admin Answered, and Resolved</strong>.
        </p>
      </div>

      <!-- Feature 4: Admin Review & Response Dashboard -->
      <div class="bg-white border border-gray-200/90 hover:border-lightTeal/60 rounded-2xl p-6 transition-all duration-300 group shadow-xs hover:shadow-md">
        <div class="w-12 h-12 rounded-xl bg-purple-50 flex items-center justify-center text-2xl text-purple-600 mb-4 group-hover:bg-purple-600 group-hover:text-white transition-all shadow-inner">
          <i class="mdi mdi-shield-account-outline"></i>
        </div>
        <div class="flex items-center gap-2 mb-2">
          <h3 class="text-base font-bold text-slate-900 font-heading">Admin Review Dashboard</h3>
          <span class="text-[9px] px-2 py-0.5 rounded-full bg-purple-100 text-purple-700 font-extrabold uppercase">Admin Suite</span>
        </div>
        <p class="text-xs text-slate-500 leading-relaxed font-medium">
          Admins can search & filter questions, inspect full conversational threads, provide official HR responses, and mark employee inquiries as verified or resolved.
        </p>
      </div>

      <!-- Feature 5: Real-time Analytics -->
      <div class="bg-white border border-gray-200/90 hover:border-lightTeal/60 rounded-2xl p-6 transition-all duration-300 group shadow-xs hover:shadow-md">
        <div class="w-12 h-12 rounded-xl bg-amber-50 flex items-center justify-center text-2xl text-amber-600 mb-4 group-hover:bg-amber-600 group-hover:text-white transition-all shadow-inner">
          <i class="mdi mdi-chart-box-outline"></i>
        </div>
        <h3 class="text-base font-bold text-slate-900 mb-2 font-heading">Live Management Analytics</h3>
        <p class="text-xs text-slate-500 leading-relaxed font-medium">
          Monitor total sessions, total questions, unanswered queries, questions needing human review, and Document vs General question breakdown in real time.
        </p>
      </div>

      <!-- Feature 6: Zero-Code Embed Widget -->
      <div class="bg-white border border-gray-200/90 hover:border-lightTeal/60 rounded-2xl p-6 transition-all duration-300 group shadow-xs hover:shadow-md">
        <div class="w-12 h-12 rounded-xl bg-lightTeal/10 flex items-center justify-center text-2xl text-darkTeal mb-4 group-hover:bg-darkTeal group-hover:text-white transition-all shadow-inner">
          <i class="mdi mdi-code-tags"></i>
        </div>
        <h3 class="text-base font-bold text-slate-900 mb-2 font-heading">Zero-Code Embed Widget</h3>
        <p class="text-xs text-slate-500 leading-relaxed font-medium">
          Deploy your policy chatbot anywhere with a single script tag. Compatible with internal intranets, portals, WordPress, Notion, and custom web apps.
        </p>
      </div>
    </div>
  </section>
</template>
