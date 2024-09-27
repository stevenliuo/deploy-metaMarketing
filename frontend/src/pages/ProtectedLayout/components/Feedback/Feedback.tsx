import { useId, useState } from 'react';
import { Modal } from 'antd';
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import { FeedbackBtn, FeedbackFrom } from './components';
import { sendFeedback } from 'src/clientApi/feedbackApi';

const Feedback = () => {
  const [loading, setLoading] = useState(false);
  const [visible, setVisible] = useState(false);
  const formId = useId();

  const handleSubmit = async (message: string) => {
    setLoading(true);
    try {
      await sendFeedback(message);
      setVisible(false);
    } finally {
      setLoading(false);
    }
  };

  return (
    <DndProvider backend={HTML5Backend}>
      <FeedbackBtn
        isOpen={visible}
        onClick={() => setVisible(true)}
      />
      <Modal
        destroyOnClose
        open={visible}
        closable={!loading}
        title="Send your feedback"
        onCancel={() => setVisible(false)}
        okButtonProps={{ form: formId, htmlType: 'submit', loading }}
        cancelButtonProps={{ disabled: loading }}
        okText="Send"
      >
        <FeedbackFrom
          formId={formId}
          onSubmit={handleSubmit}
          disabled={loading}
        />
      </Modal>
    </DndProvider>
  );
};

export default Feedback;
