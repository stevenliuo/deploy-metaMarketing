import { FC, ReactNode } from 'react';
import styles from './DashboardItem.module.css';
import { Space } from 'antd';
import ItemBox from 'src/templates/ItemBox';

type Props = {
  icon: ReactNode;
  title: string;
  onClick?: () => void;
  description?: string;
};

const DashboardItem: FC<Props> = ({ icon, title, onClick, description }) => {
  return (
    <ItemBox
      onClick={onClick}
      height={250}
      width={250}
    >
      <Space
        direction="vertical"
        size={8}
        align="center"
      >
        <div className={styles.icon}>{icon}</div>
        <div className={styles.title}>{title}</div>
        <div className={styles.description}>{description}</div>
      </Space>
    </ItemBox>
  );
};

export default DashboardItem;
