import { useCallback, useEffect, useState } from 'react';
import { getPresentation } from 'src/clientApi/presentation';
import { Presentation, Slide } from 'src/types/presentation';

type UsePresentation = {
  presentation?: Presentation;
  loading: boolean;
  setPresentation: (presentation: Presentation) => void;
  setNewSlide: (newSlide: Slide) => void;
  deleteSlide: (id: number) => void;
  updateSlide: (updateSlide: Slide) => void;
};

const usePresentation = (id: number): UsePresentation => {
  const [presentation, setPresentation] = useState<Presentation>();
  const [loading, setLoading] = useState<boolean>(true);
  const setNewSlide = useCallback(
    (newSlide: Slide) => {
      if (!presentation) return;
      setPresentation({
        ...presentation,
        slides: [...presentation.slides, newSlide],
      });
    },
    [setPresentation, presentation]
  );
  const deleteSlide = useCallback(
    (id: number) => {
      if (!presentation) return;
      setPresentation({
        ...presentation,
        slides: presentation.slides.filter((slide) => slide.id !== id),
      });
    },
    [setPresentation, presentation]
  );
  const updateSlide = useCallback(
    (updateSlide: Slide) => {
      if (!presentation) return;
      setPresentation({
        ...presentation,
        slides: presentation.slides.map((slide) => {
          if (slide.id === updateSlide.id) {
            return updateSlide;
          }
          return slide;
        }),
      });
    },
    [setPresentation, presentation]
  );

  useEffect(() => {
    const getData = async () => {
      try {
        setLoading(true);
        const presentation = await getPresentation(id);
        setPresentation(presentation);
      } finally {
        setLoading(false);
      }
    };
    getData();
  }, [id]);

  return {
    presentation,
    loading,
    setPresentation,
    setNewSlide,
    deleteSlide,
    updateSlide,
  };
};

export default usePresentation;
