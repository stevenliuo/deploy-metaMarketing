type GetFromString = <T = any>(data: string) => T | null;

export const parseJSON: GetFromString = (dataString: string) => {
  let value = null;

  try {
    value = JSON.parse(dataString || 'null');
  } catch (error) {
    return null;
  }

  return value;
};

export const getLocalStorage = <T = any>(key: string) =>
  parseJSON<T>(localStorage.getItem(key) || 'null');
