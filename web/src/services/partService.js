import client from "./client";

export function list() {
  return client.get('/api/parts')
    .then((res) => res.data)
}

export function find({ id }) {
  return client.get(`/api/parts/${id}`)
    .then((res) => res.data)
}

export function create(values) {
  const form = new FormData()
  for (const [key, value] of Object.entries(values)) {
    form.append(key, value)
  }
  return client.post(`/api/parts`, form)
    .then((res) => res.data)
}

export function update({ id, ...values }) {
  const form = new FormData()
  for (const [key, value] of Object.entries(values)) {
    form.append(key, value)
  }
  return client.patch(`/api/parts/${id}`, form)
    .then((res) => res.data)
}

export function defunct({ partId }) {
  return client.post(`/api/parts/${partId}/defunct`)
    .then((res) => res.data)
}
