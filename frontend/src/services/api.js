const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function request(path) {
  const res = await fetch(`${BASE_URL}${path}`)
  if (!res.ok) throw new Error(`Error ${res.status}`)
  return res.json()
}

export const api = {
  getResumen: () => request('/api/resumen'),
  getCliente: (nombre) => request(`/api/clientes/${encodeURIComponent(nombre)}`),
  getClientes: () => request('/api/clientes'),
  getHistorial: () => request('/api/historial'),
}
