import React, { Children } from 'react';
import { Drawer, Button } from 'antd';
import "./index.css";

const DynamicDrawer = ({ 
  visible, 
  onClose, 
  title = 'Drawer',
  children,
  width = 700,
  placement = 'right',
  extra
}) => {
  return (
    <Drawer
      title={title}
      placement={placement}
      onClose={onClose}
      open={visible}
      width={width}
      extra={extra}
    >
      {children}
    </Drawer>
  );
};

export default DynamicDrawer;
