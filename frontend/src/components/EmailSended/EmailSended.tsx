import Title from 'antd/es/typography/Title';
import { Link } from 'react-router-dom';
import styles from './EmailSended.module.css';
import { PATH_SIGN_IN } from 'src/pages';
import { MailOutlined } from '@ant-design/icons';

const SignIn = () => (
  <div className={styles.content}>
    <Title
      className={styles.textCenter}
      level={3}
    >
      Email sent
    </Title>
    <p className={styles.textCenter}>
      <MailOutlined className={styles.icon} />
    </p>
    <p className={styles.textCenter}>
      We have sent you instructions on the next steps. Check your email.
    </p>

    <div className={styles.textCenter}>
      Have an account? <Link to={PATH_SIGN_IN}>Sign In</Link>
    </div>
  </div>
);

export default SignIn;
