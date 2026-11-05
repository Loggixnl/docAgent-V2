import { ref } from 'vue'
import i18n from '../i18n'
import { normalizeLang, getStoredLang, setStoredLang } from '../i18n/storage'

const lang = ref(getStoredLang())

function applyDocumentLang(code) {
  try {
    document.documentElement.lang = code
  } catch (e) {
    // non-browser environment
  }
}

// Keep the initial value in sync with <html lang>
applyDocumentLang(lang.value)

export function setLang(next) {
  const code = setStoredLang(next)
  lang.value = code
  i18n.global.locale.value = code
  applyDocumentLang(code)
  return code
}

export function getLang() {
  return lang.value
}

export function useLanguage() {
  return { lang, setLang, getLang, normalizeLang }
}
