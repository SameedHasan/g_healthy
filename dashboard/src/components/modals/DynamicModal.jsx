import React from 'react';
import { Modal } from 'antd';

const DynamicModal = ({
  visible,
  onCancel,
  title = 'Modal',
  children,
  width = 700,
  footerButtons,
  centered = false,
  className // <- accept className prop
}) => {
  return (
    <Modal
      title={title}
      open={visible}
      onCancel={onCancel}
      width={width}
      footer={footerButtons}
      centered={centered}
      className={className}
    >
      {children}
    </Modal>
  );
};

export default DynamicModal;
