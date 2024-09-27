import Title from 'antd/es/typography/Title';
import { FC } from 'react';

import styles from './AttachedFiles.module.css';
import { Empty, Flex } from 'antd';
import { ExcelFile, ExcelFileLoading, UploadFile } from './components';
import { getFormattedDate } from 'src/helpers/date';
import { Slide } from 'src/types/presentation';
import { UpdateAttachedFile } from 'src/components/Presentation/hooks/useAttachedFiles';

type Props = {
  id: number;
  loading?: boolean;
  files: AttachedFile[];
  onUploaded?: (attachedFile: AttachedFile) => void;
  slides: Slide[];
  onUpdatedAttachedFiles: (data: UpdateAttachedFile) => void;
  disabled?: boolean;
};

const AttachedFiles: FC<Props> = ({
  loading,
  id,
  onUploaded,
  files,
  slides,
  disabled,
  onUpdatedAttachedFiles,
}) => {
  return (
    <Flex
      vertical
      className={styles.box}
      gap={16}
    >
      <Title level={5}>Attached files:</Title>
      <div className={styles.files}>
        <Flex
          vertical
          gap={8}
        >
          {!loading &&
            files.map(({ name, created_at, spreadsheets, id }) => (
              <ExcelFile
                disabled={disabled}
                id={id}
                onUpdatedAttachedFile={onUpdatedAttachedFiles}
                onUploaded={onUploaded}
                isBusy={slides.some((slide) => slide.workbook === id)}
                key={id}
                name={name}
                createdAt={created_at ? getFormattedDate(created_at) : ''}
                listsNames={(spreadsheets || []).map(
                  (spreadsheet) => spreadsheet.name
                )}
              />
            ))}
          {files.length === 0 && <Empty />}
          {loading && (
            <>
              <ExcelFileLoading />
              <ExcelFileLoading />
              <ExcelFileLoading />
            </>
          )}
        </Flex>
      </div>
      <UploadFile
        id={id}
        onUploaded={onUploaded}
      />
    </Flex>
  );
};

export default AttachedFiles;
