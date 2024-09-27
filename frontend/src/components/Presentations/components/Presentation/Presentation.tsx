import { DeleteOutlined } from '@ant-design/icons';
import { Popconfirm } from 'antd';
import Title from 'antd/es/typography/Title';
import classNames from 'classnames';
import { FC, useState, useCallback } from 'react';
import ItemBox from 'src/templates/ItemBox';
import styles from './Presentation.module.css';

type Props = {
  title: string;
  id: number;
  createdAt: string;
  updatedAt: string;
  onClick: () => void;
  onDelete: (id: number) => Promise<void>;
};
const stopPropagation = (e: React.MouseEvent) => e.stopPropagation();

const Presentation: FC<Props> = ({
  title,
  createdAt,
  updatedAt,
  onClick,
  onDelete,
  id,
}) => {
  const [loading, setLoading] = useState(false);
  const handleDelete = useCallback(async () => {
    try {
      setLoading(true);
      await onDelete(id);
    } finally {
      setLoading(false);
    }
  }, [onDelete, setLoading, id]);
  return (
    <ItemBox
      onClick={!loading ? onClick : undefined}
      style={{
        justifyContent: 'space-between',
        opacity: loading ? 0.5 : 1,
      }}
    >
      <div
        onClick={stopPropagation}
        style={{ width: '100%', display: 'flex', justifyContent: 'flex-end' }}
      >
        <Popconfirm
          disabled={loading}
          placement="leftTop"
          title="Are you sure to delete this file?"
          okText="Yes"
          cancelText="No"
          onConfirm={handleDelete}
        >
          <DeleteOutlined
            className={classNames(styles.deleteIcon, {
              [styles.disabled]: loading,
            })}
          />
        </Popconfirm>
      </div>
      <div
        style={{
          flexGrow: 1,
          justifyContent: 'center',
          display: 'flex',
          alignItems: 'center',
        }}
      >
        <Title level={4}>{title}</Title>
      </div>
      <div style={{ width: '100%' }}>
        {createdAt && (
          <div>
            <b>Created:</b> &nbsp;{createdAt}
          </div>
        )}
        {updatedAt && (
          <div>
            <b>Updated:</b> &nbsp;
            {updatedAt}
          </div>
        )}
      </div>
    </ItemBox>
  );
};

export default Presentation;
