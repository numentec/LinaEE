// Compartir una orden por WhatsApp sin usar su API:
//   - texto / enlace: click-to-chat (https://wa.me/<tel>?text=...)
//   - archivos: hoja de compartir del sistema (Web Share API)

const FILE_TYPES = {
  pdf: 'application/pdf',
  xlsx: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
}

// wa.me espera el teléfono en formato internacional, solo dígitos
export function normalizePhone(value) {
  return String(value || '').replace(/\D/g, '')
}

// Sin teléfono, WhatsApp deja elegir el contacto
export function whatsappUrl(phone, text) {
  return `https://wa.me/${normalizePhone(phone)}?text=${encodeURIComponent(
    text || ''
  )}`
}

// Texto del mensaje; link: enlace público (opcional)
export function orderMessage(order, link) {
  return [`Order # ${order.id}`, link].filter(Boolean).join('\n')
}

// Indica si el navegador puede compartir archivos de esos tipos (pdf | xlsx).
// Se comprueba con archivos vacíos para saberlo antes de descargar los reales.
export function canShareFileTypes(types) {
  if (!process.client || !navigator.share || !navigator.canShare) return false
  try {
    const files = types.map(
      (t) => new File([''], `order.${t}`, { type: FILE_TYPES[t] })
    )
    return navigator.canShare({ files })
  } catch (error) {
    return false
  }
}
