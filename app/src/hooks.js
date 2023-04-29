import { useState, useEffect } from 'react';

export function useLocalStorage(key, makeDefault) {
  let [val, _setVal] = useState(null);
  const setVal = v => {
    localStorage.setItem(key, JSON.stringify({ value: v }));
    _setVal(v);
  };
  useEffect(() => {
    const curVal = localStorage.getItem(key);
    if (!curVal) {
      _setVal(makeDefault());
    } else {
      _setVal(JSON.parse(curVal).value);
    }
  }, [makeDefault, key, _setVal]);
  return [val, setVal];
}
