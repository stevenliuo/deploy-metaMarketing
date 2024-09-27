type Spreadsheet = {
  id: number;
  name: string;
  position: number;
};
type AttachedFile = {
  id: number;
  name: string;
  project: number;
  created_at: string;
  updated_at: string;
  spreadsheets: Spreadsheet[];
};
