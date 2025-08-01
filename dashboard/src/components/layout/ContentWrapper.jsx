import React from 'react';
import { Layout } from 'antd';

const { Content } = Layout;

const ContentWrapper = ({ children, theme }) => {
  const borderRadius = theme?.token?.borderRadius || 8;
  
  return (
    <Content style={{ 
      
      overflow: 'auto', 
      paddingBottom: '24px'
     
    }}>
      <div 
        style={{ 
          padding: '0px 30px'
        }}
      >
        {children}
      </div>
    </Content>
  );
};

export default ContentWrapper;
