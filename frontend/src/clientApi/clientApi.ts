import axios from 'axios';
import { AUTH_TOKEN, REFRESH_TOKEN } from 'src/helpers/constants';
import { getLocalStorage } from 'src/helpers/storage';
import { logoutForce } from './helpers';
import { SignInResponse } from './authApi';

const clientApi = axios.create({
  headers: {
    'Content-Type': 'application/json',
  },
});

clientApi.interceptors.request.use(
  (request) => {
    const accessToken = getLocalStorage<string>(AUTH_TOKEN);
    if (accessToken) {
      request.headers['Authorization'] = `Bearer ${accessToken}`;
    }
    return request;
  },
  (error) => {
    return Promise.reject(error);
  }
);

clientApi.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (
      error.response.status === 401 &&
      !originalRequest._retry &&
      originalRequest.url !== '/api/account/token/refresh'
    ) {
      originalRequest._retry = true;
      try {
        const refreshToken = getLocalStorage<string>(REFRESH_TOKEN);
        const response = await clientApi.post<SignInResponse>(
          '/api/account/token/refresh',
          {
            refresh: refreshToken,
          }
        );
        const { access } = response.data;

        localStorage.setItem(AUTH_TOKEN, JSON.stringify(access));
        originalRequest.headers['Authorization'] = `Bearer ${access}`;
        clientApi.defaults.headers.common['Authorization'] = `Bearer ${access}`;
        return clientApi(originalRequest);
      } catch (refreshError) {
        logoutForce();
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export default clientApi;
