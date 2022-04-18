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
