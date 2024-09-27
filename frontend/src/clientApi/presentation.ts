import { Presentation } from 'src/types/presentation';
import clientApi from './clientApi';
import { getErrorMessage, handleErrors } from './helpers';
import { RcFile } from 'antd/es/upload';
import { notification } from 'antd';
import { PresentationScreenshots } from 'src/types/presantationsScreenshots';
import { saveAs } from 'file-saver';

export const getPresentations = async (): Promise<Presentation[]> => {
  try {
    const res = await clientApi.get('/api/ppt/projects/');
    return res.data;
  } catch (error) {
    handleErrors(error);
    return Promise.reject(error);
  }
};

export const deletePresentations = async (
  project_id: number
): Promise<boolean> => {
  try {
    await clientApi.delete(`/api/ppt/projects/${project_id}/delete/`);
    notification.success({
      message: 'Presentation was successfully deleted',
    });
    return true;
  } catch (error) {
    handleErrors(error);
    return Promise.reject(error);
  }
};

export const createPresentation = async (data: { title: string }) => {
  try {
    const res = await clientApi.post('api/ppt/projects/create/', data);
    return res.data;
  } catch (error) {
    handleErrors(error);
    return Promise.reject(error);
  }
};

export const getPresentation = async (id: number): Promise<Presentation> => {
  try {
    const res = await clientApi.get(`/api/ppt/projects/${id}`);
    return res.data;
  } catch (error) {
    handleErrors(error);
    return Promise.reject(error);
  }
};

export const updatePresentation = async (
  data: Presentation & { template_content?: RcFile }
): Promise<Presentation> => {
  try {
    const fromData = new FormData();
    Object.entries(data).forEach(([key, value]) => {
      if (key === 'slides' || key === 'workbook') {
        return;
      }
      if (key === 'template_content') {
        fromData.append(key, value as RcFile);
      } else {
        fromData.append(key, (value || '') as string);
      }
    });
    const res = await clientApi.put(`/api/ppt/projects/${data.id}/`, fromData, {
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

export const generatePresentationById = async (id: number) => {
  try {
    const res = await clientApi.post(`/api/ppt/projects/${id}/generate-ppt/`);
    return res.data;
  } catch (error) {
    const errorMessages = getErrorMessage(error);
    if (
      errorMessages.includes(
        'Screenshot is not ready for current project, try again later'
      ) ||
      errorMessages.includes('Preparing .xlsx files. This may take some time.')
    ) {
      notification.warning({
        message: 'Screenshot is not ready for current project, try again later',
      });
      return Promise.reject(error);
    }

    handleErrors(error);
    return Promise.reject(error);
  }
};

export const getPresentationScreenshots = async (
  id: number
): Promise<PresentationScreenshots> => {
  try {
    const res = await clientApi.get(`/api/ppt/projects/${id}/screenshots/`);
    return res.data;
  } catch (error) {
    return Promise.reject(error);
  }
};

export const downloadPresentation = async (id: number, title: string) => {
  try {
    const res = await clientApi.get(`/api/ppt/projects/${id}/download-ppt/`, {
      responseType: 'blob',
    });
    saveAs(res.data, title);
    return res.data;
  } catch (error) {
    handleErrors(error);
    return Promise.reject(error);
  }
};
