<template>
  <div>
    <TopBar :title="cliente?.nombre || '...'" back @back="$emit('back')" />

    <div v-if="cargando" class="loading">Cargando...</div>

    <template v-else-if="cliente">
      <!-- Resumen del cliente -->
      <div class="cliente-resumen">
        <div class="avatar-lg">{{ iniciales }}</div>
        <div class="total-label">Total pendiente</div>
        <div class="total-monto" :class="{ verde: cliente.total_pendiente === 0 }">
          ${{ fmt(cliente.total_pendiente) }}
        </div>
        <div v-if="cliente.telefono" class="telefono">📞 {{ cliente.telefono }}</div>
      </div>

      <!-- Fiados -->
      <div class="section-title">Historial de fiados</div>
      <div class="fiados-lista">
        <FiadoItem v-for="f in cliente.fiados" :key="f.id" :fiado="f" />
        <div v-if="cliente.fiados.length === 0" class="empty">Sin fiados registrados</div>
      </div>
    </template>

    <!-- Botón flotante -->
    <button class="fab" @click="mostrarForm = true">+</button>

    <FormModal
      v-if="mostrarForm"
      :nombre-inicial="nombre"
      @close="mostrarForm = false"
      @guardado="onGuardado"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../services/api'
import TopBar from '../components/TopBar.vue'
import FiadoItem from '../components/FiadoItem.vue'
import FormModal from '../components/FormModal.vue'

const props = defineProps({ nombre: String })
defineEmits(['back'])

const cliente = ref(null)
const cargando = ref(true)
const mostrarForm = ref(false)

const iniciales = computed(() =>
  (cliente.value?.nombre || '').split(' ').map(p => p[0]).slice(0, 2).join('').toUpperCase()
)

const fmt = (n) => Number(n).toLocaleString('es-AR')

async function cargar() {
  cargando.value = true
  try {
    cliente.value = await api.getCliente(props.nombre)
  } finally {
    cargando.value = false
  }
}

function onGuardado() {
  cargar()
}

onMounted(cargar)
</script>

<style scoped>
.loading { text-align: center; padding: 40px; color: var(--gray-500); }
.cliente-resumen {
  display: flex; flex-direction: column; align-items: center;
  padding: 24px 16px; background: white;
  border-bottom: 1px solid var(--gray-200);
  gap: 4px;
}
.avatar-lg {
  width: 64px; height: 64px; border-radius: 50%;
  background: var(--primary-light); color: var(--primary);
  font-size: 22px; font-weight: 800;
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 8px;
}
.total-label { font-size: 12px; color: var(--gray-500); font-weight: 500; }
.total-monto { font-size: 32px; font-weight: 800; color: var(--danger); }
.total-monto.verde { color: var(--success); }
.telefono { font-size: 13px; color: var(--gray-500); margin-top: 4px; }

.section-title {
  padding: 14px 16px 6px;
  font-size: 13px; font-weight: 600;
  color: var(--gray-500); text-transform: uppercase; letter-spacing: 0.5px;
}
.fiados-lista { display: flex; flex-direction: column; gap: 10px; padding: 0 16px 16px; }
.empty { text-align: center; padding: 24px; color: var(--gray-500); }
.fab {
  position: fixed; bottom: 24px; right: 24px;
  width: 56px; height: 56px; border-radius: 50%;
  background: var(--primary); color: white;
  font-size: 32px; border: none; cursor: pointer;
  box-shadow: 0 4px 16px rgba(108,71,255,0.4);
  display: flex; align-items: center; justify-content: center;
}
</style>
