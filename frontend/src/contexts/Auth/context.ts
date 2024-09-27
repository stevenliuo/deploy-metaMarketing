import { createContext } from 'react';
import AuthContext from './type';

const AuthContext = createContext<AuthContext>({
  isAuthenticated: false,
  login: () => {},
  logout: () => {},
  accountInfo: undefined,
  setAccountInfo: () => {},
});

export default AuthContext;
