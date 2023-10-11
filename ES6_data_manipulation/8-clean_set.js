// 8-clean_set.js

export default function cleanSet(set, startString) {
  let restString = '';

  if (startString) {
    for (const value of set) {
      if (value.startsWith(startString)) {
        const restOfString = value.slice(startString.length);

        if (restString !== '') {
          restString += '-';
        }
        restString += restOfString;
      }
    }
    return restString;
  }
  return '';
}
