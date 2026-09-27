export function joinUrl(base, path) {
  if (!base) return path
  if (!path) return base
  return base.replace(/\/+$/, '') + '/' + path.replace(/^\/+/, '')
}
