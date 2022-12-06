import client from "./client";

export function list({ query, page, perPage, sortBy, sortDesc } = {}) {
  return client.get('/api/simulations', {
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
  return client.get(`/api/simulations/${id}`)
    .then((res) => res.data)
}

export function runSetup({ id }) {
  return client.post(`/api/simulations/${id}/run_setup`)
    .then((res) => res.data)
}

export function runSimulation({ id, serverId, cores }) {
  let form = new FormData()
  if (serverId) {
    form.set('server_id', serverId)
  }
  form.set('cores', cores)
  return client.post(`/api/simulations/${id}/run`, form)
    .then((res) => res.data)
}

export function deleteSimulation({ id }) {
  return client.delete(`/api/simulations/${id}`)
    .then((res) => res.data)
}

export function create(values) {
  const form = new FormData()
  for (const [key, value] of Object.entries(values)) {
    if (value !== undefined) {
      form.append(key, value)
    }
  }
  return client.post(`/api/simulations`, form)
    .then((res) => res.data)
}

export function listModels() {
  return client.get(`/api/simulations/models`)
    .then((res) => res.data)
}

export function getMeasures({ id, measure }) {
  return client.get(`/api/simulations/${id}/measures`, {
    params: { measure_name: measure }
  })
    .then((res) => res.data)
}
