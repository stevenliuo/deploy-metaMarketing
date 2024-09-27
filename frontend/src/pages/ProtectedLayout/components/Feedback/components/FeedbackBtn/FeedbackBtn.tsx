import {
  CSSProperties,
  FC,
  useCallback,
  useEffect,
  useRef,
  useState,
} from 'react';
import { getLocalStorage } from 'src/helpers/storage';
import { MessageOutlined } from '@ant-design/icons';
import { useDrag, useDrop } from 'react-dnd';

import styles from './FeedbackBtn.module.css';
import AreaDrop from './AreaDrop';

type Position = {
  left: CSSProperties['left'];
  top: CSSProperties['left'];
};

type Props = {
  onClick: () => void;
  isOpen?: boolean;
};

const storeKey = 'feedbackPosition';
const getInitialPosition = (storeKey: string) => {
  const position = getLocalStorage<Position>(storeKey);

  if (!position || position.left === undefined || position.top === undefined) {
    return { left: 'calc(100vw - 90px)', top: 'calc(100vh - 90px)' };
  }

  return position;
};

const FeedbackBtn: FC<Props> = ({ onClick, isOpen }) => {
  const [positionBtn, setPositionBtn] = useState<Position>(
    getInitialPosition(storeKey)
  );
  const refBtn = useRef<HTMLDivElement>(null);
  const [isGetNewPosition, setIsGetNewPosition] = useState(false);
  const [, drop] = useDrop(() => ({
    accept: 'btn',
  }));
  const [{ isDragging }, drag] = useDrag(() => ({
    collect: (monitor) => ({
      isDragging: !!monitor.isDragging(),
    }),
    end: () => {
      setIsGetNewPosition(true);
    },
    type: 'btn',
  }));

  const handleSetPosition = useCallback(
    (position: Position) => {
      localStorage.setItem(storeKey, JSON.stringify(position));
      setPositionBtn(position);
    },
    [setPositionBtn]
  );

  useEffect(() => {
    drag(drop(refBtn));
  }, [drag, drop, refBtn]);

  useEffect(() => {
    if (!isGetNewPosition) {
      return;
    }

    const handleMove = (e: MouseEvent) => {
      if (isGetNewPosition) {
        handleSetPosition({
          left: e.clientX - 45 - 11,
          top: e.clientY - 45 - 11,
        });
        setIsGetNewPosition(false);
      }
    };
    document.addEventListener('mousemove', handleMove);

    return () => {
      document.removeEventListener('mousemove', handleMove);
    };
  }, [isGetNewPosition, handleSetPosition]);

  return (
    <>
      <div
        ref={refBtn}
        className={styles.btn}
        onClick={onClick}
        style={{
          ...(isOpen ? { zIndex: 'auto' } : {}),
          opacity: isDragging ? 0 : 1,
          ...positionBtn,
        }}
      >
        <MessageOutlined className={styles.btnIcon} />
      </div>
      <AreaDrop show={isDragging} />
    </>
  );
};

export default FeedbackBtn;
