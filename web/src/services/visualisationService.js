import client from "./client";

export function bmap(params) {
  return client.post('/api/visualisations/bmap', params)
    .then((res) => res.data)
}

export function stressMap(params) {
  return client.post('/api/visualisations/stress_map', params)
    .then((res) => res.data)
}
