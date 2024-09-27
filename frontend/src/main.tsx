import ReactDOM from 'react-dom/client';
import { RouterProvider } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import './index.css';
import router from './pages';
import { COLOR_PRIMARY } from './helpers/constants';

ReactDOM.createRoot(document.getElementById('root')!).render(
  //<React.StrictMode>
  <ConfigProvider
    theme={{
      token: {
        colorPrimary: COLOR_PRIMARY,
        borderRadius: 0,
      },
    }}
  >
    <RouterProvider router={router} />
  </ConfigProvider>
  //</React.StrictMode>
);
