<template>
  <section class="py-16 md:py-24 bg-white border-y border-gray-200/60" id="how-it-works">
    <div class="max-w-7xl mx-auto px-6 md:px-12">
      <div class="text-center max-w-3xl mx-auto mb-16">
        <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-[10px] font-extrabold uppercase tracking-widest mb-3">
          End-to-End Workflow
        </div>
        <h2 class="text-3xl md:text-4xl font-extrabold font-heading text-slate-900 mb-4">
          How the <span class="text-darkTeal">Question Management System</span> Works
        </h2>
        <p class="text-xs md:text-sm text-slate-500 leading-relaxed font-semibold">
          From the initial user inquiry to administrative review and final resolution, every step is automated, tracked, and verifiable.
        </p>
      </div>

      <!-- Linear Workflow Diagram / Stepper -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 relative">
        <!-- Step 1: User & Session -->
        <div class="bg-slate-50 border border-gray-200 rounded-2xl p-6 relative flex flex-col justify-between group hover:border-lightTeal/60 transition-all shadow-xs hover:shadow-sm">
          <div>
            <div class="flex items-center justify-between mb-4">
              <span class="w-8 h-8 rounded-xl bg-lightTeal text-white font-black flex items-center justify-center text-xs">
                01
              </span>
              <span class="text-[9px] font-extrabold uppercase tracking-wider text-slate-400">Step 1</span>
            </div>
            <h3 class="text-sm font-bold text-slate-900 mb-1.5 font-heading">User & Session</h3>
            <p class="text-xs text-slate-500 leading-relaxed font-medium">
              An employee logs in or opens the widget and starts a <strong>New Chat</strong>. A dedicated <strong>Session ID</strong> is created to group all related queries.
            </p>
          </div>
          <div class="mt-4 pt-3 border-t border-gray-200/60 flex items-center gap-1.5 text-[10px] text-darkTeal font-bold">
            <i class="mdi mdi-forum-outline"></i>
            <span>Session Initialized</span>
          </div>
        </div>

        <!-- Step 2: Question & AI Response -->
        <div class="bg-slate-50 border border-gray-200 rounded-2xl p-6 relative flex flex-col justify-between group hover:border-lightTeal/60 transition-all shadow-xs hover:shadow-sm">
          <div>
            <div class="flex items-center justify-between mb-4">
              <span class="w-8 h-8 rounded-xl bg-indigo-500 text-white font-black flex items-center justify-center text-xs">
                02
              </span>
              <span class="text-[9px] font-extrabold uppercase tracking-wider text-slate-400">Step 2</span>
            </div>
            <h3 class="text-sm font-bold text-slate-900 mb-1.5 font-heading">Question & AI Response</h3>
            <p class="text-xs text-slate-500 leading-relaxed font-medium">
              AI classifies the query as <strong>Document</strong> or <strong>General</strong>, generates an immediate response citing clauses, logs Question ID, and sets status to <em>AI Answered</em>.
            </p>
          </div>
          <div class="mt-4 pt-3 border-t border-gray-200/60 flex items-center gap-1.5 text-[10px] text-indigo-600 font-bold">
            <i class="mdi mdi-robot-outline"></i>
            <span>AI Answer Generated</span>
          </div>
        </div>

        <!-- Step 3: Admin Dashboard Oversight -->
        <div class="bg-slate-50 border border-gray-200 rounded-2xl p-6 relative flex flex-col justify-between group hover:border-lightTeal/60 transition-all shadow-xs hover:shadow-sm">
          <div>
            <div class="flex items-center justify-between mb-4">
              <span class="w-8 h-8 rounded-xl bg-purple-600 text-white font-black flex items-center justify-center text-xs">
                03
              </span>
              <span class="text-[9px] font-extrabold uppercase tracking-wider text-slate-400">Step 3</span>
            </div>
            <h3 class="text-sm font-bold text-slate-900 mb-1.5 font-heading">Dashboard Oversight</h3>
            <p class="text-xs text-slate-500 leading-relaxed font-medium">
              HR Administrators monitor incoming questions in real time. They can search questions, inspect full conversational threads, and flag queries that require human attention.
            </p>
          </div>
          <div class="mt-4 pt-3 border-t border-gray-200/60 flex items-center gap-1.5 text-[10px] text-purple-700 font-bold">
            <i class="mdi mdi-view-dashboard-outline"></i>
            <span>Live Audit & Tracking</span>
          </div>
        </div>

        <!-- Step 4: Admin Review & Resolution -->
        <div class="bg-slate-50 border border-gray-200 rounded-2xl p-6 relative flex flex-col justify-between group hover:border-lightTeal/60 transition-all shadow-xs hover:shadow-sm">
          <div>
            <div class="flex items-center justify-between mb-4">
              <span class="w-8 h-8 rounded-xl bg-emerald-600 text-white font-black flex items-center justify-center text-xs">
                04
              </span>
              <span class="text-[9px] font-extrabold uppercase tracking-wider text-slate-400">Step 4</span>
            </div>
            <h3 class="text-sm font-bold text-slate-900 mb-1.5 font-heading">Admin Review & Resolution</h3>
            <p class="text-xs text-slate-500 leading-relaxed font-medium">
              Admins write official guidance, provide approvals or policy clarifications, and mark the question as <strong>Admin Answered</strong> or <strong>Resolved</strong>.
            </p>
          </div>
          <div class="mt-4 pt-3 border-t border-gray-200/60 flex items-center gap-1.5 text-[10px] text-emerald-700 font-bold">
            <i class="mdi mdi-check-decagram-outline"></i>
            <span>Verified & Resolved</span>
          </div>
        </div>
      </div>

      <!-- Flow Summary Strip -->
      <div class="mt-10 p-4 rounded-2xl bg-slate-100 border border-gray-200/80 flex flex-wrap items-center justify-center gap-3 text-xs font-bold text-slate-700">
        <span class="px-2.5 py-1 rounded-lg bg-white border border-gray-200 shadow-xs flex items-center gap-1">
          <i class="mdi mdi-account text-darkTeal"></i> User
        </span>
        <i class="mdi mdi-arrow-right text-slate-400 text-sm"></i>
        <span class="px-2.5 py-1 rounded-lg bg-white border border-gray-200 shadow-xs flex items-center gap-1">
          <i class="mdi mdi-forum-outline text-darkTeal"></i> Session
        </span>
        <i class="mdi mdi-arrow-right text-slate-400 text-sm"></i>
        <span class="px-2.5 py-1 rounded-lg bg-white border border-gray-200 shadow-xs flex items-center gap-1">
          <i class="mdi mdi-help-circle-outline text-indigo-600"></i> Question
        </span>
        <i class="mdi mdi-arrow-right text-slate-400 text-sm"></i>
        <span class="px-2.5 py-1 rounded-lg bg-white border border-gray-200 shadow-xs flex items-center gap-1">
          <i class="mdi mdi-robot-outline text-lightTeal"></i> AI Response
        </span>
        <i class="mdi mdi-arrow-right text-slate-400 text-sm"></i>
        <span class="px-2.5 py-1 rounded-lg bg-white border border-gray-200 shadow-xs flex items-center gap-1">
          <i class="mdi mdi-view-dashboard-outline text-purple-600"></i> Dashboard
        </span>
        <i class="mdi mdi-arrow-right text-slate-400 text-sm"></i>
        <span class="px-2.5 py-1 rounded-lg bg-white border border-gray-200 shadow-xs flex items-center gap-1">
          <i class="mdi mdi-shield-check text-purple-600"></i> Admin Review
        </span>
        <i class="mdi mdi-arrow-right text-slate-400 text-sm"></i>
        <span class="px-2.5 py-1 rounded-lg bg-emerald-100 text-emerald-800 border border-emerald-200 shadow-xs flex items-center gap-1">
          <i class="mdi mdi-check-circle text-emerald-600"></i> Resolved
        </span>
      </div>
    </div>
  </section>
</template>
