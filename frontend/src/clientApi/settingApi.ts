import { AccountInfo, UpdateAccountInfo } from 'src/types/account';
import clientApi from './clientApi';
import { handleErrors } from './helpers';
import { logoutForce } from './helpers';

export const getAccountInfo = async (): Promise<AccountInfo> => {
  try {
    const res = await clientApi.get('/api/account/info');
    return res.data;
  } catch (error) {
    handleErrors(error);
    logoutForce();
    return Promise.reject(error);
  }
};

export const updateAccountInfo = async (
  data: UpdateAccountInfo
): Promise<AccountInfo> => {
  try {
    const formData = new FormData();
    Object.entries(data).forEach(([key, value]) => {
      if (key === 'settings') {
        Object.entries(value).forEach(([k, v]) => {
          if (k === 'template_content' && v) {
            formData.append(`settings.template_content`, v);
          } else {
            formData.append(`settings.${k}`, (v || '').toString());
          }
        });
      } else {
        formData.append(key, (value || '').toString());
      }
    });
    const res = await clientApi.put('/api/account/info', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return res.data;
  } catch (error) {
    handleErrors(error);
    return Promise.reject(error);
  }
};
