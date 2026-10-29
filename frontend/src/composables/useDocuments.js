import { ref, reactive } from 'vue'
import {
  getStats,
  getDocuments,
  uploadDocument,
  deleteDocument,
  getDocumentAnalysis
} from '../api/client'

const documents = ref([])
const stats = reactive({
  chunk_count: 0,
  uploads_size_bytes: 0
})

const isUploading = ref(false)
const uploadFileName = ref('')
const uploadProgress = ref(0)

const analysisModal = reactive({
  isOpen: false,
  docId: '',
  filename: '',
  content: '',
  isLoading: false
})

async function fetchStats() {
  try {
    const data = await getStats()
    stats.chunk_count = data.chunk_count || 0
    stats.uploads_size_bytes = data.uploads_size_bytes || 0
  } catch (e) {
    console.error("Failed to load statistics:", e)
  }
}

async function fetchDocuments() {
  try {
    const data = await getDocuments()
    documents.value = data || []
  } catch (e) {
    console.error("Failed to load documents:", e)
  }
}

async function upload(file, apiKey = null) {
  isUploading.value = true
  uploadFileName.value = file.name
  uploadProgress.value = 0

  try {
    const isFirstUpload = documents.value.length === 0
    const result = await uploadDocument(file, apiKey, (percent) => {
      uploadProgress.value = percent
    })

    uploadProgress.value = 100
    await Promise.all([fetchStats(), fetchDocuments()])
    return { success: true, isFirstUpload, filename: file.name }
  } finally {
    setTimeout(() => {
      isUploading.value = false
      uploadProgress.value = 0
    }, 500)
  }
}

async function removeDoc(docId) {
  await deleteDocument(docId)
  await Promise.all([fetchStats(), fetchDocuments()])
}

async function openAnalysis(doc) {
  analysisModal.isOpen = true
  analysisModal.docId = doc.id
  analysisModal.filename = doc.filename
  analysisModal.isLoading = true
  analysisModal.content = ''

  try {
    const data = await getDocumentAnalysis(doc.id)
    analysisModal.content = data.analysis_report || ''
  } catch (e) {
    analysisModal.content = '⚠️ Report could not be retrieved. ' + (e.message || '')
  } finally {
    analysisModal.isLoading = false
  }
}

function closeAnalysis() {
  analysisModal.isOpen = false
}

export function useDocuments() {
  return {
    documents,
    stats,
    isUploading,
    uploadFileName,
    uploadProgress,
    analysisModal,
    fetchStats,
    fetchDocuments,
    upload,
    removeDoc,
    openAnalysis,
    closeAnalysis
  }
}
