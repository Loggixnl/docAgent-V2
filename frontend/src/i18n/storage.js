// Shared localStorage helpers for the selected UI language.
// Kept free of Vue imports so api/client.js can use it too.

export const LANG_KEY = 'langSelected'
export const SUPPORTED_LANGS = ['en', 'nl']
export const DEFAULT_LANG = 'en'

export function normalizeLang(lang) {
  const code = String(lang || '').trim().toLowerCase()
  return SUPPORTED_LANGS.includes(code) ? code : DEFAULT_LANG
}

export function getStoredLang() {
  try {
    return normalizeLang(localStorage.getItem(LANG_KEY))
  } catch (e) {
    return DEFAULT_LANG
  }
}

export function setStoredLang(lang) {
  const code = normalizeLang(lang)
  try {
    localStorage.setItem(LANG_KEY, code)
  } catch (e) {
    // localStorage unavailable (private mode) — language still applies for this session
  }
  return code
}
