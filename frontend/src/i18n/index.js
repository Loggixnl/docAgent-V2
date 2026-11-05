import { createI18n } from 'vue-i18n'
import en from './messages/en'
import nl from './messages/nl'
import { getStoredLang } from './storage'

const i18n = createI18n({
  legacy: false,
  locale: getStoredLang(),
  fallbackLocale: 'en',
  messages: { en, nl }
})

export default i18n
