import { useCallback, useState } from 'react';
import { Button, Form, Input } from 'antd';
import { useForm } from 'antd/es/form/Form';
import Title from 'antd/es/typography/Title';
import { Link, useNavigate } from 'react-router-dom';
import {
  confirmPasswordRules,
  firstNameRules,
  lastNameRules,
  passwordRules,
  requiredEmailRules,
} from 'src/helpers/rulesFields';
import { InputEmail } from 'src/templates';
import { useAuth } from 'src/contexts/Auth';
import { PATH_EMAIL_SENDED, PATH_SIGN_IN } from 'src/pages';
import styles from './SignUp.module.css';
import { SignUpData, signUpAccount } from 'src/clientApi/authApi';

const SignUp = () => {
  const navigate = useNavigate();
  const [form] = useForm<SignUpData>();
  const { login } = useAuth();
  const [loading, setLoading] = useState(false);
  const { isFieldTouched, validateFields } = form;
  const handleSubmit = useCallback(
    async (values: SignUpData) => {
      try {
        setLoading(true);
        await signUpAccount(values);
        navigate(PATH_EMAIL_SENDED);
      } finally {
        setLoading(false);
      }
    },
    [login, setLoading]
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
        Sign Up
      </Title>
      <p className={styles.textCenter}>Create expert reports faster!</p>
      <Form
        form={form}
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
        <Form.Item
          label="First name"
          name="first_name"
          rules={firstNameRules}
        >
          <Input
            disabled={loading}
            placeholder="First name"
          />
        </Form.Item>
        <Form.Item
          label="Last name"
          name="last_name"
          rules={lastNameRules}
        >
          <Input
            disabled={loading}
            placeholder="Last name"
          />
        </Form.Item>
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
            Sign Up
          </Button>
        </Form.Item>
      </Form>
      <div className={styles.textCenter}>
        Have an account? <Link to={PATH_SIGN_IN}>Sign In</Link>
      </div>
    </div>
  );
};

export default SignUp;
