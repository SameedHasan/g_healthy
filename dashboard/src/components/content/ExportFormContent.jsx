import React, { useState } from 'react';
import { Select, Input, Typography, Space } from 'antd';

const { Title, Text } = Typography;
const { Option } = Select;

const ExportFormContent = ({ onChange }) => {
  const [form, setForm] = useState({
    format: 'csv',
    dateRange: {
      start: '',
      end: ''
    },
    fields: ['title', 'category', 'author', 'status']
  });

  const handleChange = (name, value) => {
    const updatedForm = { ...form, [name]: value };
    setForm(updatedForm);
    if (onChange) {
      onChange(updatedForm);
    }
  };

  const handleDateRangeChange = (type, value) => {
    const updatedDateRange = { ...form.dateRange, [type]: value };
    handleChange('dateRange', updatedDateRange);
  };

  return (
    <div>
      <Title level={5}>Export Options</Title>
      <div style={{ marginBottom: 16 }}>
        <Text strong>Format</Text>
        <Select
          value={form.format}
          onChange={(value) => handleChange('format', value)}
          style={{ width: '100%', marginTop: 8 }}
        >
          <Option value="csv">CSV</Option>
          <Option value="excel">Excel</Option>
          <Option value="pdf">PDF</Option>
        </Select>
      </div>
      
      <div style={{ marginBottom: 16 }}>
        <Text strong>Date Range</Text>
        <Input.Group compact style={{ marginTop: 8 }}>
          <Input 
            style={{ width: '50%' }} 
            placeholder="Start date" 
            value={form.dateRange.start}
            onChange={(e) => handleDateRangeChange('start', e.target.value)}
          />
          <Input 
            style={{ width: '50%' }} 
            placeholder="End date" 
            value={form.dateRange.end}
            onChange={(e) => handleDateRangeChange('end', e.target.value)}
          />
        </Input.Group>
      </div>
      
      <div style={{ marginBottom: 16 }}>
        <Text strong>Include Fields</Text>
        <Select
          mode="multiple"
          placeholder="Select fields"
          value={form.fields}
          onChange={(value) => handleChange('fields', value)}
          style={{ width: '100%', marginTop: 8 }}
        >
          <Option value="title">Title</Option>
          <Option value="category">Category</Option>
          <Option value="tags">Tags</Option>
          <Option value="author">Author</Option>
          <Option value="status">Status</Option>
          <Option value="datePublished">Date Published</Option>
        </Select>
      </div>
    </div>
  );
};

export default ExportFormContent;
