import { AccountInfo } from 'src/types/account';

type AuthContext = {
  accountInfo: AccountInfo | undefined;
  setAccountInfo: (accountInfo: AccountInfo) => void;
  isAuthenticated: boolean;
  login: (accessToken: string, refreshToken: string) => void;
  logout: () => void;
};

export default AuthContext;
