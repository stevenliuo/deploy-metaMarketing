import { EditOutlined, InfoCircleOutlined } from '@ant-design/icons';
import { Flex, Modal, Skeleton, Space, Tooltip } from 'antd';
import { FC, useId, useState } from 'react';
import styles from './InfoSection.module.css';
import { Presentation } from 'src/types/presentation';
import EditInfoForm from './EditInfoForm';
import { updatePresentation } from 'src/clientApi/presentation';

type Props = {
  title: string;
  tooltip?: string;
  presentation?: Presentation;
  propValue: keyof Omit<Presentation, 'slides' | 'workbook'>;
  onUpdated?: (presentation: Presentation) => void;
};

const InfoSection: FC<Props> = ({
  title,
  tooltip,
  propValue,
  presentation,
  onUpdated,
}) => {
  const formId = useId();
  const [visable, setVisable] = useState(false);
  const [loading, setLoading] = useState(false);
  const openModal = () => setVisable(true);
  const closeModal = () => setVisable(false);
  const handlerSubmit = async (values: Partial<Presentation>) => {
    try {
      setLoading(true);
      // @ts-ignore
      const newPresentation = await updatePresentation({
        ...presentation,
        ...values,
      });
      onUpdated?.(newPresentation);
      setVisable(false);
    } finally {
      setLoading(false);
    }
  };
  return (
    <>
      <div className={styles.box}>
        <Flex
          justify="space-between"
          className={styles.header}
        >
          <Space
            align="center"
            size="small"
          >
            <b>{title}</b>
            {tooltip && (
              <Tooltip title={tooltip}>
                <InfoCircleOutlined />
              </Tooltip>
            )}
          </Space>
          <EditOutlined
            className={styles.btnIcon}
            onClick={openModal}
          />
        </Flex>
        {presentation && <div>{presentation[propValue]}</div>}
        {!presentation && (
          <div className={styles.skeleton}>
            <Skeleton.Input
              style={{ width: '100%' }}
              active
              size="small"
            />
          </div>
        )}
      </div>
      <Modal
        title={`Update ${title}`}
        closable={!loading}
        open={visable}
        destroyOnClose
        onCancel={closeModal}
        cancelButtonProps={{ disabled: loading }}
        okButtonProps={{ form: formId, htmlType: 'submit', loading }}
        okText="Update"
      >
        <EditInfoForm
          propValue={propValue}
          disabled={loading}
          defaultValues={presentation}
          formId={formId}
          onSubmit={handlerSubmit}
        />
      </Modal>
    </>
  );
};

export default InfoSection;
