import { FC, useId, useMemo, useCallback, useState, useEffect } from 'react';
import styles from './Settings.module.css';
import { Button, Flex, Form, Input, Space, Upload, notification } from 'antd';
import Title from 'antd/es/typography/Title';
import { Section } from 'src/templates';
import { firstNameRules, lastNameRules } from 'src/helpers/rulesFields';
import { useAuth } from 'src/contexts/Auth';
import {
  CloseCircleOutlined,
  FilePptOutlined,
  UploadOutlined,
} from '@ant-design/icons';
import { updateAccountInfo } from 'src/clientApi/settingApi';
import { useForm } from 'antd/es/form/Form';
import { RcFile } from 'antd/es/upload';
import { UpdateAccountInfo } from 'src/types/account';

const Settings: FC = () => {
  const formId = useId();
  const [form] = useForm();
  const { accountInfo, setAccountInfo } = useAuth();
  const [loading, setLoading] = useState(false);
  const [templateName, setTemplateName] = useState<string>(
    accountInfo?.settings.template_name || ''
  );
  const [templateFile, setTemplateFile] = useState<RcFile | null>(null);
  const initValues = useMemo(
    () => ({
      first_name: accountInfo?.first_name || '',
      last_name: accountInfo?.last_name || '',
      general_instructions: accountInfo?.settings.general_instructions || '',
      terminology: accountInfo?.settings.terminology || '',
      project_instructions: accountInfo?.settings.project_instructions || '',
    }),
    [accountInfo]
  );
  const handlerUpload = useCallback(
    (file: RcFile) => {
      setTemplateFile(file);
      return false;
    },
    [setTemplateFile]
  );
  const handlerDelete = useCallback(() => {
    setTemplateFile(null);
    setTemplateName('');
  }, [setTemplateFile, setTemplateName]);
  const handlerSubmit = useCallback(
    async (values: any) => {
      if (!accountInfo) return;
      try {
        setLoading(true);
        const settings: UpdateAccountInfo['settings'] = {
          general_instructions: values.general_instructions,
          terminology: values.terminology,
          project_instructions: values.project_instructions,
        };
        if (templateFile) {
          settings.template_content = templateFile;
        } else if (templateName) {
          settings.template_name = templateName;
        } else {
          settings.template_name = null;
        }

        const account = await updateAccountInfo({
          first_name: values.first_name,
          last_name: values.last_name,
          settings,
        });
        setAccountInfo(account);
        notification.success({
          message: 'Settings updated successfully',
        });
      } finally {
        setLoading(false);
      }
    },
    [setLoading, accountInfo, templateFile]
  );

  useEffect(() => {
    setTemplateName(templateFile?.name || '');
  }, [setTemplateName, templateFile]);

  useEffect(() => {
    if (!accountInfo) return;
    form.setFieldsValue(initValues);
    setTemplateName(accountInfo.settings.template_name || '');
  }, [accountInfo, initValues]);
  return (
    <Flex
      justify="center"
      align="center"
    >
      <div className={styles.box}>
        <Flex
          justify="space-between"
          align="center"
          className={styles.header}
        >
          <Title level={3}>Settings</Title>
          <Button
            type="primary"
            htmlType="submit"
            form={formId}
          >
            Save
          </Button>
        </Flex>
        <div className={styles.content}>
          <Form
            form={form}
            id={formId}
            layout="vertical"
            initialValues={initValues}
            onFinish={handlerSubmit}
          >
            <Section title="Personal Info">
              <Form.Item
                label="First Name"
                name="first_name"
                rules={firstNameRules}
              >
                <Input disabled={loading} />
              </Form.Item>
              <Form.Item
                label="Last Name"
                name="last_name"
                rules={lastNameRules}
              >
                <Input disabled={loading} />
              </Form.Item>
            </Section>
            <Section title="General settings">
              <Form.Item
                label="General instructions"
                name="general_instructions"
              >
                <Input.TextArea
                  disabled={loading}
                  autoSize={{ minRows: 2, maxRows: 6 }}
                />
              </Form.Item>
              <Form.Item
                label="Terminology"
                name="terminology"
              >
                <Input.TextArea
                  disabled={loading}
                  autoSize={{ minRows: 2, maxRows: 6 }}
                />
              </Form.Item>
            </Section>
            <Section title="Presentation setting">
              <Form.Item label="Template presentation">
                <Flex
                  align="center"
                  justify="space-between"
                >
                  <Space
                    size="small"
                    align="center"
                  >
                    <FilePptOutlined className={styles.iconPPT} />
                    {templateName || 'No file'}{' '}
                    {templateName && (
                      <CloseCircleOutlined
                        className={styles.iconDelete}
                        onClick={handlerDelete}
                      />
                    )}
                  </Space>
                  <Upload
                    showUploadList={false}
                    accept="application/vnd.ms-powerpoint, application/vnd.openxmlformats-officedocument.presentationml.presentation"
                    beforeUpload={handlerUpload}
                  >
                    <Button
                      disabled={loading}
                      icon={<UploadOutlined />}
                    >
                      Click to Upload
                    </Button>
                  </Upload>
                </Flex>
              </Form.Item>
              <Form.Item
                label="Default Footer"
                name="project_instructions"
              >
                <Input.TextArea
                  disabled={loading}
                  autoSize={{ minRows: 2, maxRows: 6 }}
                />
              </Form.Item>
            </Section>
          </Form>
        </div>
      </div>
    </Flex>
  );
};

export default Settings;
