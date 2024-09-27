import {
  DeleteOutlined,
  EditOutlined,
  FileExcelOutlined,
  InboxOutlined,
  InsertRowBelowOutlined,
} from '@ant-design/icons';
import { FC, useCallback, useState } from 'react';
import styles from './ExcelFile.module.css';
import { Flex, Modal, Popconfirm, Space, Tooltip } from 'antd';
import classNames from 'classnames';
import { UpdateAttachedFile } from 'src/components/Presentation/hooks/useAttachedFiles';
import { updateAttachedFile } from 'src/clientApi/attachedPresentationsFiles';
import { RcFile } from 'antd/es/upload';
import Dragger from 'antd/es/upload/Dragger';

type Props = {
  name: string;
  listsNames: string[];
  createdAt?: string;
  isBusy?: boolean;
  onUpdatedAttachedFile?: (data: UpdateAttachedFile) => void;
  id: number;
  onUploaded?: (attachedFile: AttachedFile) => void;
  disabled?: boolean;
};

const ExcelFile: FC<Props> = ({
  name,
  listsNames,
  createdAt,
  isBusy,
  id,
  disabled,
  onUpdatedAttachedFile,
  onUploaded,
}) => {
  const [visable, setVisable] = useState(false);
  const [loading, setLoading] = useState(false);
  const updateFile = useCallback(
    async (file: RcFile) => {
      try {
        setLoading(true);
        const attachedFile = await updateAttachedFile(file, id);
        onUploaded?.(attachedFile);
        setVisable(false);
      } finally {
        setLoading(false);
      }
    },
    [id, onUploaded, setLoading]
  );
  return (
    <>
      <div className={styles.box}>
        <Flex
          justify="space-between"
          align="flex-start"
          gap={4}
        >
          <Space
            align="center"
            size={4}
          >
            <FileExcelOutlined className={classNames(styles.mainIcon)} />
            <Space
              direction="vertical"
              size={1}
            >
              <b className={styles.name}>{name}</b>
              {createdAt && (
                <span>
                  <b>Created:</b> {createdAt}
                </span>
              )}
            </Space>
          </Space>
          <Space size={4}>
            <EditOutlined
              className={classNames(styles.editIcon, {
                [styles.disabled]: disabled,
              })}
              onClick={disabled ? undefined : () => setVisable(true)}
            />
            <Popconfirm
              disabled={isBusy || disabled}
              placement="leftTop"
              title="Are you sure to delete this file?"
              okText="Yes"
              cancelText="No"
              onConfirm={() => {
                onUpdatedAttachedFile?.({ id, type: 'delete' });
              }}
            >
              <Tooltip
                title={isBusy ? 'This file is used on some slides' : undefined}
              >
                <DeleteOutlined
                  className={classNames(styles.deleteIcon, {
                    [styles.disabled]: disabled || isBusy,
                  })}
                />
              </Tooltip>
            </Popconfirm>
          </Space>
        </Flex>
        <Space
          className={styles.listsNames}
          wrap
          align="center"
        >
          <Tooltip title="Spreadsheets lists">
            <InsertRowBelowOutlined />
          </Tooltip>
          {listsNames.map((listName) => listName)}
        </Space>
      </div>
      <Modal
        open={visable}
        title={`Update file: ${name}`}
        confirmLoading={loading}
        onCancel={() => setVisable(false)}
        footer={null}
        closable={!loading}
      >
        <Dragger
          beforeUpload={updateFile}
          accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
          multiple
          showUploadList={false}
        >
          <p className="ant-upload-drag-icon">
            <InboxOutlined />
          </p>
          <p className="ant-upload-text">
            Click or drag Excel file (.xlsx) to this area to upload
          </p>
        </Dragger>
      </Modal>
    </>
  );
};

export default ExcelFile;
