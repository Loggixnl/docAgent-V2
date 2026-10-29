<template>
  <section class="py-12 lg:py-20 px-6 md:px-12 max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-16 items-center flex-grow">
    <div class="flex flex-col items-start text-left">
      <!-- Rounded Outline Badge with green dot -->
      <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white border border-gray-300/80 text-xs font-bold text-slate-700 mb-5 shadow-xs">
        <span class="w-2.5 h-2.5 rounded-full bg-limeGreen animate-pulse"></span>
        <span class="text-darkTeal font-extrabold uppercase tracking-wider text-[10px]">New Feature</span>
        <span class="text-slate-300">|</span>
        <span>Session-Based AI Question Management & Admin Dashboard</span>
      </div>
      
      <!-- Main Header Title -->
      <h2 class="text-3xl md:text-5xl lg:text-5xl font-black font-heading leading-tight tracking-tight text-slate-900 mb-5">
        Intelligent Policy Chatbot & <span class="text-darkTeal block mt-1">Question Management System</span>
      </h2>
      
      <p class="text-xs md:text-sm text-slate-600 leading-relaxed mb-6 max-w-xl font-medium">
        Empower employees with instant answers from company handbooks or general workplace guidance. Every question is captured with full session tracking, auto-classification, and an <strong>Admin Dashboard</strong> for review, verification, and resolution.
      </p>

      <!-- Key Capabilities Highlights -->
      <div class="grid grid-cols-2 gap-2.5 mb-8 w-full max-w-lg">
        <div class="flex items-center gap-2 p-2 rounded-xl bg-white border border-gray-200/80 text-xs font-semibold text-slate-700 shadow-xs">
          <i class="mdi mdi-forum-outline text-darkTeal text-base"></i>
          <span>Multi-Session Chats</span>
        </div>
        <div class="flex items-center gap-2 p-2 rounded-xl bg-white border border-gray-200/80 text-xs font-semibold text-slate-700 shadow-xs">
          <i class="mdi mdi-file-document-check-outline text-darkTeal text-base"></i>
          <span>Doc & General Q&A</span>
        </div>
        <div class="flex items-center gap-2 p-2 rounded-xl bg-white border border-gray-200/80 text-xs font-semibold text-slate-700 shadow-xs">
          <i class="mdi mdi-view-dashboard-outline text-darkTeal text-base"></i>
          <span>Admin Review Dashboard</span>
        </div>
        <div class="flex items-center gap-2 p-2 rounded-xl bg-white border border-gray-200/80 text-xs font-semibold text-slate-700 shadow-xs">
          <i class="mdi mdi-check-decagram-outline text-emerald-600 text-base"></i>
          <span>Resolution Lifecycle</span>
        </div>
      </div>
      
      <div class="flex flex-wrap gap-4 items-center">
        <button 
          class="px-6 py-3 text-sm font-bold rounded-full bg-gradient-to-r from-lightTeal to-darkTeal text-white shadow-lg shadow-darkTeal/20 hover:opacity-95 hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center gap-2 cursor-pointer"
          @click="$emit('register')"
        >
          <span>Get Started Free</span>
          <i class="mdi mdi-arrow-right text-xs"></i>
        </button>
        
        <div class="flex items-center gap-2 ml-1">
          <span class="text-xs text-slate-400 font-semibold uppercase tracking-wider">Powered by</span>
          <span class="text-xs font-bold text-slate-700 flex items-center gap-1 font-heading">
            <i class="mdi mdi-brain text-darkTeal"></i> Advanced AI
          </span>
        </div>
      </div>
    </div>
    
    <!-- Hero Mockup: Showing Sessions, Question Types, Statuses, and Admin Response -->
    <div class="w-full relative">
      <div class="absolute -inset-1 rounded-2xl bg-gradient-to-tr from-lightTeal to-darkTeal opacity-10 blur-xl"></div>
      <div class="relative bg-white border border-gray-200 rounded-2xl overflow-hidden shadow-2xl transition-all duration-500 hover:scale-[1.01]">
        <!-- Mockup Header -->
        <div class="bg-slate-50 py-2.5 px-4 border-b border-gray-200/80 flex items-center justify-between">
          <div class="flex items-center gap-2">
            <div class="flex gap-1.5">
              <span class="w-2.5 h-2.5 rounded-full bg-red-400"></span>
              <span class="w-2.5 h-2.5 rounded-full bg-yellow-400"></span>
              <span class="w-2.5 h-2.5 rounded-full bg-limeGreen"></span>
            </div>
            <span class="text-[10px] text-slate-500 font-bold tracking-wider uppercase font-heading ml-2">DocAgent AI Workspace & Admin</span>
          </div>
          <span class="px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 text-[9px] font-extrabold uppercase">
            Live Preview
          </span>
        </div>
        
        <!-- Mockup Body with Sidebar and Chat Area -->
        <div class="grid grid-cols-[140px_1fr] h-[340px] bg-white">
          <!-- Left Mock Sessions Sidebar -->
          <div class="bg-slate-50 border-r border-gray-200/70 p-2.5 flex flex-col justify-between">
            <div class="space-y-1.5">
              <button class="w-full py-1.5 px-2 rounded-lg bg-darkTeal text-white text-[10px] font-bold flex items-center justify-center gap-1 shadow-xs">
                <i class="mdi mdi-plus"></i> New Chat
              </button>
              
              <div class="text-[8px] font-bold text-slate-400 uppercase tracking-wider pt-1">Past Sessions</div>
              <div class="p-1.5 rounded-lg bg-lightTeal/15 border border-lightTeal/30 text-[9px] font-bold text-darkTeal truncate">
                💬 Vacation & Leave
              </div>
              <div class="p-1.5 rounded-lg hover:bg-slate-100 text-[9px] font-semibold text-slate-600 truncate">
                💬 Code of Conduct
              </div>
              <div class="p-1.5 rounded-lg hover:bg-slate-100 text-[9px] font-semibold text-slate-600 truncate">
                💡 Career Mentorship
              </div>
            </div>

            <!-- Admin Dashboard Toggle in Mockup -->
            <div class="p-1.5 rounded-lg bg-darkTeal/10 text-darkTeal text-[9px] font-bold flex items-center justify-between">
              <span>Admin Board</span>
              <i class="mdi mdi-chart-box-outline"></i>
            </div>
          </div>

          <!-- Right Mock Chat Window -->
          <div class="flex flex-col h-full bg-slate-50/20">
            <!-- Mock Header -->
            <div class="bg-white py-2 px-3 border-b border-gray-200/50 text-[10px] font-bold text-slate-800 flex items-center justify-between">
              <div class="flex items-center gap-1.5">
                <div class="w-5 h-5 rounded-md bg-lightTeal/20 text-darkTeal flex items-center justify-center text-xs">
                  <i class="mdi mdi-robot-outline"></i>
                </div>
                <span>Session: Vacation & Leave</span>
              </div>
              <span class="text-[8px] px-1.5 py-0.5 rounded-full bg-lightTeal/15 text-darkTeal font-extrabold">
                Session Active
              </span>
            </div>

            <!-- Messages Stream -->
            <div class="p-3 flex flex-col gap-2.5 overflow-y-auto flex-grow justify-start">
              <!-- User Message -->
              <div class="text-[10px] p-2.5 rounded-xl bg-slate-100 border border-gray-200 text-slate-800 self-end rounded-tr-none max-w-[90%] font-medium">
                Can I carry over unused vacation days into next year?
              </div>

              <!-- AI Answer Bubble with Badge & Status -->
              <div class="text-[10px] p-2.5 rounded-xl bg-white border border-gray-200 text-slate-800 self-start rounded-tl-none max-w-[95%] shadow-xs">
                <!-- Metadata Badges -->
                <div class="flex items-center justify-between gap-1 mb-1.5 text-[8px]">
                  <span class="px-1.5 py-0.2 rounded-full bg-lightTeal/15 text-darkTeal font-extrabold">
                    📄 Document Policy
                  </span>
                  <span class="px-1.5 py-0.2 rounded-full bg-blue-100 text-blue-800 font-bold uppercase">
                    AI Answered
                  </span>
                </div>
                
                <p class="leading-relaxed">
                  According to <strong>Handbook Section 3.1</strong>, up to 10 days of unused leave automatically carry forward.
                </p>

                <!-- Official Admin Response Box inside mock -->
                <div class="mt-2 pt-2 border-t border-emerald-200 bg-emerald-50/80 -mx-2.5 -mb-2.5 p-2 rounded-b-xl">
                  <div class="flex items-center gap-1 text-[9px] font-black text-emerald-800 mb-0.5">
                    <i class="mdi mdi-shield-check text-emerald-600"></i>
                    <span>Official HR Admin Response</span>
                    <span class="ml-auto text-[7px] bg-emerald-200 text-emerald-900 px-1 rounded font-extrabold uppercase">Resolved</span>
                  </div>
                  <p class="text-[9px] text-emerald-950 font-medium">
                    Reviewed & verified: You have 8 days eligible for automatic rollover.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
defineEmits(['register'])
</script>
