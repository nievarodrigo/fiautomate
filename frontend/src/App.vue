<template>
  <!-- Detalle cliente (no muestra nav) -->
  <ClienteDetalle v-if="clienteActual" :nombre="clienteActual" @back="clienteActual = null" />

  <!-- Vistas con nav -->
  <template v-else>
    <Dashboard v-if="tab === 'dashboard'" @ver-cliente="clienteActual = $event" />
    <Historial v-else-if="tab === 'historial'" />
    <BottomNav :tab="tab" @cambiar="tab = $event" />
  </template>
</template>

<script setup>
import { ref } from 'vue'
import Dashboard from './views/Dashboard.vue'
import ClienteDetalle from './views/ClienteDetalle.vue'
import Historial from './views/Historial.vue'
import BottomNav from './components/BottomNav.vue'

const tab = ref('dashboard')
const clienteActual = ref(null)
</script>
