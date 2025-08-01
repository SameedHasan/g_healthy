import React from 'react';
import { Typography, Space } from 'antd';
import { DeleteOutlined } from '@ant-design/icons';
import { DeleteIcon } from '../../utils/icons';

const { Title, Text, Paragraph } = Typography;

const DeleteConfirmContent = ({ item = {}, itemType = 'item' }) => {
  const itemName = item.title || item.name || 'this ' + itemType;

  return (
    <div className='confirmation-modal'>
      <div className='icon'>
        <DeleteIcon bg />
      </div>
      <div className='content'>
        <h2 >Delete article?</h2>
        <p>
          Are you sure you want to delete "{itemName}" article? There is no way to recover it once it's been deleted.
        </p>
      </div>
    </div>
  );
};

export default DeleteConfirmContent;
