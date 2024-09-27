import { Button } from 'antd';
import Title from 'antd/es/typography/Title';
import { useNavigate, useSearchParams } from 'react-router-dom';
import styles from './EmailVerification.module.css';
import { useAuth } from 'src/contexts/Auth';
import { PATH_SIGN_IN, PATH_SIGN_UP } from 'src/pages';
import { useEffect, useState } from 'react';
import { emailConfirm } from 'src/clientApi/authApi';
import { LoadingOutlined } from '@ant-design/icons';
import classNames from 'classnames';
import { getErrorMessage } from 'src/clientApi/helpers';

const EmailVerification = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [state, setState] = useState<'loading' | 'error'>('loading');
  const [errorMessages, setErrorMessages] = useState<string[]>([]);

  useEffect(() => {
    const confirm = async () => {
      try {
        const tokens = await emailConfirm(
          atob(searchParams.get('uid') || ''),
          searchParams.get('token')
        );

        if (!tokens.access || !tokens.refresh) {
          navigate(PATH_SIGN_IN);
        } else {
          login(tokens.access, tokens.refresh);
        }
      } catch (error) {
        setErrorMessages(getErrorMessage(error));
        setState('error');
      }
    };

    confirm();
  }, [searchParams]);
  return (
    <div className={classNames(styles.content, styles.textCenter)}>
      {state === 'loading' && (
        <>
          <Title level={3}>Just a Bit More Magic!</Title>
          <p className={styles.textCenter}>Your account is almost ready</p>
          <p className={styles.textCenter}>
            Sit tight, you're moments away <br /> from exporting reports faster!
          </p>
          <LoadingOutlined className={styles.loadingIcon} />
        </>
      )}
      {state === 'error' && (
        <>
          <Title level={3}>Uh-oh! We Hit a Problem!</Title>
          <p className={styles.textCenter}>
            {errorMessages.map((message, i) => (
              <div key={i}>{message}</div>
            ))}
          </p>
          <p>
            <b>Need help?</b> Feel free to contact us at
            support@metamarketing.com to complete your account setup.
          </p>
          <p>We&apos;re here to assist you!</p>
          <div>
            <Button href={PATH_SIGN_UP}>Back</Button>
          </div>
        </>
      )}
    </div>
  );
};

export default EmailVerification;
