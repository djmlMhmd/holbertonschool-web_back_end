// 10-update_uniq_items.js

export default function updateUniqueItems(maping) {
  if (!(maping instanceof Map)) {
    throw new Error('Cannot process');
  }

  for (const [key, value] of maping.entries()) {
    if (value === 1) {
      maping.set(key, 100);
    }
  }
  return maping;
}
