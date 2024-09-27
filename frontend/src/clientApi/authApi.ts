import { notification } from 'antd';
import clientApi from './clientApi';
import { handleErrors } from './helpers';

export type SignUpData = {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  password2: string;
};
export const signUpAccount = async (data: SignUpData) => {
  try {
    await clientApi.post('/api/account/registration', data);
  } catch (error) {
    //@ts-ignore
    const errorObject = error?.response?.data;
    if (errorObject) {
      Object.keys(errorObject).forEach((key) => {
        notification.error({
          message: `${key}: ${errorObject[key]}`,
        });
      });
    }
  }
};

export type SignInData = {
  email: string;
  password: string;
};

export type SignInResponse = { refresh: string; access: string };

export const signInAccount = async (
  data: SignInData
): Promise<SignInResponse> => {
  try {
    const res = await clientApi.post<SignInResponse>(
      '/api/account/token',
      data
    );
    return res.data;
  } catch (error) {
    handleErrors(error);
    return Promise.reject(error);
  }
};

export const emailConfirm = async (
  uid: string | null,
  token: string | null
): Promise<SignInResponse> => {
  try {
    if (!uid || !token) {
      throw new Error('uid and token are required');
    }
    const res = await clientApi.post<SignInResponse>(
      `/api/account/email/confirm/${uid}`,
      { token }
    );
    return res.data;
  } catch (error) {
    return Promise.reject(error);
  }
};

export const forgotPassword = async (email: string) => {
  try {
    await clientApi.post('/api/account/password/reset', { email });
  } catch (error) {
    handleErrors(error);
    return Promise.reject(error);
  }
};

export type ResetPasswordData = {
  uid: string;
  token: string;
  password: string;
  password2: string;
};

export const resetPassword = async (data: ResetPasswordData) => {
  try {
    const res = await clientApi.post(
      `/api/account/password/reset/confirm/${data.uid}`,
      data
    );
    return res.data;
  } catch (error) {
    handleErrors(error);
    return Promise.reject(error);
  }
};
