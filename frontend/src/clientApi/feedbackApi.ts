import clientApi from './clientApi';
import { handleErrors } from './helpers';

export const sendFeedback = async (message: string): Promise<void> => {
  try {
    await clientApi.post('/api/feedback/', {
      message,
      url_on_page: window.location.href,
    });
  } catch (error) {
    handleErrors(error);
    return Promise.reject(error);
  }
};
