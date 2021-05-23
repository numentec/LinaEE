// Sort by integer and fractional parts of type "int / frac"
function sortIntFrac(val1, val2) {
  // Handling null values
  if (!val1 && val2) return -1
  if (!val1 && !val2) return 0
  if (val1 && !val2) return 1

  // If not null values
  const [int1 = '0', frac1 = '0'] = val1.split('/')
  const [int2 = '0', frac2 = '0'] = val2.split('/')

  const v1 = Number(int1.trim()) + Number(frac1.trim()) / 100
  const v2 = Number(int2.trim()) + Number(frac2.trim()) / 100

  if (v1 < v2) return -1
  if (v1 === v2) return 0
  if (v1 > v2) return 1
}

export function selFunction(func) {
  const funcs = {
    sortIntFrac,
  }
  return funcs[func] ?? undefined
}
