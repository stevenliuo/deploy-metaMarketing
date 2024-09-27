import { useCallback, useState } from 'react';
import { getLocalStorage } from '../helpers/storage';
type LocalStorage<T> = {
  storageValue?: T;
  setStorageValue: (value?: T) => void;
};

const useLocalStorage = <T = any>(
  key: string,
  defaultValue?: T
): LocalStorage<T> => {
  const [value, setValue] = useState<T | undefined>(
    getLocalStorage(key) || defaultValue
  );

  const setStorageValue = useCallback(
    (value?: T) => {
      if (value === undefined || value === null) {
        localStorage.removeItem(key);
        setValue(undefined);
        return;
      }
      localStorage.setItem(key, JSON.stringify(value));
      setValue(value);
    },
    [key, setValue]
  );

  return { storageValue: value, setStorageValue };
};

export default useLocalStorage;
