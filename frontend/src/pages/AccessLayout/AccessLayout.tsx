import { Navigate, useOutlet } from 'react-router-dom';
import styles from './AccessLayout.module.css';
import { useAuth } from 'src/contexts/Auth';
import { PATH_DASHBOARD } from '../pagePath';

const AccessLayout = () => {
  const { isAuthenticated } = useAuth();
  const outlet = useOutlet();
  if (isAuthenticated) {
    return <Navigate to={PATH_DASHBOARD} />;
  }
  return <div className={styles.container}>{outlet}</div>;
};

export default AccessLayout;
