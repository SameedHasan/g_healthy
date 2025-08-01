import React, { useState } from 'react';
import { Dropdown, Menu } from 'antd';

const sortOptions = [
  { key: 'newest', label: 'Newest first' },
  { key: 'oldest', label: 'Oldest first' },
  { key: 'name', label: 'Name' },
  { key: 'size', label: 'Size' },
];

const SortTable = () => {
  const [selected, setSelected] = useState('newest');

  const menu = {
    items: sortOptions.map(opt => ({
      key: opt.key,
      label: opt.label,
    })),
    onClick: ({ key }) => setSelected(key),
    selectedKeys: [selected],
  };

  return (
    <Dropdown menu={menu} trigger={['click']} placement="bottom">
      <div className="sort-pill">
        <p>Sort by:</p>
         <span>{sortOptions.find(opt => opt.key === selected)?.label}</span>
      </div>
    </Dropdown>
  );
};

export default SortTable;

