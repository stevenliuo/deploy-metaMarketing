import { Button, Form } from 'antd';
import Title from 'antd/es/typography/Title';
import { Link, useNavigate } from 'react-router-dom';
import styles from './ForgotPassword.module.css';
import { requiredEmailRules } from 'src/helpers/rulesFields';
import { InputEmail } from 'src/templates';
import { useAuth } from 'src/contexts/Auth';
import { PATH_EMAIL_SENDED, PATH_SIGN_IN } from 'src/pages';
import { useCallback, useState } from 'react';
import { forgotPassword } from 'src/clientApi/authApi';

type EmailForm = { email: string };

const ForgotPassword = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [loading, setLoading] = useState(false);
  const handleSubmit = useCallback(
    async (values: EmailForm) => {
      try {
        setLoading(true);
        await forgotPassword(values.email);
        navigate(PATH_EMAIL_SENDED);
      } finally {
        setLoading(false);
      }
    },
    [login, setLoading]
  );
  return (
    <div className={styles.content}>
      <Title
        className={styles.textCenter}
        level={3}
      >
        Forgot password
      </Title>
      <Form<EmailForm>
        layout="vertical"
        onFinish={handleSubmit}
      >
        <Form.Item
          label="Email address"
          rules={requiredEmailRules}
          name="email"
        >
          <InputEmail
            disabled={loading}
            placeholder="Email"
          />
        </Form.Item>

        <Form.Item>
          <Button
            block
            loading={loading}
            type="primary"
            htmlType="submit"
          >
            Send email
          </Button>
        </Form.Item>
      </Form>

      <div className={styles.textCenter}>
        Have an account? <Link to={PATH_SIGN_IN}>Sign In</Link>
      </div>
    </div>
  );
};

export default ForgotPassword;
