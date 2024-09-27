import { FC } from 'react';
import { useDrop } from 'react-dnd';

import styles from './FeedbackBtn.module.css';

type Props = {
  show: boolean;
};
const AreaDrop: FC<Props> = ({ show }) => {
  const [, drop] = useDrop(() => ({
    accept: 'btn',
  }));
  return (
    <div
      ref={drop}
      className={styles.areaDrop}
      style={{
        display: show ? 'block' : 'none',
      }}
    />
  );
};

export default AreaDrop;
