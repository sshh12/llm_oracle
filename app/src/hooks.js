import { useState, useEffect, useCallback, useRef } from 'react';

export function useLocalStorage(key, makeDefault) {
  let [val, _setVal] = useState(null);
  const setVal = useCallback(
    v => {
      localStorage.setItem(key, JSON.stringify({ value: v }));
      _setVal(v);
    },
    [key]
  );
  const makeDefaultRef = useRef(makeDefault);
  useEffect(() => {
    const curVal = localStorage.getItem(key);
    if (!curVal) {
      setVal(makeDefaultRef());
    } else {
      setVal(JSON.parse(curVal).value);
    }
  }, [key, setVal, makeDefaultRef]);
  return [val, setVal];
}
