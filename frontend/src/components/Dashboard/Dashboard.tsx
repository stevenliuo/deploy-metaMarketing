import { Flex } from 'antd';
import { FilePptOutlined } from '@ant-design/icons';
import { FC } from 'react';
import { DashboardItem } from './components';
import { useNavigate } from 'react-router-dom';
import { PATH_PRESENTATIONS } from 'src/pages';

const Dashboard: FC = () => {
  const navigate = useNavigate();
  return (
    <Flex
      gap="large"
      wrap
    >
      <DashboardItem
        onClick={() => navigate(PATH_PRESENTATIONS)}
        icon={<FilePptOutlined />}
        title="Presentations"
        description="Create and manage your presentations"
      />
    </Flex>
  );
};

export default Dashboard;
