import { notification } from 'antd';
import { AUTH_TOKEN, REFRESH_TOKEN } from 'src/helpers/constants';
import { PATH_SIGN_IN } from 'src/pages';

export const getErrorMessage = (error: any): string[] => {
  const errorObject = error?.response?.data || {};
  const errorMessages = Object.values(errorObject) as string[];
  return errorMessages.length === 0 ? ['Something went wrong'] : errorMessages;
};

export const handleErrors = (error: any) => {
  const errorMessages = getErrorMessage(error);
  errorMessages.forEach((message) => {
    notification.error({
      message,
    });
  });
};

export const logoutForce = () => {
  localStorage.removeItem(AUTH_TOKEN);
  localStorage.removeItem(REFRESH_TOKEN);
  window.location.href = PATH_SIGN_IN;
};
