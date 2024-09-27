import { Form, Input } from 'antd';
import { FC } from 'react';

type FeedbackData = {
  message: string;
};
type Props = {
  formId: string;
  onSubmit: (message: string) => void;
  disabled?: boolean;
};

const FeedbackFrom: FC<Props> = ({ formId, onSubmit, disabled }) => {
  const handleSubmit = (values: FeedbackData) => {
    onSubmit(values.message);
  };
  return (
    <Form
      id={formId}
      onFinish={handleSubmit}
    >
      <Form.Item
        name="message"
        rules={[
          {
            required: true,
            message: 'Please input your message!',
          },
          {
            max: 2500,
            message: 'Message must be less than 2500 characters!',
          },
        ]}
      >
        <Input.TextArea
          placeholder="Write your feedback here..."
          disabled={disabled}
          autoSize={{
            minRows: 6,
            maxRows: 12,
          }}
        />
      </Form.Item>
    </Form>
  );
};

export default FeedbackFrom;
