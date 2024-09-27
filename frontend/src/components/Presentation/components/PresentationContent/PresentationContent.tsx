import { FC, useEffect, useRef, useCallback } from "react";
import { Flex, Spin, Button } from "antd";
import styles from './PresentationContent.module.css';
import Title from 'antd/es/typography/Title';
import { Presentation, Slide } from 'src/types/presentation';
import {
  CreateSlide,
  InfoSection,
  SlideItem,
  AttachedFiles,
  PresentationTemplate,
} from './components';
import { UpdateAttachedFile } from '../../hooks/useAttachedFiles';
import { createSlide } from "src/clientApi/slideApi";
import { COPIED_SLIDE } from "src/helpers/constants";
type Props = {
  slideIsCopied: boolean;
  setSlideIsCopied: (slideIsCopied: boolean) => void;
  presentationId: number;
  presentation?: Presentation;
  setPresentation: (presentation: Presentation) => void;
  setNewSlide: (newSlide: Slide) => void;
  deleteSlide: (id: number) => void;
  updateSlide: (updateSlide: Slide) => void;
  attachedFiles: AttachedFile[];
  loadingAttached: boolean;
  setAttachedFile: (presentation: AttachedFile) => void;
  onUpdatedAttachedFiles: (data: UpdateAttachedFile) => void;
  generating: boolean;
};

const PresentationContent: FC<Props> = ({
  slideIsCopied,
  setSlideIsCopied,
  presentation,
  attachedFiles,
  setPresentation,
  deleteSlide,
  updateSlide,
  setNewSlide,
  presentationId,
  loadingAttached,
  setAttachedFile,
  generating,
  onUpdatedAttachedFiles,
}) => {
  const contentRef = useRef<HTMLDivElement>(null);

  const handlePaste = useCallback(
    async () => {
      try {        
        const slideValues = JSON.parse(localStorage.getItem(COPIED_SLIDE)||"")
        
        const slide = await createSlide({ ...slideValues, project: presentationId });
        setNewSlide(slide);
        localStorage.removeItem(COPIED_SLIDE)
        setSlideIsCopied(false);
      } finally {

      }
    },
    [presentationId, setNewSlide]
  );
  useEffect(() => {
    if (generating) {
      contentRef.current?.scrollIntoView({
        behavior: 'instant',
        block: 'start',
      });
    }
  }, [generating]);

  return (
    <>
      <div className={styles.content}>
        <Spin
          spinning={generating}
          size="large"
          tip="Creating a presentation"
        >
          <Flex
            vertical
            gap="middle"
            ref={contentRef}
          >
            <InfoSection
              title="Title"
              presentation={presentation}
              propValue="title"
              tooltip="A title of the report (this will be used as filename when downloading the report)"
              onUpdated={setPresentation}
            />
            <InfoSection
              title="Type of report"
              presentation={presentation}
              propValue="description"
              tooltip="A description of the type of report"
              onUpdated={setPresentation}
            />
            <InfoSection
              title="Subtitle"
              presentation={presentation}
              propValue="subtitle"
              onUpdated={setPresentation}
            />
            <InfoSection
              title="Default instruction"
              presentation={presentation}
              propValue="footer"
              tooltip="A description that will be show on each slide"
              onUpdated={setPresentation}
            />
            <PresentationTemplate
              presentation={presentation}
              onUpdated={setPresentation}
            />
            <Title level={5}>Slides:</Title>
            <Flex
              gap="middle"
              wrap
            >
              {presentation?.slides?.map((slide, i) => (
                <SlideItem
                  key={slide.id}
                  slide={slide}
                  onDelete={deleteSlide}
                  onUpdated={updateSlide}
                  workbooks={presentation?.workbook}
                  position={i + 1}
                />
              ))}
              {!!presentation && (
                <CreateSlide
                  workbooks={attachedFiles}
                  presentationId={presentationId}
                  onCreated={setNewSlide}
                />
              )}
              {slideIsCopied && <Button onClick={handlePaste}>Paste Slide</Button>}
            </Flex>
          </Flex>
        </Spin>
      </div>
      <AttachedFiles
        loading={loadingAttached}
        id={presentationId}
        files={attachedFiles}
        onUploaded={setAttachedFile}
        slides={presentation?.slides || []}
        disabled={generating}
        onUpdatedAttachedFiles={onUpdatedAttachedFiles}
      />
    </>
  );
};

export default PresentationContent;
