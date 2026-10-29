<template>
  <div class="markdown-content" v-html="renderedHtml"></div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  content: {
    type: String,
    default: ''
  }
})

function escapeHtml(text) {
  if (!text) return ''
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;')
}

function formatMarkdown(text) {
  if (!text) return ''

  let html = escapeHtml(text)

  // Headers: ### Header
  html = html.replace(/^### (.*?)$/gm, '<h3>$1</h3>')
  html = html.replace(/^## (.*?)$/gm, '<h2>$1</h2>')
  html = html.replace(/^# (.*?)$/gm, '<h1>$1</h1>')

  // Bold: **text** -> <strong>text</strong>
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')

  // Italics: *text* or _text_ -> <em>text</em>
  html = html.replace(/\*(.*?)\*/g, '<em>$1</em>')
  html = html.replace(/_(.*?)_/g, '<em>$1</em>')

  // Code: `code` -> <code>code</code>
  html = html.replace(/`(.*?)`/g, '<code>$1</code>')

  // Bullet Lists: - item -> <li>item</li>
  html = html.replace(/^-\s+(.*)$/gm, '<li>$1</li>')
  html = html.replace(/(<li>.*?<\/li>)+/gs, '<ul>$&</ul>')

  // Numbered Lists: 1. item -> <li>item</li>
  html = html.replace(/^\d+\.\s+(.*)$/gm, '<li>$1</li>')
  html = html.replace(/(<li>.*?<\/li>)+/gs, '<ul>$&</ul>')

  // Tables if any: | col1 | col2 |
  const tableRegex = /((?:\|.+?\|\r?\n)+)/g
  html = html.replace(tableRegex, (match) => {
    const rows = match.trim().split('\n').map(r => r.trim()).filter(Boolean)
    if (rows.length < 2) return match
    let tableHtml = '<table>'
    rows.forEach((row, idx) => {
      // Check for separator row | --- | --- |
      const isSep = new RegExp('^\\|[\\-\\:\\s\\|]+\\|$').test(row)
      if (isSep) return
      const cells = row.split('|').slice(1, -1).map(c => c.trim())
      const tag = idx === 0 ? 'th' : 'td'
      tableHtml += `<tr>${cells.map(c => `<${tag}>${c}</${tag}>`).join('')}</tr>`
    })
    tableHtml += '</table>'
    return tableHtml
  })

  // Paragraphs: Split on double newlines
  html = html.replace(/\n\n/g, '</p><p>')

  // Convert remaining single newlines to line breaks (unless inside table/list)
  html = html.replace(/\n/g, '<br>')

  // Wrap in <p> if not already wrapped
  if (!html.startsWith('<h') && !html.startsWith('<p>') && !html.startsWith('<ul') && !html.startsWith('<table')) {
    html = '<p>' + html + '</p>'
  }

  return html
}

const renderedHtml = computed(() => formatMarkdown(props.content))
</script>
