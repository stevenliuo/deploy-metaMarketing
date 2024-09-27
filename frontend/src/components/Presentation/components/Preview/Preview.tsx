import { FC } from 'react';
import { Screenshot } from 'src/types/presantationsScreenshots';
import styles from './Preview.module.css';
import Title from 'antd/es/typography/Title';
import { Flex } from 'antd';

type Props = {
  screenshots: Screenshot[];
};

const Preview: FC<Props> = ({ screenshots }) => {
  return (
    <div className={styles.content}>
      <Title level={3}>Preview Slide:</Title>
      <Flex
        wrap
        gap={24}
      >
        {screenshots.map((screenshot, i) => (
          <div
            key={i}
            style={{
              backgroundImage: `url(${screenshot.screenshot})`,
            }}
            className={styles.slide}
          />
        ))}
      </Flex>
    </div>
  );
};

export default Preview;
