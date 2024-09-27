import {
  CloudDownloadOutlined,
  ExperimentOutlined,
  EyeOutlined,
  FilePptOutlined,
  LogoutOutlined,
} from '@ant-design/icons';
import { Flex, Tooltip } from 'antd';
import { Link } from 'react-router-dom';
import { PATH_PRESENTATIONS } from 'src/pages';
import styles from './Toolbar.module.css';
import { FC } from 'react';
import classNames from 'classnames';
import { downloadPresentation } from 'src/clientApi/presentation';

type Props = {
  hasFullData: boolean;
  hasGenerated: boolean;
  isGenerating: boolean;
  presentationId: number;
  title: string;
  typeContent: 'presentation' | 'preview';
  generatePresentation(): Promise<void>;
  setTypeContent(type: 'presentation' | 'preview'): void;
};

const Toolbar: FC<Props> = ({
  hasFullData,
  hasGenerated,
  isGenerating,
  typeContent,
  presentationId,
  title,
  generatePresentation,
  setTypeContent,
}) => {
  return (
    <div className={styles.toolbar}>
      <Flex
        vertical
        gap={24}
      >
        <Tooltip
          title="Go to Presentations list"
          placement="right"
        >
          <Link
            to={PATH_PRESENTATIONS}
            style={{ color: '#fff' }}
          >
            <LogoutOutlined
              rotate={180}
              className={classNames(styles.icon)}
            />
          </Link>
        </Tooltip>

        <Tooltip
          title={
            hasFullData
              ? 'Generate'
              : 'To create a presentation, you need a title, a template, and at least one slide'
          }
          placement="right"
        >
          <ExperimentOutlined
            onClick={
              hasFullData && !isGenerating ? generatePresentation : undefined
            }
            className={classNames(styles.icon, {
              [styles.iconDisabled]: !hasFullData || isGenerating,
            })}
          />
        </Tooltip>
        {typeContent === 'presentation' && (
          <Tooltip
            title={
              hasGenerated
                ? 'Preview'
                : 'Generate the presentation first to preview it'
            }
            placement="right"
          >
            <EyeOutlined
              onClick={
                !hasGenerated ? undefined : () => setTypeContent('preview')
              }
              className={classNames(styles.icon, {
                [styles.iconDisabled]: !hasGenerated,
              })}
            />
          </Tooltip>
        )}
        {typeContent === 'preview' && (
          <Tooltip
            title="Manage the presentation"
            placement="right"
          >
            <FilePptOutlined
              onClick={() => setTypeContent('presentation')}
              className={styles.icon}
            />
          </Tooltip>
        )}
        <Tooltip
          title={
            hasGenerated
              ? 'Download Presentation'
              : 'Generate the presentation first to download it'
          }
          placement="right"
        >
          <CloudDownloadOutlined
            onClick={
              !hasGenerated
                ? undefined
                : () => downloadPresentation(presentationId, title)
            }
            className={classNames(styles.icon, {
              [styles.iconDisabled]: !hasGenerated,
            })}
          />
        </Tooltip>
      </Flex>
    </div>
  );
};

export default Toolbar;
