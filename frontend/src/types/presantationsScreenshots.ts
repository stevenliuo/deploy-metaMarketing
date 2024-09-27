export type Screenshot = {
  screenshot: string;
  created_at: string;
  updated_at: string;
};
export type PresentationScreenshots = {
  id: number;
  title: string;
  screenshots: Screenshot[];
  created_at: string;
  updated_at: string;
};
