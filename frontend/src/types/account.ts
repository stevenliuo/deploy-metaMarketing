import { RcFile } from 'antd/es/upload';

export type AccountInfo = {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
  last_login: string;
  created_at: string;
  settings: {
    general_instructions: string | null;
    terminology: string | null;
    template_name: string | null;
    project_instructions: string | null;
  };
};

export type UpdateAccountInfo = {
  first_name: string;
  last_name: string;
  settings: {
    general_instructions: string | null;
    terminology: string | null;
    template_name?: string | null;
    template_content?: RcFile | null;
    project_instructions?: string | null;
  };
};
