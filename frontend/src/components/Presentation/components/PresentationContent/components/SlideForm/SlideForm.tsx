import { Flex, Form, Input, Select, Radio } from 'antd';
import { FC, useCallback, useMemo } from 'react';
import { promoteRules, titleRules } from 'src/helpers/rulesFields';
import styles from './SlideForm.module.css';
import { Slide, SlideFormValue } from 'src/types/presentation';
import { useForm, useWatch } from 'antd/es/form/Form';

type Props = {
  formId: string;
  defaultValues?: Slide;
  onSubmit: (values: SlideFormValue) => void;
  disabled?: boolean;
  workbooks: AttachedFile[];
};

const SlideForm: FC<Props> = ({
  formId,
  onSubmit,
  disabled,
  defaultValues,
  workbooks,
}) => {
  const [form] = useForm<Slide>();
  const workbookId = useWatch('workbook', form);
  const options = [1,2,3,4,5].map((value) => {
    return {
      label: <div className={styles.slideoption}>
              <img className={styles.image} src={`/src/assets/images/SlideOptions/SlideOption${value}.png`} alt='slide option' />
            </div>,
      value: value
    }
  })
  
  const spreadsheets = useMemo(() => {
    return (
      workbooks.find((workbook) => workbook.id === workbookId)?.spreadsheets ||
      []
    );
  }, [workbooks, workbookId]);
  const handlerWorkbookChange = useCallback(() => {
    form.setFieldsValue({ input_spreadsheet: undefined });
  }, []);
  return (
    <Form<Slide>
      form={form}
      layout="vertical"
      id={formId}
      onFinish={onSubmit}
      initialValues={defaultValues}
    >
      <Form.Item
        label="Title"
        name="specific_title"
        rules={titleRules}
      >
        <Input disabled={disabled} />
      </Form.Item>
      <Flex gap={8}>
        <Form.Item
          className={styles.select}
          name="workbook"
          label="Workbook"
          rules={[
            {
              message: 'Workbook is required.',
              required: true,
            },
          ]}
        >
          <Select
            onChange={handlerWorkbookChange}
            disabled={disabled}
          >
            {workbooks.map((workbook) => (
              <Select.Option
                key={workbook.id}
                value={workbook.id}
              >
                {workbook.name}
              </Select.Option>
            ))}
          </Select>
        </Form.Item>
        <Form.Item
          className={styles.select}
          name="input_spreadsheet"
          label="Spreadsheet"
          rules={[
            {
              message: 'Spreadsheet is required.',
              required: true,
            },
          ]}
        >
          <Select disabled={disabled || !spreadsheets.length}>
            {spreadsheets.map((spreadsheet) => (
              <Select.Option
                key={spreadsheet.id}
                value={spreadsheet.id}
              >
                {spreadsheet.name}
              </Select.Option>
            ))}
          </Select>
        </Form.Item>
      </Flex>
      <Form.Item
        name="slide_option"
        label="Select Slide Option:"
        initialValue={1}
      >
        <Radio.Group options={options} />
      </Form.Item>
      <Form.Item
        name="specific_instructions"
        label="Instructions"
        rules={promoteRules}
      >
        <Input.TextArea
          disabled={disabled}
          autoSize={{ minRows: 4, maxRows: 8 }}
        />
      </Form.Item>
    </Form>
  );
};

export default SlideForm;
