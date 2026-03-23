<template>
  <div>
    <TopBar title="🏪 Fiautomate" @refresh="cargar" />

    <div v-if="cargando" class="loading">Cargando...</div>

    <div v-else-if="error" class="error-msg">
      ❌ No se pudo conectar al servidor
      <button @click="cargar">Reintentar</button>
    </div>

    <template v-else>
      <ResumenStats :total="resumen.total_general" :cantidad="resumen.cantidad_clientes" />

      <div class="section-title">Clientes con fiados</div>

      <div v-if="resumen.clientes?.length === 0" class="empty">
        🎉 No hay fiados pendientes
      </div>

      <div v-else class="lista">
        <ClienteCard
          v-for="c in resumen.clientes"
          :key="c.nombre"
          :cliente="c"
          @click="verCliente"
        />
      </div>
    </template>

    <!-- Botón flotante -->
    <button class="fab" @click="mostrarForm = true">+</button>

    <FormModal
      v-if="mostrarForm"
      @close="mostrarForm = false"
      @guardado="onGuardado"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../services/api'
import TopBar from '../components/TopBar.vue'
import ResumenStats from '../components/ResumenStats.vue'
import ClienteCard from '../components/ClienteCard.vue'
import FormModal from '../components/FormModal.vue'

const emit = defineEmits(['ver-cliente'])
const resumen = ref({ clientes: [], total_general: 0, cantidad_clientes: 0 })
const cargando = ref(true)
const error = ref(false)
const mostrarForm = ref(false)

async function cargar() {
  cargando.value = true
  error.value = false
  try {
    resumen.value = await api.getResumen()
  } catch {
    error.value = true
  } finally {
    cargando.value = false
  }
}

function verCliente(nombre) {
  emit('ver-cliente', nombre)
}

function onGuardado() {
  cargar()
}

onMounted(cargar)
</script>

<style scoped>
.loading, .empty {
  text-align: center; padding: 40px 16px;
  color: var(--gray-500); font-size: 15px;
}
.error-msg {
  text-align: center; padding: 32px 16px;
  color: var(--danger); display: flex; flex-direction: column; gap: 12px; align-items: center;
}
.error-msg button {
  padding: 8px 20px; border-radius: 20px;
  background: var(--primary); color: white; border: none; cursor: pointer;
}
.section-title {
  padding: 12px 16px 6px;
  font-size: 13px; font-weight: 600;
  color: var(--gray-500); text-transform: uppercase; letter-spacing: 0.5px;
}
.lista { background: white; border-radius: var(--radius); margin: 0 16px; box-shadow: var(--shadow); overflow: hidden; }
.fab {
  position: fixed; bottom: 24px; right: 24px;
  width: 56px; height: 56px; border-radius: 50%;
  background: var(--primary); color: white;
  font-size: 32px; border: none; cursor: pointer;
  box-shadow: 0 4px 16px rgba(108,71,255,0.4);
  display: flex; align-items: center; justify-content: center;
}
</style>
