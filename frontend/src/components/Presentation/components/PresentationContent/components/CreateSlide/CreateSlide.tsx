import { PlusOutlined } from '@ant-design/icons';
import { FC, useCallback, useId, useState } from 'react';
import ItemBox from 'src/templates/ItemBox';
import styles from './CreateSlide.module.css';
import { Modal } from 'antd';
import SlideForm from '../SlideForm';
import { Slide, SlideFormValue } from 'src/types/presentation';
import { createSlide } from 'src/clientApi/slideApi';

type Props = {
  presentationId: number;
  onCreated: (slide: Slide) => void;
  workbooks: AttachedFile[];
};
const CreateSlide: FC<Props> = ({ presentationId, onCreated, workbooks }) => {
  const formId = useId();
  const [loading, setLoading] = useState(false);
  const [visible, setVisible] = useState(false);
  const openModal = () => {
    setVisible(true);
  };
  const closeModal = () => {
    if (loading) return;
    setVisible(false);
  };

  const handleCreate = useCallback(
    async (values: SlideFormValue) => {
      try {
        const slide = await createSlide({ ...values, project: presentationId });
        onCreated(slide);
        setVisible(false);
        setLoading(true);
      } finally {
        setLoading(false);
      }
    },
    [presentationId, onCreated, setVisible, setLoading]
  );

  return (
    <>
      <ItemBox onClick={openModal}>
        <PlusOutlined className={styles.icon} />
      </ItemBox>
      <Modal
        closable={!loading}
        open={visible}
        title="Create new slide"
        onCancel={closeModal}
        destroyOnClose
        okButtonProps={{ form: formId, htmlType: 'submit', loading }}
        okText="Create"
      >
        <SlideForm
          workbooks={workbooks}
          formId={formId}
          onSubmit={handleCreate}
        />
      </Modal>
    </>
  );
};

export default CreateSlide;
