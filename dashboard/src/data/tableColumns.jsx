import React from 'react';
import { Button, Dropdown } from 'antd';
import { MoreOutlined } from '@ant-design/icons';

// Function to open dynamic drawer
const openDynamicDrawer = (record, type) => {
  // This is a placeholder - the actual implementation will be in the component
  console.log(`Open ${type} drawer for record:`, record);
  
  // We'll dispatch a custom event that the component can listen for
  const event = new CustomEvent('openDynamicDrawer', { 
    detail: { record, type } 
  });
  window.dispatchEvent(event);
};

// Function to open dynamic modal
const openDynamicModal = (record, type) => {
  // This is a placeholder - the actual implementation will be in the component
  console.log(`Open ${type} modal for record:`, record);
  
  // We'll dispatch a custom event that the component can listen for
  const event = new CustomEvent('openDynamicModal', { 
    detail: { record, type } 
  });
  window.dispatchEvent(event);
};

// Action menu items for table rows
const getActionItems = (record) => {
  return [
    {
      key: 'view',
      label: 'View Details',
      onClick: () => openDynamicDrawer(record, 'view'),
    },
    {
      key: 'edit',
      label: 'Edit',
      onClick: () => openDynamicModal(record, 'edit'),
    },
    {
      key: 'delete',
      label: 'Delete',
      danger: true,
      onClick: () => openDynamicModal(record, 'delete'),
    },
  ];
};

// Table Columns Definition
const getTableColumns = () => [
  { title: 'ID', dataIndex: 'id', key: 'id', width: 100, fixed: 'left' },
  { title: 'Name', dataIndex: 'name', key: 'name', width: 150 },
  { title: 'Address', dataIndex: 'address', key: 'address', width: 250 },
  { title: 'Goal', dataIndex: 'goal', key: 'goal', ellipsis: true, width: 300 },
  { title: 'Category', dataIndex: 'category', key: 'category', width: 120 },
  { title: 'Log Date', dataIndex: 'logDate', key: 'logDate', width: 180 },
  {
    title: '',
    key: 'actions',
    width: 60,
    align: 'center',
    fixed: 'right',
    render: (_, record) => (
      <Dropdown menu={{ items: getActionItems(record) }} trigger={['click']}>
        <Button type="text" icon={<MoreOutlined />}  />
      </Dropdown>
    ),
  },
];

export default getTableColumns;
