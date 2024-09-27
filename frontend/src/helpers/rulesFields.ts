import { Rule } from 'antd/es/form';
export const passwordRegexp =
  // eslint-disable-next-line no-useless-escape
  /^(?=.*[0-9])(?=.*[!@#£$%^&*~`\(\)_\-+={}\[\]'"<>\\|/:;?,.])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$£%^&*~`\(\)_\-+={}\[\]'"<>\\|/:;?,.]{8,30}$/g;
export const passwordMessage =
  'Password must contain 8 to 30 characters, one uppercase letter, one number, one extra-symbol.';
export const confirmPasswordMessage = 'Please confirm this password';
export const confirmPasswordNoMatchMessage =
  'The passwords you entered do not match.';

export const emailRules: Rule[] = [
  {
    message: 'The input is not valid E-mail!',
    transform: (val: string) => val.trim(),
    type: 'email',
    whitespace: true,
  },
  {
    max: 128,
    message: 'Limited to 128 characters!',
  },
];

export const requiredEmailRules: Rule[] = [
  ...emailRules,
  {
    message: 'Email address is required.',
    required: true,
  },
];

export const firstNameRules = [
  {
    message: 'First name is required.',
    required: true,
    whitespace: true,
  },
  {
    max: 200,
    message: 'Limited to 200 characters!',
  },
];

export const lastNameRules = [
  {
    message: 'Last name is required.',
    required: true,
    whitespace: true,
  },
  {
    max: 200,
    message: 'Limited to 200 characters!',
  },
];

export const passwordOnlyRequiredRules: Rule[] = [
  {
    message: 'Your password is required.',
    required: true,
  },
];

export const passwordRules: Rule[] = [
  ...passwordOnlyRequiredRules,
  {
    message: passwordMessage,
    pattern: passwordRegexp,
  },
];

export const confirmPasswordRules: Rule[] = [
  {
    message: confirmPasswordMessage,
    required: true,
  },
  ({ getFieldValue }) => ({
    validator(_, value) {
      if (value && value === getFieldValue('password')) {
        return Promise.resolve();
      }
      return Promise.reject(new Error(confirmPasswordNoMatchMessage));
    },
  }),
];

export const titleRules = [
  {
    message: 'Title is required.',
    required: true,
    whitespace: true,
  },
  {
    max: 200,
    message: 'Limited to 200 characters!',
  },
];

export const promoteRules = [
  {
    message: 'Instructions is required.',
    required: true,
    whitespace: true,
  },
];
