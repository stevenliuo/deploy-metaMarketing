import {
  Route,
  createBrowserRouter,
  createRoutesFromElements,
  defer,
  useOutlet,
} from 'react-router-dom';
import { AuthProvider } from 'src/contexts/Auth';
import {
  PATH_DASHBOARD,
  PATH_EMAIL_VERIFICATION,
  PATH_SIGN_IN,
  PATH_SIGN_UP,
  PATH_PRESENTATION,
  PATH_PRESENTATIONS,
  PATH_SETTINGS,
  PATH_EMAIL_SENDED,
  PATH_FORGOT_PASSWORD,
  PATH_RESET_PASSWORD,
} from './pagePath';
import AccessLayout from './AccessLayout';
import ProtectedLayout from './ProtectedLayout';
import SignIn from 'src/components/SignIn';
import SignUp from 'src/components/SignUp';
import NotFound from 'src/components/NotFound';
import Dashboard from 'src/components/Dashboard';
import Presentations from 'src/components/Presentations';
import Presentation from 'src/components/Presentation';
import EmailVerification from 'src/components/EmailVerification';
import Settings from 'src/components/Settings';
import { getAccountInfo } from 'src/clientApi/settingApi';
import EmailSended from 'src/components/EmailSended';
import ForgotPassword from 'src/components/ForgotPassword';
import RestPassword from 'src/components/RestPassword';

const AuthLayout = () => {
  const outlet = useOutlet();
  return <AuthProvider>{outlet}</AuthProvider>;
};

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route
      element={<AuthLayout />}
      path="/"
    >
      <Route element={<AccessLayout />}>
        <Route
          element={<SignIn />}
          path={PATH_SIGN_IN}
        />
        <Route
          element={<SignUp />}
          path={PATH_SIGN_UP}
        />
        <Route
          element={<EmailVerification />}
          path={PATH_EMAIL_VERIFICATION}
        />
        <Route
          element={<ForgotPassword />}
          path={PATH_FORGOT_PASSWORD}
        />
        <Route
          element={<RestPassword />}
          path={PATH_RESET_PASSWORD}
        />
        <Route
          element={<EmailSended />}
          path={PATH_EMAIL_SENDED}
        />
      </Route>
      <Route
        loader={() => defer({ accountInfo: getAccountInfo() })}
        element={<ProtectedLayout />}
        path="/"
      >
        <Route
          element={<Dashboard />}
          path={PATH_DASHBOARD}
        />
        <Route
          element={<Presentations />}
          path={PATH_PRESENTATIONS}
        />
        <Route
          element={<Presentation />}
          path={PATH_PRESENTATION}
        />
        <Route
          path={PATH_SETTINGS}
          element={<Settings />}
        />
      </Route>

      <Route
        path="*"
        element={<NotFound />}
      />
    </Route>
  )
);

export default router;
