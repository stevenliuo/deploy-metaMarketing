import { useCallback, useState } from 'react';
import { Button, Form, Input } from 'antd';
import { useForm } from 'antd/es/form/Form';
import Title from 'antd/es/typography/Title';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { confirmPasswordRules, passwordRules } from 'src/helpers/rulesFields';
import { useAuth } from 'src/contexts/Auth';
import { PATH_SIGN_IN } from 'src/pages';
import styles from './RestPassword.module.css';
import {
  ResetPasswordData,
  SignUpData,
  resetPassword,
} from 'src/clientApi/authApi';
type FormValues = Pick<ResetPasswordData, 'password' | 'password2'>;

const RestPassword = () => {
  const navigate = useNavigate();
  const [form] = useForm<SignUpData>();
  const [searchParams] = useSearchParams();
  const { login } = useAuth();
  const [loading, setLoading] = useState(false);
  const { isFieldTouched, validateFields } = form;
  const handleSubmit = useCallback(
    async (values: FormValues) => {
      try {
        setLoading(true);
        await resetPassword({
          ...values,
          token: searchParams.get('token') || '',
          uid: atob(searchParams.get('uid') || ''),
        });
        setLoading(false);
        navigate(PATH_SIGN_IN);
      } finally {
        setLoading(false);
      }
    },
    [login, setLoading, searchParams]
  );
  const handlerChangePassword = useCallback(() => {
    if (!isFieldTouched('password2')) {
      return;
    }
    validateFields(['password2']);
  }, [isFieldTouched, validateFields]);

  return (
    <div className={styles.content}>
      <Title
        className={styles.textCenter}
        level={3}
      >
        Reset Password
      </Title>
      <Form
        form={form}
        layout="vertical"
        onFinish={handleSubmit}
      >
        <Form.Item
          label="Password"
          name="password"
          rules={passwordRules}
        >
          <Input.Password
            disabled={loading}
            onChange={handlerChangePassword}
            placeholder="Password"
          />
        </Form.Item>
        <Form.Item
          label="Confirm password"
          name="password2"
          rules={confirmPasswordRules}
        >
          <Input.Password
            disabled={loading}
            placeholder="Confirm password"
          />
        </Form.Item>
        <Form.Item>
          <Button
            loading={loading}
            block
            type="primary"
            htmlType="submit"
          >
            Set up new password
          </Button>
        </Form.Item>
      </Form>
      <div className={styles.textCenter}>
        Have an account? <Link to={PATH_SIGN_IN}>Sign In</Link>
      </div>
    </div>
  );
};

export default RestPassword;
