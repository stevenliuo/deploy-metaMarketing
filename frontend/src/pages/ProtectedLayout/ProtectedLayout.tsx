import {
  Await,
  Navigate,
  useLoaderData,
  useLocation,
  useNavigate,
  useOutlet,
} from 'react-router-dom';
import { useAuth } from 'src/contexts/Auth';
import {
  PATH_DASHBOARD,
  PATH_SETTINGS,
  PATH_SIGN_IN,
  PATH_PRESENTATIONS,
} from '../pagePath';
import {
  Avatar,
  Dropdown,
  Flex,
  Layout,
  Menu,
  MenuProps,
  Skeleton,
} from 'antd';
import { Content, Header } from 'antd/es/layout/layout';
import { LogoutOutlined } from '@ant-design/icons';
import Logo from 'src/templates/Logo';
import { FC, Suspense, useEffect, useMemo } from 'react';
import { AccountInfo } from 'src/types/account';
import { Feedback } from './components';

const LayoutWithUser: FC<{ accountInfo: AccountInfo }> = ({ accountInfo }) => {
  const { setAccountInfo } = useAuth();
  const outlet = useOutlet();

  useEffect(() => {
    setAccountInfo(accountInfo);
  }, [accountInfo]);

  return <>{outlet}</>;
};

const ProtectedLayout = () => {
  const navigate = useNavigate();
  const { isAuthenticated, logout, accountInfo: userInfo } = useAuth();
  const location = useLocation();
  const capitalLetters = useMemo(() => {
    if (!userInfo) return 'U';
    return [(userInfo.first_name || '')[0], (userInfo.last_name || '')[0]]
      .filter(Boolean)
      .join('')
      .toUpperCase();
  }, [userInfo]);

  //@ts-ignore
  const { accountInfo } = useLoaderData();
  const items: MenuProps['items'] = [
    {
      key: PATH_DASHBOARD,
      label: 'Dashboard',
      onClick: () => navigate(PATH_DASHBOARD),
    },
    {
      key: PATH_PRESENTATIONS,
      label: 'Presentations',
      onClick: () => navigate(PATH_PRESENTATIONS),
    },
    {
      key: '/settings',
      label: 'Settings',
      onClick: () => navigate(PATH_SETTINGS),
    },
  ];
  const menuItem: MenuProps['items'] = [
    {
      key: 'logout',
      onClick: () => logout(),
      label: 'Logout',
      icon: <LogoutOutlined />,
    },
  ];

  if (!isAuthenticated) {
    return <Navigate to={PATH_SIGN_IN} />;
  }

  return (
    <Layout>
      <Header style={{ backgroundColor: 'white' }}>
        <Flex
          style={{ height: '100%' }}
          justify="space-between"
          gap={8}
          align="center"
        >
          <Logo />
          <Menu
            theme="light"
            mode="horizontal"
            selectedKeys={[location.pathname]}
            items={items}
            style={{ flex: 1, minWidth: 0 }}
          />
          <Dropdown menu={{ items: menuItem }}>
            <Avatar>{capitalLetters}</Avatar>
          </Dropdown>
        </Flex>
      </Header>
      <Content style={{ padding: '16px 50px', height: 'calc(100vh - 64px)' }}>
        <Suspense fallback={<Skeleton active />}>
          <Await
            resolve={accountInfo}
            children={(accountInfo) => (
              <LayoutWithUser accountInfo={accountInfo} />
            )}
          />
        </Suspense>
        <Feedback />
      </Content>
    </Layout>
  );
};

export default ProtectedLayout;
