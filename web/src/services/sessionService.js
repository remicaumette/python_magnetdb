import client from "./client";

export function create(values) {
  const form = new FormData()
  for (const [key, value] of Object.entries(values)) {
    form.append(key, value)
  }
  return client.post(`/api/sessions`, form)
    .then((res) => res.data)
}
