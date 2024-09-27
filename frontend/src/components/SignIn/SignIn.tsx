import { Button, Form, Input } from 'antd';
import Title from 'antd/es/typography/Title';
import { Link } from 'react-router-dom';
import styles from './SignIn.module.css';
import {
  passwordOnlyRequiredRules,
  requiredEmailRules,
} from 'src/helpers/rulesFields';
import { InputEmail } from 'src/templates';
import { useAuth } from 'src/contexts/Auth';
import { PATH_FORGOT_PASSWORD, PATH_SIGN_UP } from 'src/pages';
import { useCallback, useState } from 'react';
import { SignInData, signInAccount } from 'src/clientApi/authApi';

const SignIn = () => {
  const { login } = useAuth();
  const [loading, setLoading] = useState(false);
  const handleSubmit = useCallback(
    async (values: SignInData) => {
      try {
        setLoading(true);
        const tokens = await signInAccount(values);
        login(tokens.access, tokens.refresh);
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
        Sign in to MetaMarketing
      </Title>
      <Form<SignInData>
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
          label="Password"
          name="password"
          rules={passwordOnlyRequiredRules}
        >
          <Input.Password
            disabled={loading}
            placeholder="Password"
          />
        </Form.Item>
        <Form.Item>
          <Button
            block
            loading={loading}
            type="primary"
            htmlType="submit"
          >
            Sign In
          </Button>
        </Form.Item>
      </Form>
      <p className={styles.textCenter}>
        <Link to={PATH_FORGOT_PASSWORD}>Forgot password?</Link>
      </p>
      <div className={styles.textCenter}>
        No company account yet? <Link to={PATH_SIGN_UP}>Register</Link>
      </div>
    </div>
  );
};

export default SignIn;
