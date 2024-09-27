import moment from 'moment';
export const FORMATE_DATE = 'MM.DD.YYYY';

export const convertUtcToLocalDate = (date: any) =>
  moment(date).add(moment().utcOffset(), 'minutes');
export const getTimeWithTimeZone = (date: any) =>
  date ? moment(`${date}`) : undefined;

export const getFormattedDate = (date: any) => {
  if (moment.isMoment(date)) {
    return date.format(FORMATE_DATE);
  }
  return getTimeWithTimeZone(date)?.format(FORMATE_DATE);
};
