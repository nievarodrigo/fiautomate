<template>
  <div class="fiado" :class="{ saldado: fiado.saldado }">
    <div class="fiado-header">
      <span class="badge" :class="fiado.saldado ? 'badge-ok' : 'badge-pend'">
        {{ fiado.saldado ? '✅ Saldado' : '⏳ Pendiente' }}
      </span>
      <span class="fecha">{{ fecha }}</span>
    </div>
    <div class="fiado-montos">
      <span class="original">Original: ${{ fmt(fiado.monto_original) }}</span>
      <span v-if="!fiado.saldado" class="pendiente">Debe: ${{ fmt(fiado.monto_pendiente) }}</span>
    </div>
    <p v-if="fiado.descripcion" class="descripcion">{{ fiado.descripcion }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({ fiado: Object })
const fmt = (n) => Number(n).toLocaleString('es-AR')
const fecha = computed(() => {
  const d = new Date(props.fiado.fecha)
  return d.toLocaleDateString('es-AR', { day: '2-digit', month: 'short', year: 'numeric' })
})
</script>

<style scoped>
.fiado {
  background: white;
  border-radius: 10px;
  padding: 14px;
  border-left: 4px solid var(--warn);
  box-shadow: var(--shadow);
}
.fiado.saldado { border-left-color: var(--success); opacity: 0.7; }
.fiado-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.badge { font-size: 12px; font-weight: 600; padding: 3px 8px; border-radius: 20px; }
.badge-ok { background: var(--success-light); color: var(--success); }
.badge-pend { background: var(--warn-light); color: var(--warn); }
.fecha { font-size: 12px; color: var(--gray-500); }
.fiado-montos { display: flex; gap: 16px; }
.original { font-size: 13px; color: var(--gray-500); }
.pendiente { font-size: 13px; font-weight: 700; color: var(--danger); }
.descripcion { font-size: 12px; color: var(--gray-500); margin-top: 6px; font-style: italic; }
</style>
