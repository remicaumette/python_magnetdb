import client from "../client";

export function list() {
  return client.get('/api/admin/audit_logs').then((res) => res.data)
}
