// Estados de una orden (ExtOrderMaster.STATUS_CHOICES) con su color en la UI
export const ORDER_STATUSES = [
  { value: 'pending', text: 'Pending', color: 'amber' },
  { value: 'processed', text: 'Processed', color: 'green' },
  { value: 'shipped', text: 'Shipped', color: 'deep-purple' },
  { value: 'delivered', text: 'Delivered', color: 'light-blue' },
  { value: 'cancelled', text: 'Cancelled', color: 'red' },
]

export function getOrderStatus(value) {
  return (
    ORDER_STATUSES.find((status) => status.value === value) || {
      value,
      text: value || 'Unknown',
      color: 'grey',
    }
  )
}
