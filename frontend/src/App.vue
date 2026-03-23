<template>
  <Dashboard v-if="!clienteActual" @ver-cliente="clienteActual = $event" />
  <ClienteDetalle v-else :nombre="clienteActual" @back="clienteActual = null" />
</template>

<script setup>
import { ref } from 'vue'
import Dashboard from './views/Dashboard.vue'
import ClienteDetalle from './views/ClienteDetalle.vue'

const clienteActual = ref(null)
</script>
