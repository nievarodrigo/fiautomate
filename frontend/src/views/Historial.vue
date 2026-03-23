<template>
  <div>
    <TopBar title="📋 Historial" @refresh="cargar" />

    <div v-if="cargando" class="loading">Cargando...</div>

    <template v-else>
      <!-- Stats -->
      <div class="stats-grid">
        <div class="stat">
          <span class="stat-label">Total fiado</span>
          <span class="stat-val">${{ fmt(data.stats.total_fiado) }}</span>
        </div>
        <div class="stat">
          <span class="stat-label">Total cobrado</span>
          <span class="stat-val success">${{ fmt(data.stats.total_cobrado) }}</span>
        </div>
        <div class="stat full">
          <span class="stat-label">Pendiente de cobro</span>
          <span class="stat-val danger">${{ fmt(data.stats.total_pendiente) }}</span>
        </div>
      </div>

      <!-- Filtros -->
      <div class="filtros">
        <button :class="{ active: filtro === 'todos' }" @click="filtro = 'todos'">Todos</button>
        <button :class="{ active: filtro === 'fiado' }" @click="filtro = 'fiado'">Fiados</button>
        <button :class="{ active: filtro === 'pago' }" @click="filtro = 'pago'">Pagos</button>
      </div>

      <!-- Lista -->
      <div class="movimientos">
        <div v-if="movimientosFiltrados.length === 0" class="empty">Sin movimientos</div>
        <div v-for="(m, i) in movimientosFiltrados" :key="i" class="movimiento" :class="m.tipo">
          <div class="mov-icono">{{ m.tipo === 'fiado' ? '📝' : '💰' }}</div>
          <div class="mov-info">
            <span class="mov-cliente">{{ m.cliente }}</span>
            <span class="mov-desc">
              {{ m.tipo === 'fiado' ? 'Fiado' : `Pago (${m.metodo})` }}
              <span v-if="m.descripcion"> · {{ m.descripcion }}</span>
            </span>
            <span class="mov-fecha">{{ fecha(m.fecha) }}</span>
          </div>
          <div class="mov-monto" :class="m.tipo === 'pago' ? 'success' : 'danger'">
            {{ m.tipo === 'pago' ? '+' : '-' }}${{ fmt(m.monto) }}
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../services/api'
import TopBar from '../components/TopBar.vue'

const data = ref({ movimientos: [], stats: { total_fiado: 0, total_cobrado: 0, total_pendiente: 0 } })
const cargando = ref(true)
const filtro = ref('todos')

const fmt = (n) => Number(n || 0).toLocaleString('es-AR')

const fecha = (iso) => {
  const d = new Date(iso)
  return d.toLocaleDateString('es-AR', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

const movimientosFiltrados = computed(() =>
  filtro.value === 'todos' ? data.value.movimientos : data.value.movimientos.filter(m => m.tipo === filtro.value)
)

async function cargar() {
  cargando.value = true
  try { data.value = await api.getHistorial() }
  finally { cargando.value = false }
}

onMounted(cargar)
</script>

<style scoped>
.loading { text-align: center; padding: 40px; color: var(--gray-500); }
.empty { text-align: center; padding: 32px; color: var(--gray-500); }

.stats-grid {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: 10px; padding: 16px;
}
.stat {
  background: white; border-radius: var(--radius);
  padding: 14px; box-shadow: var(--shadow);
  display: flex; flex-direction: column; gap: 4px;
}
.stat.full { grid-column: 1 / -1; }
.stat-label { font-size: 12px; color: var(--gray-500); font-weight: 500; }
.stat-val { font-size: 22px; font-weight: 800; }
.stat-val.success { color: var(--success); }
.stat-val.danger { color: var(--danger); }

.filtros {
  display: flex; gap: 8px; padding: 0 16px 12px;
}
.filtros button {
  padding: 7px 16px; border-radius: 20px;
  border: 1.5px solid var(--gray-200);
  background: white; font-size: 13px; font-weight: 600; cursor: pointer;
}
.filtros button.active {
  background: var(--primary); color: white; border-color: var(--primary);
}

.movimientos { display: flex; flex-direction: column; gap: 0; margin: 0 16px; background: white; border-radius: var(--radius); box-shadow: var(--shadow); overflow: hidden; }
.movimiento {
  display: flex; align-items: center; gap: 12px;
  padding: 14px 16px; border-bottom: 1px solid var(--gray-100);
}
.movimiento:last-child { border-bottom: none; }
.mov-icono { font-size: 22px; flex-shrink: 0; }
.mov-info { flex: 1; display: flex; flex-direction: column; gap: 2px; }
.mov-cliente { font-weight: 600; font-size: 14px; }
.mov-desc { font-size: 12px; color: var(--gray-500); }
.mov-fecha { font-size: 11px; color: var(--gray-500); }
.mov-monto { font-weight: 800; font-size: 15px; }
.mov-monto.success { color: var(--success); }
.mov-monto.danger { color: var(--danger); }
</style>
