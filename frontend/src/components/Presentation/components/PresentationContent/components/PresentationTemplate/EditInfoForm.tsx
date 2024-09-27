import { Form, Input } from 'antd';
import { FC } from 'react';
import { Presentation } from 'src/types/presentation';

type Props = {
  formId: string;
  onSubmit: (value: Partial<Presentation>) => void;
  propValue: keyof Presentation;
  defaultValues?: Presentation;
  disabled?: boolean;
};

const EditInfoForm: FC<Props> = ({
  onSubmit,
  formId,
  defaultValues,
  propValue,
  disabled,
}) => {
  return (
    <Form<Partial<Presentation>>
      onFinish={onSubmit}
      initialValues={defaultValues}
      id={formId}
    >
      <Form.Item name={propValue}>
        <Input.TextArea
          disabled={disabled}
          autoSize={{ minRows: 2, maxRows: 6 }}
        />
      </Form.Item>
    </Form>
  );
};

export default EditInfoForm;
