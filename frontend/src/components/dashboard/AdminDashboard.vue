<template>
  <div class="h-full flex flex-col bg-white overflow-hidden">
    <!-- DASHBOARD TOP HEADER -->
    <div class="p-4 sm:p-5 border-b border-gray-200 bg-slate-50/60 shrink-0">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <div class="flex items-center gap-2">
            <span class="w-8 h-8 rounded-xl bg-gradient-to-br from-lightTeal to-darkTeal flex items-center justify-center text-white text-base shadow-sm">
              <i class="mdi mdi-view-dashboard"></i>
            </span>
            <h1 class="text-base sm:text-lg font-black font-heading text-slate-900 tracking-tight">
              AI Question & Session Management Dashboard
            </h1>
          </div>
          <p class="text-xs text-slate-500 mt-1 flex items-center gap-1.5 flex-wrap">
            <span>Workflow:</span>
            <span class="font-semibold text-slate-700">User</span>
            <i class="mdi mdi-arrow-right text-[10px] text-slate-400"></i>
            <span class="font-semibold text-slate-700">Session</span>
            <i class="mdi mdi-arrow-right text-[10px] text-slate-400"></i>
            <span class="font-semibold text-slate-700">Question</span>
            <i class="mdi mdi-arrow-right text-[10px] text-slate-400"></i>
            <span class="font-semibold text-darkTeal">AI Response</span>
            <i class="mdi mdi-arrow-right text-[10px] text-slate-400"></i>
            <span class="font-semibold text-purple-700">Admin Review</span>
            <i class="mdi mdi-arrow-right text-[10px] text-slate-400"></i>
            <span class="font-bold text-emerald-700">Resolved</span>
          </p>
        </div>

        <div class="flex items-center gap-2">
          <!-- Refresh Button -->
          <button 
            class="py-1.5 px-3 rounded-xl border border-gray-200 bg-white hover:bg-slate-50 text-slate-700 text-xs font-bold transition-all flex items-center gap-1.5 cursor-pointer shadow-xs"
            :disabled="isLoading"
            @click="refreshData"
          >
            <i class="mdi mdi-refresh" :class="{ 'mdi-spin': isLoading }"></i>
            <span>Refresh</span>
          </button>

          <!-- Back to Chat Button -->
          <button 
            class="py-1.5 px-3.5 rounded-xl bg-gradient-to-r from-lightTeal to-darkTeal hover:from-darkTeal hover:to-lightTeal text-white text-xs font-bold transition-all flex items-center gap-1.5 cursor-pointer shadow-sm"
            @click="$emit('backToChat')"
          >
            <i class="mdi mdi-chat-processing-outline"></i>
            <span>Back to Chat</span>
          </button>
        </div>
      </div>

      <!-- ANALYTICS CARDS GRID (5 metrics) -->
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-2.5 sm:gap-3.5 mt-4">
        <!-- 1. Total Sessions -->
        <div class="bg-white border border-gray-200/90 rounded-xl p-3 shadow-xs">
          <div class="flex items-center justify-between text-slate-500 mb-1">
            <span class="text-[10px] font-bold uppercase tracking-wider">Total Sessions</span>
            <i class="mdi mdi-forum-outline text-darkTeal text-base"></i>
          </div>
          <div class="text-xl font-black text-slate-900">{{ analytics.total_sessions || 0 }}</div>
          <div class="text-[10px] text-slate-400 mt-0.5">Active chat threads</div>
        </div>

        <!-- 2. Total Questions (Queries) -->
        <div class="bg-white border border-gray-200/90 rounded-xl p-3 shadow-xs">
          <div class="flex items-center justify-between text-slate-500 mb-1">
            <span class="text-[10px] font-bold uppercase tracking-wider">Total Questions</span>
            <i class="mdi mdi-help-circle-outline text-purple-600 text-base"></i>
          </div>
          <div class="text-xl font-black text-slate-900">{{ analytics.total_questions || 0 }}</div>
          <div class="text-[10px] text-purple-700/80 font-medium mt-0.5">Queries submitted</div>
        </div>

        <!-- 3. Unanswered (Queries) -->
        <div class="bg-white border border-gray-200/90 rounded-xl p-3 shadow-xs">
          <div class="flex items-center justify-between text-slate-500 mb-1">
            <span class="text-[10px] font-bold uppercase tracking-wider">Unanswered</span>
            <i class="mdi mdi-clock-alert-outline text-amber-500 text-base"></i>
          </div>
          <div class="text-xl font-black text-amber-600">{{ analytics.unanswered_questions || 0 }}</div>
          <div class="text-[10px] text-amber-600/80 mt-0.5">Pending response</div>
        </div>

        <!-- 4. Needs Review (Queries) -->
        <div class="bg-white border border-gray-200/90 rounded-xl p-3 shadow-xs">
          <div class="flex items-center justify-between text-slate-500 mb-1">
            <span class="text-[10px] font-bold uppercase tracking-wider">Needs Review</span>
            <i class="mdi mdi-alert-circle-outline text-coralOrange text-base"></i>
          </div>
          <div class="text-xl font-black text-coralOrange">{{ analytics.needs_review || 0 }}</div>
          <div class="text-[10px] text-coralOrange/80 mt-0.5">Flagged for HR admin</div>
        </div>

        <!-- 5. Resolved (Queries) -->
        <div class="bg-white border border-gray-200/90 rounded-xl p-3 shadow-xs col-span-2 sm:col-span-1">
          <div class="flex items-center justify-between text-slate-500 mb-1">
            <span class="text-[10px] font-bold uppercase tracking-wider">Resolved</span>
            <i class="mdi mdi-check-circle-outline text-emerald-600 text-base"></i>
          </div>
          <div class="flex items-baseline gap-1 text-sm font-black text-slate-900">
            <span class="text-emerald-700">{{ analytics.resolved || 0 }} Res</span>
            <span class="text-slate-300">/</span>
            <span class="text-purple-600">{{ analytics.admin_answered || 0 }} Ans</span>
          </div>
          <!-- Progress bar -->
          <div class="w-full bg-emerald-100 h-1.5 rounded-full overflow-hidden mt-2">
            <div 
              class="bg-emerald-600 h-full transition-all duration-300"
              :style="{ width: queryResolutionRatio + '%' }"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- MAIN DASHBOARD CONTENT AREA -->
    <div class="flex-1 flex flex-col min-h-0">
      <!-- TABS: Query Management vs Sessions -->
      <div class="px-4 sm:px-6 pt-3 border-b border-gray-200 flex items-center justify-between bg-white shrink-0">
        <div class="flex items-center gap-4">
          <button 
            class="py-2.5 px-1 border-b-2 font-bold text-xs flex items-center gap-2 transition-all cursor-pointer"
            :class="currentTab === 'questions' ? 'border-darkTeal text-darkTeal' : 'border-transparent text-slate-500 hover:text-slate-800'"
            @click="currentTab = 'questions'"
          >
            <i class="mdi mdi-email-alert-outline text-base"></i>
            <span>Query Management</span>
            <span class="text-[10px] px-2 py-0.5 rounded-full bg-purple-100 text-purple-700 font-extrabold">
              {{ questions.length }}
            </span>
          </button>

          <button 
            class="py-2.5 px-1 border-b-2 font-bold text-xs flex items-center gap-2 transition-all cursor-pointer"
            :class="currentTab === 'sessions' ? 'border-darkTeal text-darkTeal' : 'border-transparent text-slate-500 hover:text-slate-800'"
            @click="currentTab = 'sessions'"
          >
            <i class="mdi mdi-message-reply-text-outline text-base"></i>
            <span>Chat Sessions</span>
            <span class="text-[10px] px-2 py-0.5 rounded-full bg-slate-100 text-slate-700 font-extrabold">
              {{ sessions.length }}
            </span>
          </button>
        </div>
      </div>

      <!-- QUERY MANAGEMENT TAB CONTENT (Contact HR/Admin inquiries only) -->
      <div v-if="currentTab === 'questions'" class="flex-1 flex flex-col min-h-0 p-4 sm:p-6 overflow-hidden">
        <!-- Header label -->
        <div class="flex items-center gap-2 mb-3 shrink-0">
          <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-purple-50 border border-purple-200 text-purple-700 text-[10px] font-extrabold">
            <i class="mdi mdi-email-alert-outline"></i>
            Showing Contact HR / Admin queries only
          </span>
        </div>

        <!-- Filters Bar -->
        <div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-2.5 mb-4 shrink-0">
          <!-- Search input -->
          <div class="relative flex-1 max-w-md">
            <i class="mdi mdi-magnify absolute left-3 top-2.5 text-slate-400 text-base"></i>
            <input 
              v-model="questionSearch"
              type="text"
              placeholder="Search queries by message, email, or ID..."
              class="w-full pl-9 pr-3 py-2 bg-slate-50 border border-gray-200 rounded-xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-darkTeal focus:bg-white transition-all font-medium"
              @input="debounceFetchQuestions"
            />
          </div>

          <div class="flex items-center gap-2 flex-wrap">
            <!-- Status Filter -->
            <select 
              v-model="statusFilter"
              class="bg-slate-50 border border-gray-200 rounded-xl py-2 px-3 text-xs font-bold text-slate-700 focus:outline-none focus:border-darkTeal cursor-pointer"
              @change="fetchQuestions"
            >
              <option value="">All Statuses</option>
              <option value="new">New</option>
              <option value="needs_review">Needs Review</option>
              <option value="admin_answered">Admin Answered</option>
              <option value="resolved">Resolved</option>
            </select>
          </div>
        </div>

        <!-- Queries Table / List -->
        <div class="flex-1 overflow-y-auto border border-gray-200 rounded-2xl shadow-xs min-h-0">
          <div v-if="isLoadingQuestions" class="h-64 flex flex-col items-center justify-center text-slate-400 gap-2">
            <i class="mdi mdi-loading mdi-spin text-3xl text-purple-500"></i>
            <span class="text-xs font-semibold">Loading HR/Admin queries...</span>
          </div>

          <div v-else-if="questions.length === 0" class="h-64 flex flex-col items-center justify-center text-slate-400 gap-2 text-center p-6">
            <i class="mdi mdi-email-off-outline text-4xl text-slate-300"></i>
            <h4 class="text-xs font-bold text-slate-700">No queries found</h4>
            <p class="text-[11px] text-slate-400 max-w-sm">No Contact HR / Admin queries have been submitted yet, or none match the selected filters.</p>
          </div>

          <table v-else class="w-full text-left border-collapse">
            <thead class="bg-purple-50/60 sticky top-0 z-10 border-b border-purple-100">
              <tr class="text-[10px] font-extrabold uppercase text-slate-500 tracking-wider">
                <th class="py-3 px-3.5">Query ID</th>
                <th class="py-3 px-3.5">User & Session</th>
                <th class="py-3 px-3.5">Query / Message</th>
                <th class="py-3 px-3.5">Status</th>
                <th class="py-3 px-3.5">Submitted</th>
                <th class="py-3 px-3.5 text-right">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100 text-xs">
              <tr 
                v-for="q in questions" 
                :key="q.id"
                class="hover:bg-purple-50/30 transition-colors"
              >
                <!-- Query ID -->
                <td class="py-3 px-3.5 font-mono text-[10px] text-slate-500 font-semibold whitespace-nowrap">
                  {{ q.id }}
                </td>

                <!-- User & Session -->
                <td class="py-3 px-3.5 max-w-[160px]">
                  <div class="font-bold text-slate-800 truncate" :title="q.user_email || 'Anonymous'">
                    {{ q.user_email || 'User' }}
                  </div>
                  <div class="text-[10px] text-slate-400 truncate mt-0.5" :title="q.session_title || q.session_id">
                    {{ q.session_title || q.session_id }}
                  </div>
                </td>

                <!-- Query Message & Admin Response Preview -->
                <td class="py-3 px-3.5 max-w-md">
                  <div class="flex items-start gap-1.5">
                    <i class="mdi mdi-email-alert-outline text-purple-500 text-sm shrink-0 mt-0.5"></i>
                    <div class="font-bold text-slate-900 leading-snug line-clamp-2">
                      {{ q.question }}
                    </div>
                  </div>
                  <!-- Admin Answer snippet (if present) -->
                  <div v-if="q.admin_response" class="text-[10px] text-purple-700 font-semibold line-clamp-1 mt-1">
                    <i class="mdi mdi-shield-check text-xs"></i> Admin: {{ q.admin_response }}
                  </div>
                  <div v-else class="text-[10px] text-amber-600 font-semibold mt-1">
                    <i class="mdi mdi-clock-alert-outline text-xs"></i> Awaiting admin response
                  </div>
                </td>

                <!-- Status Badge -->
                <td class="py-3 px-3.5 whitespace-nowrap">
                  <span 
                    class="px-2.5 py-1 rounded-full text-[9px] font-extrabold uppercase tracking-wider"
                    :class="getStatusBadgeClass(q.status)"
                  >
                    {{ formatStatusLabel(q.status) }}
                  </span>
                </td>

                <!-- Timestamp -->
                <td class="py-3 px-3.5 text-slate-500 text-[10px] whitespace-nowrap font-medium">
                  {{ formatDate(q.created_at) }}
                </td>

                <!-- Actions -->
                <td class="py-3 px-3.5 text-right whitespace-nowrap">
                  <div class="flex items-center justify-end gap-1.5">
                    <button 
                      class="py-1 px-2.5 rounded-lg bg-white border border-purple-300 hover:border-purple-500 text-purple-700 hover:bg-purple-50 font-bold text-xs transition-all cursor-pointer shadow-xs flex items-center gap-1"
                      title="Review and respond to this query"
                      @click="openQuestionReview(q)"
                    >
                      <i class="mdi mdi-reply-outline"></i>
                      <span>Review</span>
                    </button>
                    <button 
                      class="py-1 px-2 rounded-lg bg-white border border-red-200 hover:border-red-400 text-red-600 hover:bg-red-50 font-bold text-xs transition-all cursor-pointer shadow-xs flex items-center gap-1"
                      title="Delete query"
                      @click="promptDeleteQuery(q)"
                    >
                      <i class="mdi mdi-delete-outline text-sm"></i>
                      <span>Delete</span>
                    </button>
                  </div>
                </td>

              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- SESSIONS TAB CONTENT -->
      <div v-else class="flex-1 flex flex-col min-h-0 p-4 sm:p-6 overflow-hidden">
        <!-- Search sessions -->
        <div class="flex items-center justify-between gap-3 mb-4 shrink-0">
          <div class="relative flex-1 max-w-md">
            <i class="mdi mdi-magnify absolute left-3 top-2.5 text-slate-400 text-base"></i>
            <input 
              v-model="sessionSearch"
              type="text"
              placeholder="Search sessions by title, user email, or session ID..."
              class="w-full pl-9 pr-3 py-2 bg-slate-50 border border-gray-200 rounded-xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-darkTeal focus:bg-white transition-all font-medium"
              @input="debounceFetchSessions"
            />
          </div>
        </div>

        <!-- Sessions Table -->
        <div class="flex-1 overflow-y-auto border border-gray-200 rounded-2xl shadow-xs min-h-0">
          <div v-if="isLoadingSessions" class="h-64 flex flex-col items-center justify-center text-slate-400 gap-2">
            <i class="mdi mdi-loading mdi-spin text-3xl text-darkTeal"></i>
            <span class="text-xs font-semibold">Loading sessions...</span>
          </div>

          <div v-else-if="sessions.length === 0" class="h-64 flex flex-col items-center justify-center text-slate-400 gap-2 text-center p-6">
            <i class="mdi mdi-chat-outline text-4xl text-slate-300"></i>
            <h4 class="text-xs font-bold text-slate-700">No chat sessions found</h4>
            <p class="text-[11px] text-slate-400 max-w-sm">No sessions found matching your search.</p>
          </div>

          <table v-else class="w-full text-left border-collapse">
            <thead class="bg-slate-50/80 sticky top-0 z-10 border-b border-gray-200">
              <tr class="text-[10px] font-extrabold uppercase text-slate-500 tracking-wider">
                <th class="py-3 px-3.5">Session ID</th>
                <th class="py-3 px-3.5">Session Title</th>
                <th class="py-3 px-3.5">User</th>
                <th class="py-3 px-3.5">Questions</th>
                <th class="py-3 px-3.5">Last Active</th>
                <th class="py-3 px-3.5 text-right">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100 text-xs">
              <tr 
                v-for="s in sessions" 
                :key="s.id"
                class="hover:bg-slate-50/70 transition-colors"
              >
                <!-- Session ID -->
                <td class="py-3 px-3.5 font-mono text-[10px] text-slate-500 font-semibold whitespace-nowrap">
                  {{ s.id }}
                </td>

                <!-- Title -->
                <td class="py-3 px-3.5 font-bold text-slate-900 max-w-xs truncate" :title="s.title">
                  {{ s.title || 'New Chat' }}
                </td>

                <!-- User -->
                <td class="py-3 px-3.5 text-slate-600 font-medium">
                  {{ s.user_email || 'User' }}
                </td>

                <!-- Question Count -->
                <td class="py-3 px-3.5">
                  <span class="px-2 py-0.5 rounded-full bg-lightTeal/15 text-darkTeal font-extrabold text-[10px]">
                    {{ s.question_count || 0 }} questions
                  </span>
                </td>

                <!-- Last Active -->
                <td class="py-3 px-3.5 text-slate-500 text-[10px] whitespace-nowrap font-medium">
                  {{ formatDate(s.updated_at || s.created_at) }}
                </td>

                <!-- Actions -->
                <td class="py-3 px-3.5 text-right whitespace-nowrap">
                  <div class="flex items-center justify-end gap-1.5">
                    <button 
                      class="py-1 px-2.5 rounded-lg bg-gradient-to-r from-lightTeal to-darkTeal text-white font-bold text-xs hover:opacity-95 transition-all cursor-pointer shadow-xs flex items-center gap-1"
                      title="View session conversation thread"
                      @click="viewSessionConversation(s.id)"
                    >
                      <i class="mdi mdi-forum-outline"></i>
                      <span>View</span>
                    </button>
                    <button 
                      class="py-1 px-2 rounded-lg bg-white border border-red-200 hover:border-red-400 text-red-600 hover:bg-red-50 font-bold text-xs transition-all cursor-pointer shadow-xs flex items-center gap-1"
                      title="Delete chat session"
                      @click="promptDeleteSession(s)"
                    >
                      <i class="mdi mdi-delete-outline text-sm"></i>
                      <span>Delete</span>
                    </button>
                  </div>
                </td>

              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- MODAL 1: QUESTION REVIEW & ADMIN RESPONSE -->
    <div 
      v-if="selectedQuestion" 
      class="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-slate-900/50 backdrop-blur-sm"
      @click.self="selectedQuestion = null"
    >
      <div class="bg-white rounded-2xl border border-gray-200 shadow-2xl max-w-2xl w-full max-h-[90vh] flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        <!-- Modal Header -->
        <div class="p-4 sm:p-5 border-b border-gray-200 flex items-center justify-between bg-slate-50/70">
          <div>
            <div class="flex items-center gap-2">
              <span class="w-7 h-7 rounded-lg bg-purple-100 text-purple-700 flex items-center justify-center text-sm font-bold">
                <i class="mdi mdi-shield-check"></i>
              </span>
              <h3 class="text-sm font-black font-heading text-slate-900">
                Admin Review & Response
              </h3>
            </div>
            <div class="text-[10px] text-slate-500 mt-0.5 flex items-center gap-2">
              <span>Question ID: <strong class="font-mono">{{ selectedQuestion.id }}</strong></span>
              <span>•</span>
              <span>Session: <strong class="font-mono">{{ selectedQuestion.session_id }}</strong></span>
            </div>
          </div>
          <button 
            class="w-7 h-7 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-200 flex items-center justify-center cursor-pointer transition-colors"
            @click="selectedQuestion = null"
          >
            <i class="mdi mdi-close text-base"></i>
          </button>
        </div>

        <!-- Modal Body (Scrollable) -->
        <div class="p-4 sm:p-6 overflow-y-auto space-y-4 flex-1">
          <!-- Question Box -->
          <div class="bg-slate-50 border border-gray-200 rounded-xl p-3.5">
            <div class="flex items-center justify-between text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1.5">
              <span class="flex items-center gap-1.5 flex-wrap">
                <span>User Question / Inquiry</span>
                <span v-if="selectedQuestion.user_email" class="text-slate-600 font-semibold normal-case">
                  (Contact: <a :href="'mailto:' + selectedQuestion.user_email" class="text-darkTeal hover:underline font-bold">{{ selectedQuestion.user_email }}</a>)
                </span>
              </span>
              <span 
                class="px-2 py-0.2 rounded-full text-[9px] font-extrabold"
                :class="selectedQuestion.question_type === 'document' ? 'bg-lightTeal/15 text-darkTeal' : (selectedQuestion.question_type === 'inquiry' ? 'bg-purple-100 text-purple-800' : 'bg-indigo-50 text-indigo-700')"
              >
                {{ selectedQuestion.question_type === 'document' ? 'Document Policy' : (selectedQuestion.question_type === 'inquiry' ? 'Widget Direct Inquiry' : 'General Knowledge') }}
              </span>
            </div>
            <div class="text-xs font-bold text-slate-900 leading-relaxed whitespace-pre-wrap">
              {{ selectedQuestion.question }}
            </div>
          </div>

          <!-- AI Generated Response Box -->
          <div class="bg-white border border-slate-200 rounded-xl p-3.5 shadow-xs">
            <div class="flex items-center justify-between text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1.5">
              <span class="flex items-center gap-1 text-darkTeal">
                <i class="mdi mdi-robot-outline"></i> {{ selectedQuestion.question_type === 'inquiry' ? 'Inquiry Routing & Notes' : 'AI Generated Response' }}
              </span>
              <span v-if="selectedQuestion.source" class="text-slate-500 font-semibold truncate max-w-[200px]">
                Src: {{ selectedQuestion.source }}
              </span>
            </div>
            <div class="text-xs text-slate-700 leading-relaxed whitespace-pre-wrap max-h-48 overflow-y-auto p-1 bg-slate-50/50 rounded-lg">
              {{ selectedQuestion.ai_response || (selectedQuestion.question_type === 'inquiry' ? 'Direct Admin Inquiry submitted from the chat widget. Pending admin review and response below.' : 'No AI response generated.') }}
            </div>
          </div>

          <!-- Admin Response Input Box -->
          <div class="space-y-2">
            <label class="block text-xs font-bold text-slate-800">
              Official Admin Response / Notes:
            </label>
            <p class="text-[10px] text-slate-400">
              Provide policy clarifications, HR decisions, or revised answers. This will be visible to the user in their chat session.
            </p>
            <textarea 
              v-model="editAdminResponse"
              rows="4"
              placeholder="Type official admin response, policy clarification, or review notes here..."
              class="w-full p-3 bg-slate-50 border border-gray-300 rounded-xl text-xs text-slate-800 focus:outline-none focus:border-darkTeal focus:bg-white transition-all font-medium"
            ></textarea>
          </div>

          <!-- Status Selector -->
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 bg-slate-50/80 p-3 rounded-xl border border-gray-200">
            <div>
              <label class="block text-xs font-bold text-slate-800">Update Question Status</label>
              <span class="text-[10px] text-slate-400">Set the resolution state for this question</span>
            </div>
            <select 
              v-model="editStatus"
              class="bg-white border border-gray-300 rounded-xl py-2 px-3 text-xs font-bold text-slate-700 focus:outline-none focus:border-darkTeal cursor-pointer"
            >
              <option value="new">New</option>
              <option value="ai_answered">AI Answered</option>
              <option value="needs_review">Needs Review</option>
              <option value="admin_answered">Admin Answered</option>
              <option value="resolved">Resolved</option>
            </select>
          </div>
        </div>

        <!-- Modal Footer -->
        <div class="p-4 border-t border-gray-200 flex flex-wrap items-center justify-between gap-2 bg-slate-50/60">
          <!-- Quick action buttons & Delete -->
          <div class="flex items-center gap-1.5 flex-wrap">
            <button 
              class="py-1.5 px-2 rounded-lg border border-red-200 hover:border-red-400 bg-white hover:bg-red-50 text-red-600 font-bold text-[10px] transition-colors cursor-pointer flex items-center gap-1"
              title="Delete this query permanently"
              @click="promptDeleteQuery(selectedQuestion)"
            >
              <i class="mdi mdi-delete-outline text-xs"></i> Delete
            </button>
            <button 
              class="py-1.5 px-2.5 rounded-lg border border-amber-300 bg-amber-50 text-amber-800 font-bold text-[10px] hover:bg-amber-100 transition-colors cursor-pointer"
              @click="editStatus = 'needs_review'"
            >
              <i class="mdi mdi-alert-circle-outline mr-0.5"></i> Flag Review
            </button>
            <button 
              class="py-1.5 px-2.5 rounded-lg border border-emerald-300 bg-emerald-50 text-emerald-800 font-bold text-[10px] hover:bg-emerald-100 transition-colors cursor-pointer"
              @click="editStatus = 'resolved'"
            >
              <i class="mdi mdi-check-circle-outline mr-0.5"></i> Mark Resolved
            </button>
          </div>


          <div class="flex items-center gap-2">
            <button 
              class="py-2 px-3 rounded-xl text-slate-600 hover:text-slate-800 hover:bg-slate-200 text-xs font-bold transition-colors cursor-pointer"
              @click="selectedQuestion = null"
            >
              Cancel
            </button>
            <button 
              class="py-2 px-4 rounded-xl bg-gradient-to-r from-lightTeal to-darkTeal hover:from-darkTeal hover:to-lightTeal text-white text-xs font-bold transition-all flex items-center gap-1.5 cursor-pointer shadow-sm"
              :disabled="isSaving"
              @click="saveQuestionReview"
            >
              <i class="mdi mdi-content-save-outline" :class="{ 'mdi-spin': isSaving }"></i>
              <span>Save & Update</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL 2: SESSION CONVERSATION VIEWER -->
    <div 
      v-if="selectedSessionDetail" 
      class="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-slate-900/50 backdrop-blur-sm"
      @click.self="selectedSessionDetail = null"
    >
      <div class="bg-white rounded-2xl border border-gray-200 shadow-2xl max-w-3xl w-full max-h-[92vh] flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        <!-- Session Modal Header -->
        <div class="p-4 sm:p-5 border-b border-gray-200 flex items-center justify-between bg-slate-50/70">
          <div>
            <div class="flex items-center gap-2">
              <span class="w-7 h-7 rounded-lg bg-lightTeal/15 text-darkTeal flex items-center justify-center text-sm font-bold">
                <i class="mdi mdi-chat-outline"></i>
              </span>
              <h3 class="text-sm font-black font-heading text-slate-900">
                {{ selectedSessionDetail.session?.title || 'Session Conversation' }}
              </h3>
            </div>
            <div class="text-[10px] text-slate-500 mt-0.5 flex items-center gap-2">
              <span>Session ID: <strong class="font-mono">{{ selectedSessionDetail.session?.id }}</strong></span>
              <span>•</span>
              <span>{{ selectedSessionDetail.questions?.length || 0 }} Questions Recorded</span>
            </div>
          </div>
          <button 
            class="w-7 h-7 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-200 flex items-center justify-center cursor-pointer transition-colors"
            @click="selectedSessionDetail = null"
          >
            <i class="mdi mdi-close text-base"></i>
          </button>
        </div>

        <!-- Session Messages Thread (Scrollable) -->
        <div class="p-4 sm:p-6 overflow-y-auto space-y-4 flex-1 bg-slate-50/20">
          <div 
            v-if="!selectedSessionDetail.questions || selectedSessionDetail.questions.length === 0" 
            class="py-12 text-center text-slate-400 text-xs"
          >
            No questions recorded in this session.
          </div>

          <div 
            v-for="(q, qIdx) in selectedSessionDetail.questions" 
            :key="q.id"
            class="bg-white border border-gray-200 rounded-2xl p-4 shadow-xs space-y-3"
          >
            <!-- Question Header -->
            <div class="flex items-center justify-between text-[10px] pb-2 border-b border-gray-100">
              <div class="flex items-center gap-2">
                <span class="font-extrabold text-slate-400">#{{ qIdx + 1 }}</span>
                <span class="font-mono text-slate-500">{{ q.id }}</span>
                <span 
                  class="px-2 py-0.2 rounded-full font-extrabold"
                  :class="q.question_type === 'document' ? 'bg-lightTeal/15 text-darkTeal' : 'bg-indigo-50 text-indigo-700'"
                >
                  {{ q.question_type === 'document' ? 'Document' : 'General' }}
                </span>
                <span 
                  class="px-2 py-0.2 rounded-full font-bold uppercase tracking-wider text-[8px]"
                  :class="getStatusBadgeClass(q.status)"
                >
                  {{ formatStatusLabel(q.status) }}
                </span>
              </div>
              <button 
                class="text-[10px] font-bold text-darkTeal hover:underline cursor-pointer flex items-center gap-0.5"
                @click="openQuestionReview(q)"
              >
                <i class="mdi mdi-pencil text-xs"></i>
                <span>Review / Edit</span>
              </button>
            </div>

            <!-- User Query -->
            <div class="flex items-start gap-2.5">
              <div class="w-6 h-6 rounded-lg bg-slate-100 flex items-center justify-center text-xs text-slate-500 shrink-0">
                <i class="mdi mdi-account"></i>
              </div>
              <div class="text-xs font-bold text-slate-900 leading-relaxed">
                {{ q.question }}
              </div>
            </div>

            <!-- AI Response -->
            <div class="flex items-start gap-2.5 bg-slate-50/80 p-3 rounded-xl border border-slate-100">
              <div class="w-6 h-6 rounded-lg bg-lightTeal/15 flex items-center justify-center text-xs text-darkTeal shrink-0">
                <i class="mdi mdi-robot-outline"></i>
              </div>
              <div class="text-xs text-slate-700 leading-relaxed whitespace-pre-wrap flex-1">
                {{ q.ai_response || 'No AI response.' }}
                <div v-if="q.source" class="mt-2 text-[9px] font-semibold text-slate-400">
                  <i class="mdi mdi-file-document-outline"></i> Source: {{ q.source }}
                </div>
              </div>
            </div>

            <!-- Admin Response (if present) -->
            <div v-if="q.admin_response" class="flex items-start gap-2.5 bg-emerald-50/80 p-3 rounded-xl border border-emerald-200">
              <div class="w-6 h-6 rounded-lg bg-emerald-100 text-emerald-800 flex items-center justify-center text-xs shrink-0 font-bold">
                <i class="mdi mdi-shield-check"></i>
              </div>
              <div class="flex-1">
                <span class="text-[10px] font-black text-emerald-800 uppercase tracking-wider block mb-0.5">Admin Response</span>
                <div class="text-xs text-emerald-950 font-medium whitespace-pre-wrap leading-relaxed">
                  {{ q.admin_response }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Session Modal Footer -->
        <div class="p-4 border-t border-gray-200 flex items-center justify-between bg-slate-50/60">
          <button 
            class="py-1.5 px-3 rounded-xl border border-red-200 hover:border-red-400 bg-white hover:bg-red-50 text-red-600 font-bold text-xs transition-colors cursor-pointer flex items-center gap-1.5 shadow-xs"
            title="Delete this chat session permanently"
            @click="promptDeleteSession(selectedSessionDetail.session)"
          >
            <i class="mdi mdi-delete-outline text-sm"></i>
            <span>Delete Session</span>
          </button>
          <button 
            class="py-2 px-4 rounded-xl bg-slate-200 hover:bg-slate-300 text-slate-700 text-xs font-bold transition-colors cursor-pointer"
            @click="selectedSessionDetail = null"
          >
            Close
          </button>
        </div>
      </div>
    </div>

    <!-- MODAL 3: DELETE CONFIRMATION -->
    <div 
      v-if="deleteModal.isOpen" 
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm"
      @click.self="deleteModal.isOpen = false"
    >
      <div class="bg-white rounded-2xl border border-gray-200 shadow-2xl max-w-md w-full p-5 sm:p-6 animate-in fade-in zoom-in-95 duration-200">
        <div class="flex items-start gap-3.5">
          <div class="w-10 h-10 rounded-xl bg-red-100 text-red-600 flex items-center justify-center text-xl shrink-0">
            <i class="mdi mdi-delete-alert-outline"></i>
          </div>
          <div class="flex-1 min-w-0">
            <h3 class="text-sm font-black font-heading text-slate-900">
              {{ deleteModal.type === 'query' ? 'Delete HR Query' : 'Delete Chat Session' }}
            </h3>
            <p class="text-xs text-slate-600 mt-1 leading-relaxed">
              <template v-if="deleteModal.type === 'query'">
                Are you sure you want to delete this query? This inquiry and its conversation history will be permanently deleted.
              </template>
              <template v-else>
                Are you sure you want to delete this chat session? All messages and questions in this session will be permanently removed.
              </template>
            </p>
            <div v-if="deleteModal.item" class="mt-3 p-2.5 rounded-xl bg-slate-50 border border-gray-100 text-[11px] text-slate-500 font-mono truncate">
              ID: {{ deleteModal.item.id }}
              <span v-if="deleteModal.item.title" class="block font-sans font-bold text-slate-700 mt-0.5 truncate">
                {{ deleteModal.item.title }}
              </span>
              <span v-else-if="deleteModal.item.question" class="block font-sans font-bold text-slate-700 mt-0.5 truncate">
                {{ deleteModal.item.question }}
              </span>
            </div>
          </div>
        </div>

        <div class="flex items-center justify-end gap-2.5 mt-6">
          <button 
            class="py-2 px-3.5 rounded-xl border border-gray-200 hover:bg-slate-100 text-slate-700 text-xs font-bold transition-colors cursor-pointer"
            :disabled="deleteModal.isDeleting"
            @click="deleteModal.isOpen = false"
          >
            Cancel
          </button>
          <button 
            class="py-2 px-4 rounded-xl bg-red-600 hover:bg-red-700 text-white text-xs font-bold transition-all flex items-center gap-1.5 cursor-pointer shadow-sm"
            :disabled="deleteModal.isDeleting"
            @click="executeDelete"
          >
            <i class="mdi mdi-loading mdi-spin" v-if="deleteModal.isDeleting"></i>
            <i class="mdi mdi-delete-outline" v-else></i>
            <span>{{ deleteModal.isDeleting ? 'Deleting...' : 'Confirm Delete' }}</span>
          </button>
        </div>
      </div>
    </div>
  </div>

</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { 
  getAdminAnalytics, 
  getAdminQuestions, 
  getAdminSessions, 
  getAdminSessionDetail, 
  updateAdminQuestion,
  deleteAdminQuestion,
  deleteAdminSession
} from '../../api/client'

defineEmits(['backToChat'])

const currentTab = ref('questions') // 'questions' or 'sessions'
const isLoading = ref(false)
const isLoadingQuestions = ref(false)
const isLoadingSessions = ref(false)
const isSaving = ref(false)

const analytics = ref({
  total_sessions: 0,
  total_questions: 0,
  total_queries: 0,
  unanswered_questions: 0,
  unanswered_queries: 0,
  needs_review: 0,
  needs_review_queries: 0,
  admin_answered: 0,
  resolved: 0
})

const questions = ref([])
const sessions = ref([])

const questionSearch = ref('')
const statusFilter = ref('')
// Locked to 'inquiry' — Query Management only shows Contact HR/Admin submissions
const typeFilter = ref('inquiry')
const sessionSearch = ref('')

const selectedQuestion = ref(null)
const editStatus = ref('new')
const editAdminResponse = ref('')

const selectedSessionDetail = ref(null)

const deleteModal = ref({
  isOpen: false,
  type: 'query', // 'query' | 'session'
  item: null,
  isDeleting: false
})

let debounceTimerQuestions = null
let debounceTimerSessions = null

const queryResolutionRatio = computed(() => {
  const total = (analytics.value.total_queries ?? analytics.value.total_questions ?? 0)
  if (total === 0) return 0
  const completed = (analytics.value.resolved || 0) + (analytics.value.admin_answered || 0)
  return Math.min(100, Math.round((completed / total) * 100))
})


onMounted(async () => {
  await refreshData()
})

async function refreshData() {
  isLoading.value = true
  await Promise.all([
    fetchAnalytics(),
    fetchQuestions(),
    fetchSessions()
  ])
  isLoading.value = false
}

async function fetchAnalytics() {
  try {
    const data = await getAdminAnalytics()
    if (data) {
      analytics.value = data
    }
  } catch (err) {
    console.error("Failed to load analytics:", err)
  }
}

async function fetchQuestions() {
  isLoadingQuestions.value = true
  try {
    const data = await getAdminQuestions(
      questionSearch.value,
      statusFilter.value,
      typeFilter.value
    )
    questions.value = data || []
  } catch (err) {
    console.error("Failed to load questions:", err)
  } finally {
    isLoadingQuestions.value = false
  }
}

function debounceFetchQuestions() {
  clearTimeout(debounceTimerQuestions)
  debounceTimerQuestions = setTimeout(() => {
    fetchQuestions()
  }, 300)
}

async function fetchSessions() {
  isLoadingSessions.value = true
  try {
    const data = await getAdminSessions(sessionSearch.value)
    sessions.value = data || []
  } catch (err) {
    console.error("Failed to load sessions:", err)
  } finally {
    isLoadingSessions.value = false
  }
}

function debounceFetchSessions() {
  clearTimeout(debounceTimerSessions)
  debounceTimerSessions = setTimeout(() => {
    fetchSessions()
  }, 300)
}

function openQuestionReview(q) {
  selectedQuestion.value = q
  editStatus.value = q.status || 'new'
  editAdminResponse.value = q.admin_response || ''
}

async function saveQuestionReview() {
  if (!selectedQuestion.value) return
  isSaving.value = true

  try {
    await updateAdminQuestion(selectedQuestion.value.id, {
      status: editStatus.value,
      admin_response: editAdminResponse.value
    })

    // Update in local questions list
    const target = questions.value.find(item => item.id === selectedQuestion.value.id)
    if (target) {
      target.status = editStatus.value
      target.admin_response = editAdminResponse.value
    }

    // Also update in session thread if open
    if (selectedSessionDetail.value && selectedSessionDetail.value.questions) {
      const threadQ = selectedSessionDetail.value.questions.find(item => item.id === selectedQuestion.value.id)
      if (threadQ) {
        threadQ.status = editStatus.value
        threadQ.admin_response = editAdminResponse.value
      }
    }

    // Refresh analytics
    fetchAnalytics()

    selectedQuestion.value = null
  } catch (err) {
    alert(`Could not save review: ${err.message}`)
  } finally {
    isSaving.value = false
  }
}

async function viewSessionConversation(sessionId) {
  try {
    const data = await getAdminSessionDetail(sessionId)
    selectedSessionDetail.value = data
  } catch (err) {
    alert(`Could not load session details: ${err.message}`)
  }
}

function promptDeleteQuery(q) {
  if (!q) return
  deleteModal.value = {
    isOpen: true,
    type: 'query',
    item: q,
    isDeleting: false
  }
}

function promptDeleteSession(s) {
  if (!s) return
  deleteModal.value = {
    isOpen: true,
    type: 'session',
    item: s,
    isDeleting: false
  }
}

async function executeDelete() {
  if (!deleteModal.value.item) return
  deleteModal.value.isDeleting = true

  try {
    if (deleteModal.value.type === 'query') {
      const qId = deleteModal.value.item.id
      await deleteAdminQuestion(qId)
      // Remove from questions array
      questions.value = questions.value.filter(item => item.id !== qId)
      // If modal was open for this question, close it
      if (selectedQuestion.value?.id === qId) {
        selectedQuestion.value = null
      }
    } else {
      const sId = deleteModal.value.item.id
      await deleteAdminSession(sId)
      // Remove from sessions array
      sessions.value = sessions.value.filter(item => item.id !== sId)
      // If modal was open for this session, close it
      if (selectedSessionDetail.value?.session?.id === sId) {
        selectedSessionDetail.value = null
      }
    }

    // Refresh analytics immediately
    await fetchAnalytics()
    deleteModal.value.isOpen = false
  } catch (err) {
    alert(`Could not delete: ${err.message}`)
  } finally {
    deleteModal.value.isDeleting = false
  }
}

function getStatusBadgeClass(status) {
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

function formatStatusLabel(status) {
  switch (status) {
    case 'resolved': return 'Resolved'
    case 'admin_answered': return 'Admin Answered'
    case 'needs_review': return 'Needs Review'
    case 'new': return 'New'
    case 'ai_answered':
    default: return 'AI Answered'
  }
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  try {
    const d = new Date(dateStr)
    return d.toLocaleString(undefined, {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch (e) {
    return dateStr
  }
}
</script>
