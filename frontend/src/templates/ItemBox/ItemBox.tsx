import { CSSProperties, FC, HTMLAttributes, ReactNode } from 'react';
import styles from './ItemBox.module.css';

type Props = {
  children: ReactNode;
  width?: CSSProperties['width'];
  height?: CSSProperties['height'];
} & HTMLAttributes<HTMLDivElement>;

const ItemBox: FC<Props> = ({ onClick, width, height, children, ...props }) => {
  const { style, ...divProps } = props;
  return (
    <div
      className={styles.box}
      onClick={onClick}
      style={{ ...style, width, height }}
      {...divProps}
    >
      {children}
    </div>
  );
};

export default ItemBox;
