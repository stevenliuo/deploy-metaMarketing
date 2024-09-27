export type Slide = {
  id: number;
  position: number;
  perform_analysis: boolean;
  slide_option: number;
  specific_title: string;
  specific_instructions: string;
  input_spreadsheet: number;
  workbook: number;
  project: number;
  created_at: string;
  updated_at: string;
};

export type CreateSlideFormValue = Omit<
  Slide,
  'id' | 'created_at' | 'updated_at' | 'position'
>;

export type SlideFormValue = Omit<
  Slide,
  'id' | 'created_at' | 'updated_at' | 'position' | 'project'
>;

export type Presentation = {
  id: number;
  name: string;
  title: string;
  description: string;
  subtitle: string;
  footer: string;
  template_name: string;
  workbook: [];
  slides: Slide[];
  created_at: string;
  updated_at: string;
};
