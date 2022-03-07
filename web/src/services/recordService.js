import client from "./client";

export function list() {
  return client.get('/api/records')
    .then((res) => res.data)
}

export function find({ id }) {
  return client.get(`/api/records/${id}`)
    .then((res) => res.data)
}

export function create(values) {
  const form = new FormData()
  for (const [key, value] of Object.entries(values)) {
    form.append(key, value)
  }
  return client.post(`/api/records`, form)
    .then((res) => res.data)
}
