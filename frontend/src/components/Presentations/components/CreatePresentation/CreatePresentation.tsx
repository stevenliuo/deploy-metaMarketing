import { FC, useId, useState } from 'react';
import ItemBox from 'src/templates/ItemBox';
import { PlusOutlined } from '@ant-design/icons';
import styles from './CreatePresentation.module.css';
import { Modal, Form, Input } from 'antd';
import { generatePath, useNavigate } from 'react-router-dom';
import { titleRules } from 'src/helpers/rulesFields';
import { createPresentation } from 'src/clientApi/presentation';
import { PATH_PRESENTATION } from 'src/pages';

type FormValues = {
  title: string;
};

type FormProps = {
  disabled?: boolean;
  formId: string;
  onSubmit?: (value: FormValues) => void;
};

const CreatePresentationFrom: FC<FormProps> = ({
  formId,
  disabled,
  onSubmit,
}) => {
  return (
    <Form<FormValues>
      onFinish={onSubmit}
      layout="vertical"
      id={formId}
    >
      <Form.Item
        label="Title"
        name="title"
        rules={titleRules}
      >
        <Input disabled={disabled} />
      </Form.Item>
    </Form>
  );
};
type Props = {
  disabled?: boolean;
};
const CreatePresentation: FC<Props> = ({ disabled }) => {
  const navigate = useNavigate();
  const formId = useId();
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const openModal = () => {
    if (disabled) return;
    setOpen(true);
  };
  const closeModal = () => setOpen(false);
  const handleSubmit = async (values: FormValues) => {
    try {
      setLoading(true);

      const presentation = await createPresentation(values);
      closeModal();
      navigate(generatePath(PATH_PRESENTATION, { id: presentation.id }));
    } finally {
      setLoading(false);
    }
  };
  return (
    <>
      <ItemBox onClick={openModal}>
        <PlusOutlined className={styles.icon} />
      </ItemBox>
      <Modal
        destroyOnClose
        closable={!loading}
        okButtonProps={{ form: formId, htmlType: 'submit' }}
        title="Create Presentation"
        open={open}
        onCancel={closeModal}
      >
        <CreatePresentationFrom
          disabled={loading}
          formId={formId}
          onSubmit={handleSubmit}
        />
      </Modal>
    </>
  );
};

export default CreatePresentation;
