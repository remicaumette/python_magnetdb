import client from "./client";

export function list({ page, perPage, sortBy, sortDesc, query } = {}) {
  return client.get('/api/records', {
    params: {
      page,
      query,
      sort_by: sortBy,
      sort_desc: sortDesc,
      per_page: perPage,
    },
  })
    .then((res) => res.data)
}

export function find({ id }) {
  return client.get(`/api/records/${id}`)
    .then((res) => res.data)
}

export function visualize({ id, x, y }) {
  return client.get(`/api/records/${id}/visualize`, { params: { x, y } })
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

export function update({ id, ...values }) {
  const form = new FormData()
  for (const [key, value] of Object.entries(values)) {
    form.append(key, value)
  }
  return client.patch(`/api/records/${id}`, form)
    .then((res) => res.data)
}
