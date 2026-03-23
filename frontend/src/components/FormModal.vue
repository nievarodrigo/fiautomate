<template>
  <div class="overlay" @click.self="$emit('close')">
    <div class="modal">
      <div class="modal-header">
        <h2>{{ titulo }}</h2>
        <button class="close-btn" @click="$emit('close')">✕</button>
      </div>

      <!-- Tabs -->
      <div class="tabs">
        <button :class="{ active: tab === 'fiado' }" @click="tab = 'fiado'">Nuevo fiado</button>
        <button :class="{ active: tab === 'pago' }" @click="tab = 'pago'">Registrar pago</button>
      </div>

      <!-- Form Fiado -->
      <form v-if="tab === 'fiado'" @submit.prevent="enviarFiado" class="form">
        <label>
          Cliente
          <input v-model="fiado.nombre" type="text" placeholder="Ej: Carlitos" required autofocus />
        </label>
        <label>
          Monto ($)
          <input v-model.number="fiado.monto" type="number" min="1" placeholder="Ej: 2000" required />
        </label>
        <label>
          Descripción (opcional)
          <input v-model="fiado.descripcion" type="text" placeholder="Ej: fideos, aceite..." />
        </label>
        <button type="submit" class="btn-primary" :disabled="enviando">
          {{ enviando ? 'Guardando...' : '✅ Guardar fiado' }}
        </button>
      </form>

      <!-- Form Pago -->
      <form v-else @submit.prevent="enviarPago" class="form">
        <label>
          Cliente
          <input v-model="pago.nombre" type="text" placeholder="Ej: Carlitos" required autofocus />
        </label>
        <label>
          Monto pagado ($)
          <input v-model.number="pago.monto" type="number" min="1" placeholder="Ej: 1000" required />
        </label>
        <label>Método de pago</label>
        <div class="metodo-btns">
          <button type="button" :class="{ selected: pago.metodo === 'efectivo' }" @click="pago.metodo = 'efectivo'">
            💵 Efectivo
          </button>
          <button type="button" :class="{ selected: pago.metodo === 'mercadopago' }" @click="pago.metodo = 'mercadopago'">
            📱 MercadoPago
          </button>
        </div>
        <button type="submit" class="btn-primary" :disabled="enviando">
          {{ enviando ? 'Guardando...' : '✅ Registrar pago' }}
        </button>
      </form>

      <p v-if="respuesta" class="respuesta">{{ respuesta }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['close', 'guardado'])

const props = defineProps({ nombreInicial: String })

const tab = ref('fiado')
const enviando = ref(false)
const respuesta = ref('')

const fiado = ref({ nombre: props.nombreInicial || '', monto: null, descripcion: '' })
const pago = ref({ nombre: props.nombreInicial || '', monto: null, metodo: 'efectivo' })

const titulo = 'Registrar'
const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function enviarFiado() {
  enviando.value = true
  respuesta.value = ''
  try {
    const text = fiado.value.descripcion
      ? `#fiado: ${fiado.value.nombre} ${fiado.value.monto} ${fiado.value.descripcion}`
      : `#fiado: ${fiado.value.nombre} ${fiado.value.monto}`

    const res = await fetch(`${BASE}/webhook/whatsapp`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    })
    const data = await res.json()
    respuesta.value = data.reply || '✅ Guardado'
    fiado.value = { nombre: '', monto: null, descripcion: '' }
    emit('guardado')
  } finally {
    enviando.value = false
  }
}

async function enviarPago() {
  enviando.value = true
  respuesta.value = ''
  try {
    const metodoFlag = pago.value.metodo === 'mercadopago' ? ' mp' : ''
    const text = `#pago: ${pago.value.nombre} ${pago.value.monto}${metodoFlag}`

    const res = await fetch(`${BASE}/webhook/whatsapp`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    })
    const data = await res.json()
    respuesta.value = data.reply || '✅ Guardado'
    pago.value = { nombre: '', monto: null, metodo: 'efectivo' }
    emit('guardado')
  } finally {
    enviando.value = false
  }
}
</script>

<style scoped>
.overlay {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex; align-items: flex-end;
  z-index: 100;
}
.modal {
  background: white;
  border-radius: 20px 20px 0 0;
  width: 100%; max-width: 480px; margin: 0 auto;
  padding: 20px;
  max-height: 90vh; overflow-y: auto;
}
.modal-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 16px;
}
.modal-header h2 { font-size: 18px; font-weight: 700; }
.close-btn {
  width: 32px; height: 32px; border-radius: 50%;
  border: none; background: var(--gray-100);
  font-size: 14px; cursor: pointer;
}
.tabs {
  display: flex; gap: 8px; margin-bottom: 20px;
}
.tabs button {
  flex: 1; padding: 10px; border-radius: 10px;
  border: 2px solid var(--gray-200);
  background: white; font-weight: 600; font-size: 14px; cursor: pointer;
}
.tabs button.active {
  border-color: var(--primary); color: var(--primary); background: var(--primary-light);
}
.form { display: flex; flex-direction: column; gap: 14px; }
.form label {
  display: flex; flex-direction: column; gap: 6px;
  font-size: 13px; font-weight: 600; color: var(--gray-700);
}
.form input {
  padding: 12px 14px; border-radius: 10px;
  border: 1.5px solid var(--gray-200);
  font-size: 15px; outline: none;
}
.form input:focus { border-color: var(--primary); }
.metodo-btns { display: flex; gap: 10px; }
.metodo-btns button {
  flex: 1; padding: 12px; border-radius: 10px;
  border: 2px solid var(--gray-200);
  background: white; font-size: 14px; font-weight: 600; cursor: pointer;
}
.metodo-btns button.selected {
  border-color: var(--primary); color: var(--primary); background: var(--primary-light);
}
.btn-primary {
  padding: 14px; border-radius: 12px;
  background: var(--primary); color: white;
  border: none; font-size: 16px; font-weight: 700;
  cursor: pointer; margin-top: 4px;
}
.btn-primary:disabled { opacity: 0.6; }
.respuesta {
  margin-top: 12px; padding: 12px; background: var(--gray-50);
  border-radius: 10px; font-size: 13px; white-space: pre-line;
}
</style>
