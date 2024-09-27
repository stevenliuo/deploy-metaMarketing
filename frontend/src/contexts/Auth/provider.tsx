import { FC, ReactNode, useCallback, useEffect, useState } from 'react';
import AuthContext from './context';
import useLocalStorage from 'src/hooks/useLocalStorage';
import { AUTH_TOKEN, REFRESH_TOKEN } from 'src/helpers/constants';
import { AccountInfo } from 'src/types/account';

type Props = {
  children: ReactNode;
};

const AuthProvider: FC<Props> = ({ children }) => {
  const { storageValue: accessToken, setStorageValue: setAccessToken } =
    useLocalStorage<string>(AUTH_TOKEN);
  const { setStorageValue: setRefreshToken } =
    useLocalStorage<string>(REFRESH_TOKEN);
  const [token, setToken] = useState<string | undefined>(accessToken);
  const [accountInfo, setAccountInfo] = useState<AccountInfo | undefined>();

  const login = useCallback(
    (accessToken: string, refreshToken: string) => {
      setAccessToken(accessToken);
      setRefreshToken(refreshToken);
    },
    [setAccessToken, setRefreshToken]
  );
  const logout = useCallback(() => {
    setAccessToken(undefined);
    setRefreshToken(undefined);
  }, [setToken]);

  useEffect(() => {
    setToken(accessToken);
  }, [accessToken, setToken]);

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated: !!token,
        login,
        logout,
        accountInfo,
        setAccountInfo,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
