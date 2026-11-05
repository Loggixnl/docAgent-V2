<template>
  <footer class="border-t border-gray-300/40 py-8 px-6 md:px-12 flex flex-col md:flex-row items-center justify-between text-xs text-slate-500 max-w-7xl mx-auto gap-4 w-full">
    <div class="flex items-center gap-2 text-sm text-slate-700 font-bold font-heading">
      <i class="mdi mdi-shield-text-outline text-darkTeal text-base"></i> {{ $t('brand') }}
    </div>
    <p>{{ $t('footer.copyright') }}</p>
  </footer>
</template>
