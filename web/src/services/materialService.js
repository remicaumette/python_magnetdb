import client from "./client";

export function list() {
  return client.get('/api/materials')
    .then((res) => res.data)
}

export function find({ id }) {
  return client.get(`/api/materials/${id}`)
    .then((res) => res.data)
}

export function create(values) {
  return client.post(`/api/materials`, values)
    .then((res) => res.data)
}

export function update({ id, ...values }) {
  return client.patch(`/api/materials/${id}`, values)
    .then((res) => res.data)
}

export function destroy({ id }) {
  return client.delete(`/api/materials/${id}`)
    .then((res) => res.data)
}
