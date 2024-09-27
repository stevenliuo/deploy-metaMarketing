import {
  SortAscendingOutlined,
  SortDescendingOutlined,
} from '@ant-design/icons';
import { Input, Radio, Space } from 'antd';
import { FC } from 'react';
import styles from './Toolbar.module.css';
import { Presentation } from 'src/types/presentation';
import classNames from 'classnames';

type Props = {
  sortDirection: 'asc' | 'desc';
  sortFiled: keyof Presentation;
  setKeyword: (keyword: string) => void;
  setSortFiled: (sortFiled: keyof Presentation) => void;
  setSortDirection: (sortDirection: 'asc' | 'desc') => void;
};

const Toolbar: FC<Props> = ({
  sortDirection,
  sortFiled,
  setSortFiled,
  setSortDirection,
  setKeyword,
}) => (
  <div className={styles.box}>
    <Space>
      <b>Search:</b>
      <Input
        size="small"
        placeholder="Search by name"
        allowClear
        onChange={(e) => setKeyword(e.target.value)}
      />
      <b>Sort by:</b>{' '}
      <Radio.Group
        defaultValue="newest"
        buttonStyle="solid"
        value={sortFiled}
        onChange={(e) => setSortFiled(e.target.value)}
      >
        <Radio value="created_at">Created Date</Radio>
        <Radio value="updated_at">Updated Date</Radio>
      </Radio.Group>
      <>
        <SortAscendingOutlined
          className={classNames(styles.sortIcon, {
            [styles.active]: sortDirection === 'asc',
          })}
          onClick={() => setSortDirection('asc')}
        />
        <SortDescendingOutlined
          className={classNames(styles.sortIcon, {
            [styles.active]: sortDirection === 'desc',
          })}
          onClick={() => setSortDirection('desc')}
        />
      </>
    </Space>
  </div>
);

export default Toolbar;
