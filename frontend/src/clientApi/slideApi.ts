import { CreateSlideFormValue, Slide } from 'src/types/presentation';
import clientApi from './clientApi';
import { handleErrors } from './helpers';

export const createSlide = async (data: CreateSlideFormValue) => {
  try {
    const res = await clientApi.post('/api/ppt/slide-instructions/', data);
    return res.data;
  } catch (error) {
    handleErrors(error);
    return Promise.reject(error);
  }
};

export const updateSlide = async (data: Slide) => {
  try {
    const res = await clientApi.put(
      `/api/ppt/slide-instructions/${data.id}/`,
      data
    );
    return res.data;
  } catch (error) {
    handleErrors(error);
    return Promise.reject(error);
  }
};

export const deleteSlide = async (id: number) => {
  try {
    const res = await clientApi.delete(
      `/api/ppt/slide-instructions/${id}/delete/`
    );
    return res.data;
  } catch (error) {
    handleErrors(error);
    return Promise.reject(error);
  }
};
