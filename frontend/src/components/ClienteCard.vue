<template>
  <button class="card" @click="$emit('click', cliente.nombre)">
    <div class="avatar">{{ iniciales }}</div>
    <div class="info">
      <span class="nombre">{{ cliente.nombre }}</span>
      <span class="detalle">{{ cliente.fiados }} fiado{{ cliente.fiados !== 1 ? 's' : '' }} pendiente{{ cliente.fiados !== 1 ? 's' : '' }}</span>
    </div>
    <div class="monto">
      <span>${{ fmt(cliente.total) }}</span>
      <span class="chevron">›</span>
    </div>
  </button>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({ cliente: Object })
defineEmits(['click'])

const iniciales = computed(() =>
  props.cliente.nombre.split(' ').map(p => p[0]).slice(0, 2).join('').toUpperCase()
)
const fmt = (n) => Number(n).toLocaleString('es-AR')
</script>

<style scoped>
.card {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  background: white;
  border: none;
  border-bottom: 1px solid var(--gray-100);
  cursor: pointer;
  text-align: left;
  transition: background 0.15s;
}
.card:active { background: var(--gray-50); }
.avatar {
  width: 42px; height: 42px;
  border-radius: 50%;
  background: var(--primary-light);
  color: var(--primary);
  font-weight: 700; font-size: 14px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.info { flex: 1; display: flex; flex-direction: column; gap: 2px; }
.nombre { font-weight: 600; font-size: 15px; }
.detalle { font-size: 12px; color: var(--gray-500); }
.monto { display: flex; align-items: center; gap: 4px; font-weight: 700; color: var(--danger); }
.chevron { color: var(--gray-500); font-size: 20px; }
</style>
