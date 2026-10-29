<template>
  <aside class="h-full w-full bg-white border border-gray-200 rounded-2xl p-4 sm:p-5 flex flex-col justify-between overflow-hidden shadow-sm">
    <!-- Top Section: App Branding & New Chat -->
    <div class="shrink-0 flex flex-col gap-3.5">
      <!-- Sidebar Header -->
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3 min-w-0">
          <div class="w-10 h-10 rounded-xl flex items-center justify-center text-white bg-gradient-to-br from-lightTeal to-darkTeal shadow-md text-lg shrink-0">
            <i class="mdi mdi-shield-text-outline"></i>
          </div>
          <div class="min-w-0">
            <h2 class="text-sm font-black font-heading text-slate-900 tracking-tight leading-none truncate">DocAgent AI</h2>
            <span class="text-[9px] text-darkTeal font-bold uppercase tracking-wider block mt-0.5 truncate">HR & Policy Assistant</span>
          </div>
        </div>
        
        <!-- Mobile Drawer Close Button -->
        <button 
          class="lg:hidden w-8 h-8 rounded-xl flex items-center justify-center text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors cursor-pointer shrink-0"
          title="Close sidebar"
          @click="$emit('closeMobile')"
        >
          <i class="mdi mdi-close text-lg"></i>
        </button>
      </div>

      <!-- New Chat Action Button -->
      <button 
        class="w-full py-2.5 px-4 rounded-xl bg-gradient-to-r from-lightTeal to-darkTeal hover:from-darkTeal hover:to-lightTeal text-white font-bold text-xs shadow-sm hover:shadow-md flex items-center justify-center gap-2 transition-all cursor-pointer transform active:scale-[0.98]"
        @click="handleNewChat"
      >
        <i class="mdi mdi-plus-circle-outline text-base"></i>
        <span>New Chat</span>
      </button>
    </div>

    <!-- MIDDLE SECTION: KNOWLEDGE / DOCUMENTS -->
    <div class="flex-1 flex flex-col min-h-0 my-3">
      <!-- Drag & Drop Uploader -->
      <div class="mb-3 shrink-0">
        <h3 class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1.5 font-heading">Upload Documents</h3>
        <div 
          class="border-2 border-dashed border-gray-300 hover:border-darkTeal/60 rounded-xl p-3 text-center cursor-pointer transition-all flex flex-col items-center gap-1 bg-slate-50/50"
          :class="{ 'dropzone-hover': isDragOver }"
          @click="triggerFileInput"
          @dragover.prevent="isDragOver = true"
          @dragleave.prevent="isDragOver = false"
          @drop.prevent="handleDrop"
        >
          <input 
            ref="fileInputRef" 
            type="file" 
            accept=".pdf,.txt,.md,.docx" 
            class="hidden" 
            @change="handleFileSelected"
          >
          <i class="mdi mdi-cloud-upload-outline text-xl text-darkTeal animate-pulse"></i>
          <p class="text-xs font-bold text-slate-700">Drag & drop or <span class="text-darkTeal hover:underline font-bold">browse</span></p>
          <span class="text-[9px] text-slate-500 font-medium">PDF, MD, TXT, DOCX (Max 10MB)</span>
        </div>

        <!-- Upload Progress Container -->
        <div v-if="isUploading" class="mt-2 bg-slate-50 border border-gray-200 rounded-xl p-2">
          <div class="flex items-center justify-between text-[10px]">
            <span class="text-slate-700 font-bold truncate max-w-[80%]">{{ uploadFileName }}</span>
            <span class="text-darkTeal font-extrabold">{{ uploadProgress }}%</span>
          </div>
          <div class="w-full h-1.5 bg-slate-200 rounded-full mt-1 overflow-hidden">
            <div 
              class="h-full bg-limeGreen transition-all duration-200" 
              :style="{ width: uploadProgress + '%' }"
            ></div>
          </div>
        </div>
      </div>

      <div class="flex items-center justify-between mb-2 shrink-0">
        <h3 class="text-[10px] font-bold text-slate-400 uppercase tracking-widest font-heading">Indexed Policy Files</h3>
        <span class="px-2 py-0.5 rounded-full bg-lightTeal/15 text-darkTeal text-[10px] font-extrabold">
          {{ documents.length }}
        </span>
      </div>

      <!-- Scrollable Document Cards List -->
      <div class="flex-1 overflow-y-auto space-y-2 pr-1 min-h-0">
        <div 
          v-if="documents.length === 0" 
          class="h-full min-h-[100px] flex flex-col items-center justify-center py-6 text-slate-400 gap-1.5 border border-dashed border-gray-200 rounded-xl bg-slate-50/30"
        >
          <i class="mdi mdi-file-question-outline text-2xl text-slate-300"></i>
          <p class="text-[10px] font-semibold text-slate-500">No documents uploaded yet</p>
        </div>

        <div 
          v-for="doc in documents" 
          :key="doc.id" 
          class="bg-slate-50/50 hover:bg-slate-50 border border-slate-200/80 hover:border-lightTeal/50 rounded-2xl p-2.5 sm:p-3 flex flex-col gap-2 transition-all duration-200 shadow-sm"
        >
          <div class="flex items-start gap-2.5">
            <div class="w-7 h-7 rounded-lg bg-lightTeal/10 flex items-center justify-center text-darkTeal text-sm shrink-0">
              <i class="mdi mdi-file-document-outline"></i>
            </div>
            <div class="flex-grow min-w-0">
              <div class="text-xs font-bold text-slate-800 truncate" :title="doc.filename">
                {{ doc.filename }}
              </div>
              <div class="text-[9px] text-slate-500 flex items-center gap-1.5 mt-0.5 font-semibold">
                <span>{{ formatFileSize(doc.file_size) }}</span>
                <span>•</span>
                <span>{{ doc.chunk_count }} chunks</span>
              </div>
            </div>
          </div>

          <div class="flex gap-1.5 w-full">
            <button 
              v-if="doc.has_analysis"
              class="flex-grow py-1 px-2.5 rounded-full bg-white border border-slate-200 hover:border-slate-400 text-[9px] font-bold text-slate-700 hover:text-slate-900 hover:bg-slate-50 flex items-center justify-center gap-1 transition-all duration-200 cursor-pointer"
              @click="$emit('viewAnalysis', doc)"
            >
              <i class="mdi mdi-text-box-search-outline text-darkTeal text-xs"></i> Analysis
            </button>

            <button 
              class="py-1 px-2 rounded-full bg-white border border-slate-200 hover:border-coralOrange/50 hover:bg-coralOrange/5 hover:text-coralOrange text-[9px] font-bold text-slate-500 flex items-center justify-center gap-1 transition-all duration-200 cursor-pointer"
              :class="doc.has_analysis ? 'w-7 shrink-0' : 'flex-grow'"
              title="Delete Document"
              @click="confirmDeleteDoc(doc.id)"
            >
              <i class="mdi mdi-delete-outline text-xs"></i> 
              <span v-if="!doc.has_analysis">Remove</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- BOTTOM SECTION: ADMIN DASHBOARD QUICK ACCESS & STATS -->
    <div class="shrink-0 border-t border-gray-200 pt-3 flex flex-col gap-2.5">
      <!-- Admin Dashboard / Back to Chat Toggle Button -->
      <button 
        class="w-full py-2.5 px-3 rounded-xl border font-bold text-xs flex items-center justify-between transition-all cursor-pointer group shadow-sm"
        :class="isDashboardView 
          ? 'bg-darkTeal border-darkTeal text-white hover:bg-darkTeal/90' 
          : 'border-darkTeal/30 bg-lightTeal/10 hover:bg-lightTeal/20 text-darkTeal'"
        :title="isDashboardView ? 'Back to Chat Assistant' : 'Open Admin Question Management Dashboard'"
        @click="$emit('toggleDashboard')"
      >
        <div class="flex items-center gap-2">
          <div class="w-6 h-6 rounded-lg flex items-center justify-center text-xs" :class="isDashboardView ? 'bg-white/20 text-white' : 'bg-darkTeal text-white'">
            <i :class="isDashboardView ? 'mdi mdi-chat-outline' : 'mdi mdi-view-dashboard-outline'"></i>
          </div>
          <span class="font-bold" :class="isDashboardView ? 'text-white' : 'text-slate-900 group-hover:text-darkTeal'">
            {{ isDashboardView ? 'Back to Chat' : 'Admin Dashboard' }}
          </span>
        </div>
        <i class="mdi text-sm transition-transform" :class="isDashboardView ? 'mdi-arrow-left group-hover:-translate-x-0.5' : 'mdi-arrow-right group-hover:translate-x-0.5'"></i>
      </button>

      <!-- System Analytics Grid -->
      <div class="grid grid-cols-2 gap-2">
        <div class="bg-slate-50 border border-gray-100 rounded-xl p-2">
          <span class="text-[8px] text-slate-500 uppercase font-bold tracking-wider block mb-0.5">Chunks</span>
          <span class="text-xs font-bold text-slate-900">{{ stats.chunk_count.toLocaleString() }}</span>
        </div>
        <div class="bg-slate-50 border border-gray-100 rounded-xl p-2">
          <span class="text-[8px] text-slate-500 uppercase font-bold tracking-wider block mb-0.5">DB Size</span>
          <span class="text-xs font-bold text-slate-900">{{ formattedDbSize }}</span>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useDocuments } from '../../composables/useDocuments'
import { useAuth } from '../../composables/useAuth'

const emit = defineEmits(['viewAnalysis', 'firstUploadComplete', 'openSettings', 'closeMobile', 'toggleDashboard', 'newChat'])

defineProps({
  isDashboardView: {
    type: Boolean,
    default: false
  }
})

const { documents, stats, isUploading, uploadFileName, uploadProgress, upload, removeDoc } = useDocuments()
const { apiKey } = useAuth()

const fileInputRef = ref(null)
const isDragOver = ref(false)

const formattedDbSize = computed(() => {
  const bytes = stats.uploads_size_bytes || 0
  if (bytes < 1024 * 1024) {
    return `${(bytes / 1024).toFixed(1)} KB`
  }
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
})

function formatFileSize(bytes) {
  if (!bytes) return '0 KB'
  if (bytes < 1024 * 1024) {
    return `${(bytes / 1024).toFixed(1)} KB`
  }
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

function handleNewChat() {
  emit('newChat')
  emit('closeMobile')
}

function triggerFileInput() {
  fileInputRef.value?.click()
}

async function handleFileSelected(e) {
  const file = e.target.files?.[0]
  if (file) {
    await processUpload(file)
    e.target.value = ''
  }
}

async function handleDrop(e) {
  isDragOver.value = false
  const file = e.dataTransfer.files?.[0]
  if (file) {
    await processUpload(file)
  }
}

async function processUpload(file) {
  try {
    const res = await upload(file)
    if (res.isFirstUpload) {
      emit('firstUploadComplete', file.name)
    }
  } catch (err) {
    alert(`Upload Error: ${err.message}`)
  }
}

async function confirmDeleteDoc(docId) {
  if (confirm("Are you sure you want to delete this document? All embedded search chunks will be permanently removed.")) {
    try {
      await removeDoc(docId)
    } catch (err) {
      alert(`Error: ${err.message}`)
    }
  }
}
</script>
