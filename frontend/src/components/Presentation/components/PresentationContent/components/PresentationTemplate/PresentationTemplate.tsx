import { FilePptOutlined, UploadOutlined } from '@ant-design/icons';
import { Button, Flex, Skeleton, Space, Upload } from 'antd';
import { FC, useState, useCallback } from 'react';
import styles from './PresentationTemplate.module.css';
import { Presentation } from 'src/types/presentation';
import { updatePresentation } from 'src/clientApi/presentation';
import { RcFile } from 'antd/es/upload';

type Props = {
  presentation?: Presentation;
  onUpdated?: (presentation: Presentation) => void;
};

const PresentationTemplate: FC<Props> = ({ presentation, onUpdated }) => {
  const [loading, setLoading] = useState(false);

  const handlerUpload = useCallback(
    async (file: RcFile) => {
      try {
        setLoading(true);

        // @ts-ignore
        const newPresentation = await updatePresentation({
          ...presentation,
          template_content: file,
          template_name: file.name,
        });
        onUpdated?.(newPresentation);
      } finally {
        setLoading(false);
      }
      return false;
    },
    [setLoading, presentation, onUpdated]
  );
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
            <b>Template name</b>
          </Space>
        </Flex>
        {presentation && (
          <Space
            size="large"
            align="center"
          >
            <Space
              size="small"
              align="center"
            >
              <FilePptOutlined className={styles.iconPPT} />{' '}
              {presentation.template_name || 'No file'}
            </Space>
            <Upload
              showUploadList={false}
              accept="application/vnd.ms-powerpoint, application/vnd.openxmlformats-officedocument.presentationml.presentation"
              beforeUpload={handlerUpload}
            >
              <Button
                disabled={loading}
                icon={<UploadOutlined />}
              >
                Click to Upload
              </Button>
            </Upload>
          </Space>
        )}
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
    </>
  );
};

export default PresentationTemplate;
