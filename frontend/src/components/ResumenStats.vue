<template>
  <div class="stats">
    <div class="stat-card">
      <span class="stat-label">Total adeudado</span>
      <span class="stat-value danger">${{ fmt(total) }}</span>
    </div>
    <div class="stat-card">
      <span class="stat-label">Clientes con deuda</span>
      <span class="stat-value">{{ cantidad }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({ total: Number, cantidad: Number })
const fmt = (n) => Number(n).toLocaleString('es-AR')
</script>

<style scoped>
.stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  padding: 16px;
}
.stat-card {
  background: white;
  border-radius: var(--radius);
  padding: 16px;
  box-shadow: var(--shadow);
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.stat-label { font-size: 12px; color: var(--gray-500); font-weight: 500; }
.stat-value { font-size: 24px; font-weight: 800; color: var(--gray-900); }
.stat-value.danger { color: var(--danger); }
</style>
