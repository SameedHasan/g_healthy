import { DatePicker, Input, Space } from 'antd';
import { CalendarIcon, CalendarArrowDownIcon } from '../../utils/icons';
const { RangePicker } = DatePicker;

const CustomRangePicker = () => {
  return (
    <div className='custom-range-picker'>

      <CalendarIcon />

      <RangePicker
        format="MMM D, YYYY"
        separator=" - "
        suffixIcon={<CalendarArrowDownIcon />}
        style={{ width: 220 }}
        defaultValue={[null, null]}
        placeholder={['Mar 31, 2025', 'Mar 31, 2025']}
      />
    </div>
  );
};

export default CustomRangePicker;
