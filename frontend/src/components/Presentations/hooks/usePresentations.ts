import { useCallback, useEffect, useMemo, useState } from 'react';
import {
  deletePresentations,
  getPresentations,
} from 'src/clientApi/presentation';
import { Presentation } from 'src/types/presentation';

type UsePresentations = {
  loading: boolean;
  presentations: Presentation[];
  filterPresentations: Presentation[];
  sortFiled: keyof Presentation;
  sortDirection: 'asc' | 'desc';
  setKeyword: (keyword: string) => void;
  setSortFiled: (sortFiled: keyof Presentation) => void;
  setSortDirection: (sortDirection: 'asc' | 'desc') => void;
  deletePresentation: (id: number) => Promise<void>;
};

const usePresentations = (): UsePresentations => {
  const [presentations, setPresentations] = useState<Presentation[]>([]);
  const [keyword, setKeyword] = useState<string>('');
  const [sortFiled, setSortFiled] = useState<keyof Presentation>('created_at');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc');
  const [loading, setLoading] = useState(false);
  const filterPresentations = useMemo(() => {
    let filterPresentations = [...presentations];

    if (keyword) {
      filterPresentations = filterPresentations.filter((presentation) =>
        presentation.title.toLowerCase().includes(keyword.toLowerCase())
      );
    }

    switch (sortFiled) {
      case 'created_at':
        filterPresentations = filterPresentations.sort((a, b) => {
          if (sortDirection === 'asc') {
            return (
              new Date(a.created_at).getTime() -
              new Date(b.created_at).getTime()
            );
          }
          return (
            new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
          );
        });
        break;
      case 'updated_at':
        filterPresentations = filterPresentations.sort((a, b) => {
          if (sortDirection === 'asc') {
            return (
              new Date(a.updated_at).getTime() -
              new Date(b.updated_at).getTime()
            );
          }
          return (
            new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime()
          );
        });
        break;
      default:
        break;
    }

    return filterPresentations;
  }, [presentations, keyword, sortDirection, sortFiled]);
  const deletePresentation = useCallback(async (id: number) => {
    try {
      await deletePresentations(id);
      setPresentations((prev) =>
        prev.filter((presentation) => presentation.id !== id)
      );
    } catch (error) {
      console.error(error);
    }
  }, []);

  useEffect(() => {
    const getData = async () => {
      try {
        setLoading(true);
        const presentations = await getPresentations();
        setPresentations(presentations);
      } finally {
        setLoading(false);
      }
    };
    getData();
  }, []);

  return {
    loading,
    filterPresentations,
    presentations,
    sortDirection,
    sortFiled,
    setKeyword,
    setSortFiled,
    setSortDirection,
    deletePresentation,
  };
};
export default usePresentations;
