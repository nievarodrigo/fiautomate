<template>
  <nav class="bottom-nav">
    <button :class="{ active: tab === 'dashboard' }" @click="$emit('cambiar', 'dashboard')">
      <span class="nav-icon">🏠</span>
      <span class="nav-label">Inicio</span>
    </button>
    <button :class="{ active: tab === 'historial' }" @click="$emit('cambiar', 'historial')">
      <span class="nav-icon">📋</span>
      <span class="nav-label">Historial</span>
    </button>
  </nav>
</template>

<script setup>
defineProps({ tab: String })
defineEmits(['cambiar'])
</script>

<style scoped>
.bottom-nav {
  position: fixed; bottom: 0; left: 0; right: 0;
  max-width: 480px; margin: 0 auto;
  display: flex; background: white;
  border-top: 1px solid var(--gray-200);
  z-index: 20;
}
.bottom-nav button {
  flex: 1; padding: 10px 0 14px;
  border: none; background: none; cursor: pointer;
  display: flex; flex-direction: column; align-items: center; gap: 3px;
}
.nav-icon { font-size: 22px; }
.nav-label { font-size: 11px; font-weight: 600; color: var(--gray-500); }
.bottom-nav button.active .nav-label { color: var(--primary); }
.bottom-nav button.active .nav-icon { filter: none; }
</style>
