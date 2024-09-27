import { RcFile } from 'antd/es/upload';
import clientApi from './clientApi';
import { handleErrors } from './helpers';
import { notification } from 'antd';

export const uploadFile = async (
  file: RcFile,
  id: number
): Promise<AttachedFile> => {
  try {
    const formData = new FormData();
    formData.append('content', file);
    formData.append('project', id.toString());

    const res = await clientApi.post(
      `/api/ppt/projects/${id}/input-workbooks/`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    return res.data;
  } catch (error) {
    handleErrors(error);
    return Promise.reject(error);
  }
};

export const getAttachedFilesByPresentationId = async (
  id: number
): Promise<AttachedFile[]> => {
  try {
    const res = await clientApi.get(`/api/ppt/projects/${id}/input-workbooks/`);
    return res.data;
  } catch (error) {
    handleErrors(error);
    return Promise.reject(error);
  }
};

export const updateAttachedFile = async (
  file: RcFile,
  id: number
): Promise<AttachedFile> => {
  try {
    const formData = new FormData();
    formData.append('content', file);
    formData.append('project', id.toString());
    const res = await clientApi.put(
      `/api/ppt/input-workbooks/${id}/`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    return res.data;
  } catch (error) {
    //@ts-ignore
    if (error?.response?.data?.error) {
      notification.error({
        //@ts-ignore
        message: error.response.data.error,
      });
    }
    return Promise.reject(error);
  }
};

export const deleteAttachedFile = async (id: number): Promise<boolean> => {
  try {
    await clientApi.delete(`/api/ppt/input-workbooks/${id}/`);
    return true;
  } catch (error) {
    handleErrors(error);
    return Promise.reject(error);
  }
};
