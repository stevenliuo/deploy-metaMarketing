import { FC, ReactNode } from 'react';
import styles from './Section.module.css';

type Props = {
  title: string;
  children: ReactNode;
  tooltip?: string;
};

const Section: FC<Props> = ({ title, children }) => {
  return (
    <section>
      <div className={styles.title}>{title}</div>
      <div className={styles.content}>{children}</div>
    </section>
  );
};

export default Section;
