import React from 'react';
import { Layout, Menu, Typography } from 'antd';
import { Link, useLocation } from 'react-router-dom';
import { AllMediaIcon, FolderIcon, MediaImageIcon, MediaVideoIcon } from '../../utils/icons';

const { Sider } = Layout;
const { Title } = Typography;

/**
 * MediaSidebar component - Sub sidebar specifically for Media section
 * Appears when Media is selected in the main sidebar
 */
const MediaSidebar = ({ visible, onSelect }) => {
  const location = useLocation();
  const pathname = location.pathname;

  // Media section sub-menu items
  const mediaSubMenuItems = [
    {
      key: 'media-all',
      to: '/media/all',
      icon: <Link to="/media/all"><AllMediaIcon isActive={false} /></Link>,
      label: <Link to="/media/all">All Media</Link>
    },
    {
      key: 'media-videos',
      to: '/media/videos',
      icon: <Link to="/media/videos"><MediaVideoIcon isActive={false} /></Link>,
      label: <Link to="/media/videos">Videos</Link>
    },
    {
      key: 'media-images',
      to: '/media/images',
      icon: <Link to="/media/images"><MediaImageIcon isActive={false} /></Link>,
      label: <Link to="/media/images">Images</Link>
    },
    {
      key: 'media-documents',
      to: '/media/documents',
      icon: <Link to="/media/documents"><FolderIcon isActive={false} /></Link>,
      label: <Link to="/media/documents">Documents</Link>
    }
  ];

  // Helper to find the best matching key for the current path
  const findSelectedKey = (items, path) => {
    let match = { key: 'media-all', length: 0 };
    for (const item of items) {
      if (item.to && (path === item.to || path.startsWith(item.to + '/'))) {
        if (item.to.length > match.length) {
          match = { key: item.key, length: item.to.length };
        }
      }
    }
    return match.key;
  };

  const selectedKey = findSelectedKey(mediaSubMenuItems, pathname);
  // Set isActive for icons
  const menuItemsWithActive = mediaSubMenuItems.map(item => ({
    ...item,
    icon: <Link to={item.to}>{React.cloneElement(item.icon.props.children, { isActive: selectedKey === item.key })}</Link>,
  }));


  return (
    <Sider
      width={220}
      theme="light"
      style={{
        overflow: 'auto',
        height: '100vh',
        position: 'fixed',
        left: 80, // Position right after the collapsed main sidebar
        top: 0,
        bottom: 0,
        borderRight: '1px solid #f0f0f0',
        zIndex: 99, // Just below the main sidebar
        transform: visible ? 'translateX(0)' : 'translateX(-100%)',
        transition: 'transform 0.15s ease-out',
        opacity: visible ? 1 : 0,
        pointerEvents: visible ? 'auto' : 'none'
      }}
    >
      <div style={{
        height: '64px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'flex-start',
        paddingLeft: '24px',
        marginBottom: '8px'
      }}>
        <Title level={4} style={{ margin: 0 }}>
          Media
        </Title>
      </div>
      <Menu
        theme="light"
        defaultSelectedKeys={[selectedKey]}
        selectedKeys={[selectedKey]}
        items={menuItemsWithActive}
        mode="inline"
        onClick={onSelect}
        className='media-sidebar-menu'
        style={{ borderRight: 0 }}
      />
    </Sider>
  );
};

export default MediaSidebar;
