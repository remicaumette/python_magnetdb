import client from "./client";

export function list() {
  return client.get('/api/sites')
    .then((res) => res.data)
}

export function find({ id }) {
  return client.get(`/api/sites/${id}`)
    .then((res) => res.data)
}

export function create(values) {
  return client.post(`/api/sites`, values)
    .then((res) => res.data)
}

export function update({ id, ...values }) {
  return client.patch(`/api/sites/${id}`, values)
    .then((res) => res.data)
}

export function destroy({ id }) {
  return client.delete(`/api/sites/${id}`)
    .then((res) => res.data)
}
