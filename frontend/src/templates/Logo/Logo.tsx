import { CSSProperties, FC, HTMLAttributes } from 'react';
import styles from './Logo.module.css';

type Props = {
  width?: CSSProperties['width'];
  height?: CSSProperties['height'];
} & HTMLAttributes<HTMLDivElement>;

const Logo: FC<Props> = ({ width = 50, height = 50, ...props }) => {
  const { style, ...divProps } = props;
  return (
    <div
      className={styles.logo}
      style={{ ...style, width, height }}
      {...divProps}
    />
  );
};

export default Logo;
