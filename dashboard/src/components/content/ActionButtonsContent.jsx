import React from 'react';
import { Button, Space } from 'antd';
import { EditOutlined, DeleteOutlined } from '@ant-design/icons';

const ActionButtonsContent = ({ onEdit, onDelete, itemType = 'item' }) => {
  return (
    <div>
      <Space direction="vertical" style={{ width: '100%' }}>
        <Button 
          type="primary" 
          block 
          icon={<EditOutlined />} 
          style={{ height: 48, marginBottom: 16 }}
          onClick={onEdit}
        >
          Edit
        </Button>
        <Button 
          danger 
          block 
          icon={<DeleteOutlined />} 
          style={{ height: 48 }}
          onClick={onDelete}
        >
          Delete
        </Button>
      </Space>
    </div>
  );
};

export default ActionButtonsContent;
