import { FC, useMemo, useState } from 'react';
import { PresentationContent, Toolbar } from './components';
import { Flex } from 'antd';
import { useParams } from 'react-router-dom';
import {
  useAttachedFiles,
  useGeneratedPresentation,
  usePresentation,
} from './hooks';
import Preview from './components/Preview';

const Presentation: FC = () => {
  const [typeContent, setTypeContent] = useState<'presentation' | 'preview'>(
    'presentation'
  );
  const { id } = useParams<{ id: string }>();
  const presentationId = +(id || 0);
  const {
    presentation,
    setPresentation,
    setNewSlide,
    deleteSlide,
    updateSlide,
  } = usePresentation(presentationId);
  const {
    loading: loadingAttached,
    attachedFiles,
    setAttachedFile,
    handleUpdatedAttachedFiles,
  } = useAttachedFiles(presentationId);
  const { status, generatePresentation, screenshots } =
    useGeneratedPresentation(presentationId);
  const hasFullData = useMemo(() => {
    if (!presentation) {
      return false;
    }
    return (
      !!presentation.title &&
      !!presentation.template_name &&
      !!presentation.slides.length
    );
  }, [presentation]);

  return (
    <Flex gap="middle">
      <Toolbar
        title={presentation?.title || 'Presentation'}
        typeContent={typeContent}
        presentationId={presentationId}
        setTypeContent={setTypeContent}
        isGenerating={status === 'loading'}
        hasFullData={hasFullData}
        hasGenerated={status === 'success'}
        generatePresentation={generatePresentation}
      />

      {typeContent === 'preview' && <Preview screenshots={screenshots} />}
      {typeContent == 'presentation' && (
        <PresentationContent
          generating={status === 'loading'}
          presentationId={presentationId}
          presentation={presentation}
          setPresentation={setPresentation}
          deleteSlide={deleteSlide}
          updateSlide={updateSlide}
          setNewSlide={setNewSlide}
          attachedFiles={attachedFiles}
          loadingAttached={loadingAttached}
          setAttachedFile={setAttachedFile}
          onUpdatedAttachedFiles={handleUpdatedAttachedFiles}
        />
      )}
    </Flex>
  );
};

export default Presentation;
