import { useCallback, useEffect, useState } from 'react';
import { getErrorMessage } from 'src/clientApi/helpers';
import {
  generatePresentationById,
  getPresentationScreenshots,
} from 'src/clientApi/presentation';
import { Screenshot } from 'src/types/presantationsScreenshots';

type UseGeneratedPresentation = {
  status: 'loading' | 'success' | 'error' | 'empty';
  generatePresentation(): Promise<void>;
  screenshots?: Screenshot[];
};

const useGeneratedPresentation = (id: number) => {
  const [screenshots, setScreenshots] = useState<Screenshot[]>([]);
  const [status, setStatus] =
    useState<UseGeneratedPresentation['status']>('empty');
  const getGeneratedPresentation = useCallback(async () => {
    try {
      const newScreenshots = await getPresentationScreenshots(id);
      setScreenshots(newScreenshots.screenshots);
      setStatus('success');
    } catch (e) {
      const errorMessages = getErrorMessage(e);
      if (errorMessages.includes('Generated PPT content empty')) {
        setStatus('loading');
      } else if (errorMessages.includes('Generating PPT is not starting yet')) {
        setStatus('empty');
      } else {
        setStatus('error');
      }
    }
  }, [id, setScreenshots]);
  const generatePresentation = useCallback(async () => {
    setStatus('loading');
    try {
      await generatePresentationById(id);
    } catch (e) {
      setStatus('error');
    }
  }, [setStatus, id]);

  useEffect(() => {
    if (status !== 'loading') {
      return;
    }
    const interval = setInterval(() => {
      getGeneratedPresentation();
    }, 30 * 1000);
    return () => clearInterval(interval);
  }, [getGeneratedPresentation, status]);

  useEffect(() => {
    getGeneratedPresentation();
  }, [getGeneratedPresentation]);
  return {
    status,
    generatePresentation,
    screenshots: screenshots,
  };
};

export default useGeneratedPresentation;
