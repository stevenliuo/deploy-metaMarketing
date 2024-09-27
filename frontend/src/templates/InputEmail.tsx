import { ChangeEvent, FC, useEffect, useState } from 'react';
import { Input, InputProps } from 'antd';

type Value = string | undefined;
type Props = {
  className?: string;
  disabled?: boolean;
  onChange?: (value: Value) => void;
  placeholder?: string;
  value?: Value;
} & InputProps;

const removingSpaces = (value: Value) =>
  typeof value === 'string' ? value.replace(/\s/g, '') : value;

const InputEmail: FC<Props> = (props) => {
  const [val, setVal] = useState<string | undefined>();
  const { value, onChange, ...resProps } = props;
  const _onChange = (event: ChangeEvent<HTMLInputElement>) => {
    const newVal = removingSpaces(event.target.value);

    setVal(() => newVal);
    onChange && onChange(newVal);

    if (newVal !== event.target.value) {
      const element = event.target;
      const positon = element.selectionStart;

      setTimeout(() => {
        positon && element.setSelectionRange(positon - 1, positon - 1, 'none');
      });
    }
  };
  useEffect(() => {
    if (!val) {
      setVal(() => removingSpaces(value));
    }
  }, [value]);

  return (
    <Input
      value={val}
      onChange={_onChange}
      {...resProps}
    />
  );
};

export default InputEmail;
