import { FC } from 'react';
import { Flex, Skeleton } from 'antd';
import { CreatePresentation, Presentation, Toolbar } from './components';
import { usePresentations } from './hooks';
import { generatePath, useNavigate } from 'react-router-dom';
import { PATH_PRESENTATION } from 'src/pages';
import ItemBox from 'src/templates/ItemBox';
import { getFormattedDate } from 'src/helpers/date';

const Presentations: FC = () => {
  const {
    loading,
    filterPresentations,
    setKeyword,
    sortFiled,
    sortDirection,
    setSortFiled,
    setSortDirection,
    deletePresentation,
  } = usePresentations();
  const navigate = useNavigate();
  return (
    <Flex
      gap="large"
      vertical
    >
      <Toolbar
        sortFiled={sortFiled}
        sortDirection={sortDirection}
        setKeyword={setKeyword}
        setSortFiled={setSortFiled}
        setSortDirection={setSortDirection}
      />
      <Flex
        gap="large"
        wrap
      >
        <CreatePresentation disabled={loading} />
        {!loading &&
          filterPresentations.map((presentation) => (
            <Presentation
              key={presentation.id}
              title={presentation.title}
              id={presentation.id}
              createdAt={getFormattedDate(presentation.created_at) || ''}
              updatedAt={getFormattedDate(presentation.updated_at) || ''}
              onDelete={deletePresentation}
              onClick={() =>
                navigate(
                  generatePath(PATH_PRESENTATION, { id: `${presentation.id}` })
                )
              }
            />
          ))}
        {loading && (
          <>
            <ItemBox>
              <Skeleton active />
            </ItemBox>
            <ItemBox>
              <Skeleton active />
            </ItemBox>
            <ItemBox>
              <Skeleton active />
            </ItemBox>
          </>
        )}
      </Flex>
    </Flex>
  );
};

export default Presentations;
