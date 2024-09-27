import { Button, Result } from 'antd';
import { useAuth } from 'src/contexts/Auth';

const NotFound = () => {
  const { isAuthenticated } = useAuth();
  return (
    <div>
      <Result
        status="404"
        title="404"
        subTitle="Sorry, the page you visited does not exist."
        extra={
          <Button
            type="primary"
            href={isAuthenticated ? '/dashboard' : '/'}
          >
            Back Home
          </Button>
        }
      />
    </div>
  );
};

export default NotFound;
