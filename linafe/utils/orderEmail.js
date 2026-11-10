// Adjuntos del correo de una orden (SaleAppSettings.EmailAttachments)
export const EMAIL_ATTACHMENT_OPTIONS = [
  { value: 'pdf', text: 'PDF', icon: 'mdi-file-pdf-box' },
  { value: 'xlsx', text: 'Excel', icon: 'mdi-microsoft-excel' },
  { value: 'both', text: 'Both', icon: 'mdi-paperclip' },
]

// Contenido seleccionable al enviar una orden por correo (toggles múltiples)
export const EMAIL_CONTENT_OPTIONS = [
  { value: 'pdf', text: 'PDF', icon: 'mdi-file-pdf-box' },
  { value: 'xlsx', text: 'Excel', icon: 'mdi-microsoft-excel' },
  { value: 'link', text: 'Link', icon: 'mdi-link-variant' },
]

// Opción de adjuntos de SaleApp (pdf | xlsx | both) -> lista de tipos
export function attachmentTypes(attachments) {
  return attachments === 'both' ? ['pdf', 'xlsx'] : [attachments || 'pdf']
}
