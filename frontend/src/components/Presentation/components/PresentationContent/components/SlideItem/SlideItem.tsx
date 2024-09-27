import { Card, Flex, Modal, Space } from 'antd';
import { FC, useCallback, useId, useMemo, useState } from 'react';

import styles from './SlideItem.module.css';
import { DeleteOutlined, EditOutlined, CopyOutlined } from '@ant-design/icons';
import classNames from 'classnames';
import { Slide, SlideFormValue } from 'src/types/presentation';
import { deleteSlide, updateSlide } from 'src/clientApi/slideApi';
import SlideForm from '../SlideForm';
import { COPIED_SLIDE } from 'src/helpers/constants';

type Props = {
  position: number;
  slide: Slide;
  onDelete: (id: number) => void;
  onUpdated: (slide: Slide) => void;
  workbooks: AttachedFile[];
  setSlideIsCopied: (slideIsCopied: boolean) => void;
};

const SlideItem: FC<Props> = ({
  slide,
  onDelete,
  onUpdated,
  workbooks,
  position,
  setSlideIsCopied,
}) => {
  const formId = useId();
  const [visible, setVisible] = useState(false);
  const [loading, setLoading] = useState(false);
  const workbookInfo = useMemo(() => {
    const workbook = workbooks.find((wb) => wb.id === slide.workbook);
    if (!workbook) return;
    const spreadsheet = workbook.spreadsheets.find(
      (spreadsheet) => spreadsheet.id === slide.input_spreadsheet
    );
    let workbookInfo = `${workbook.name} - ${spreadsheet?.name}`;
    return workbookInfo;
  }, [slide, workbooks]);
  const handleDelete = useCallback(async () => {
    try {
      setLoading(true);
      await deleteSlide(slide.id);
      onDelete(slide.id);
    } finally {
      setLoading(false);
    }
  }, [onDelete, slide, setLoading]);
  const handleUpdate = useCallback(
    async (values: SlideFormValue) => {
      try {
        setLoading(true);
        const updatedSlide = await updateSlide({ ...slide, ...values });
        onUpdated(updatedSlide);
        setVisible(false);
      } finally {
        setLoading(false);
      }
    },
    [onUpdated, slide]
  );
  const handleCopy = () => {
    let copiedSlideValues = {
      "perform_analysis": slide.perform_analysis,
      "slide_option": slide.slide_option,
      "specific_title": slide.specific_title,
      "specific_instructions": slide.specific_instructions,
      "input_spreadsheet": slide.input_spreadsheet,
      "workbook": slide.workbook
    };
    localStorage.setItem(COPIED_SLIDE, JSON.stringify(copiedSlideValues));
    setSlideIsCopied(true);
  }
  const closeModal = useCallback(() => {
    if (loading) return;
    setVisible(false);
  }, [loading, setVisible]);
  const openModal = useCallback(() => {
    setVisible(true);
  }, [setVisible]);

  return (
    <>
      <Card
        loading={loading}
        className={styles.box}
        title={`Slide ${position}`}
        extra={
          <Space size={8}>
            <EditOutlined
              className={classNames(styles.iconBtn, styles.editBtn)}
              onClick={loading ? undefined : openModal}
            />
            <CopyOutlined
              className={classNames(styles.iconBtn, styles.copyBtn)}
              onClick={loading ? undefined : handleCopy} 
            />
            <DeleteOutlined
              className={classNames(styles.iconBtn, styles.deleteBtn)}
              onClick={loading ? undefined : handleDelete}
            />
          </Space>
        }
      >
        <Flex
          vertical
          gap="middle"
        >
          <div>
            <b>Title:</b> {slide.specific_title}
          </div>
          <div>
            <b>File Name:</b> {workbookInfo}
          </div>
          <div>
            <b>Instruction:</b> {slide.specific_instructions}
          </div>
        </Flex>
      </Card>
      <Modal
        closable={!loading}
        open={visible}
        title="Update slide"
        onCancel={closeModal}
        destroyOnClose
        okButtonProps={{ form: formId, htmlType: 'submit', loading }}
        okText="Save"
      >
        <SlideForm
          defaultValues={slide}
          workbooks={workbooks}
          formId={formId}
          onSubmit={handleUpdate}
        />
      </Modal>
    </>
  );
};

export default SlideItem;
