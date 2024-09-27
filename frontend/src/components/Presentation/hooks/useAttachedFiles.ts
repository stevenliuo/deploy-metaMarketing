import { useCallback, useEffect, useState } from 'react';
import {
  deleteAttachedFile,
  getAttachedFilesByPresentationId,
} from 'src/clientApi/attachedPresentationsFiles';

export type UpdateAttachedFile = {
  id: number;
  type: 'update' | 'delete';
};

type UsePresentation = {
  attachedFiles: AttachedFile[];
  loading: boolean;
  setAttachedFile: (presentation: AttachedFile) => void;
  handleUpdatedAttachedFiles: (data: UpdateAttachedFile) => void;
};

const useAttachedFiles = (id: number): UsePresentation => {
  const [attachedFiles, setAttachedFiles] = useState<AttachedFile[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const setAttachedFile = useCallback(
    (attachedFile: AttachedFile) => {
      setAttachedFiles((prev) => {
        if (prev.some((file) => file.id === attachedFile.id)) {
          return prev.map((file) =>
            file.id === attachedFile.id ? attachedFile : file
          );
        }
        return [...prev, attachedFile];
      });
    },
    [setAttachedFiles]
  );
  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      const files = await getAttachedFilesByPresentationId(id);
      setAttachedFiles(files);
    } finally {
      setLoading(false);
    }
  }, [id, setLoading, setAttachedFiles]);

  const handleUpdatedAttachedFiles = useCallback(
    async ({ id, type }: UpdateAttachedFile) => {
      try {
        if (type === 'delete') {
          setAttachedFiles((prev) => prev.filter((file) => file.id !== id));
          await deleteAttachedFile(id);
        } else {
          console.error('Invalid type');
        }
      } catch (error) {
        loadData();
      }
    },
    [loadData, setAttachedFiles]
  );

  useEffect(() => {
    loadData();
  }, [loadData]);

  return {
    attachedFiles,
    loading,
    setAttachedFile,
    handleUpdatedAttachedFiles,
  };
};

export default useAttachedFiles;
