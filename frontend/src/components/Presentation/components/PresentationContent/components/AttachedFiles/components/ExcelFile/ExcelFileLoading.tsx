import { FileExcelOutlined } from '@ant-design/icons';
import { FC } from 'react';
import styles from './ExcelFile.module.css';
import { Flex, Skeleton } from 'antd';

const ExcelFileLoading: FC = () => {
  return (
    <div className={styles.box}>
      <Flex
        gap={4}
        justify="space-between"
        align="center"
      >
        <FileExcelOutlined className={styles.mainIcon} />
        <div className={styles.skeleton}>
          <Skeleton.Input
            style={{ width: '100%' }}
            active
            size="small"
          />
        </div>
      </Flex>
    </div>
  );
};

export default ExcelFileLoading;
