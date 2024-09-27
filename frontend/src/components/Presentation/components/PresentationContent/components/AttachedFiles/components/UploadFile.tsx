import { InboxOutlined } from '@ant-design/icons';
import { RcFile } from 'antd/es/upload';
import Dragger from 'antd/es/upload/Dragger';
import { FC, useCallback } from 'react';
import { uploadFile } from 'src/clientApi/attachedPresentationsFiles';

type Props = {
  id: number;
  onUploaded?: (attachedFile: AttachedFile) => void;
};

const UploadFile: FC<Props> = ({ id, onUploaded }) => {
  const upload = useCallback(
    async (file: RcFile) => {
      const attachedFile = await uploadFile(file, id);
      onUploaded?.(attachedFile);
      return false;
    },
    [id]
  );

  return (
    <Dragger
      beforeUpload={upload}
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
  );
};

export default UploadFile;
