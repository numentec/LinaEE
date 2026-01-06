// mock/catalogos.js
export const mockCatalogos = [
  {
    id: 'cat_001',
    company_id: 'cia_01',
    name: 'Catálogo Navidad',
    template: 'minimal',
    orientation: 'portrait', // portrait | landscape
    status: 'draft', // draft | ready | sent | archived
    pages_count: 12,
    updated_at: '2025-12-20T10:30:00Z',
  },
  {
    id: 'cat_002',
    company_id: 'cia_01',
    name: 'Catálogo Verano',
    template: 'minimal',
    orientation: 'landscape',
    status: 'ready',
    pages_count: 8,
    updated_at: '2025-12-10T15:10:00Z',
  },
  {
    id: 'cat_003',
    company_id: 'cia_01',
    name: 'Promos Fin de Año',
    template: 'minimal',
    orientation: 'portrait',
    status: 'sent',
    pages_count: 15,
    updated_at: '2025-12-05T09:05:00Z',
  },
]

export default mockCatalogos
