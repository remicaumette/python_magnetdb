import client from "./client";

export function list() {
  return client.get('/api/magnets')
    .then((res) => res.data)
}

export function find({ id }) {
  return client.get(`/api/magnets/${id}`)
    .then((res) => res.data)
}

export function create(values) {
  return client.post(`/api/magnets`, values)
    .then((res) => res.data)
}

export function update({ id, ...values }) {
  return client.patch(`/api/magnets/${id}`, values)
    .then((res) => res.data)
}

export function destroy({ id }) {
  return client.delete(`/api/magnets/${id}`)
    .then((res) => res.data)
}
