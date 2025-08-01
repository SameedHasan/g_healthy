import React, { useMemo } from 'react';
import { Layout, Menu, Image, Typography } from 'antd';
import { useLocation } from 'react-router-dom';
import createMenuItems from '../../data/menuItems.jsx';
import SidebarFooter from './SidebarFooter';
import logo from '@/assets/images/logo.png';
import logo2 from '@/assets/images/logo_2.png';
import '@/App.css';
import { ArrowDownIcon } from '../../utils/icons/index.jsx';
import generateMenuItems from '../utility/generateMenuItems.jsx';

const { Sider } = Layout;
const { Title } = Typography;

const Sidebar = ({ collapsed, onMenuSelect, menuItems=[] }) => {
  const location = useLocation();
  const sidebarStyle = {
    overflow: 'auto',
    backgroundColor: '#fff',
    height: '100vh',
    position: 'fixed',
    left: 0,
    top: 0,
    bottom: 0,
    borderRight: '1px solid #f0f0f0',
    zIndex: 100
  };

  // Enhanced: Helper to find the full key path (parent and child) for nested menu items
  const findSelectedKeyPath = (items, path, parentKeys = []) => {
    let bestMatch = { keys: ['dashboard'], length: 0 };
    for (const item of items) {
      let currentKeys = [...parentKeys, item.key];
      if (item.label && item.label.props && item.label.props.to) {
        const to = item.label.props.to;
        if (path === to || path.startsWith(to + '/')) {
          if (to.length > bestMatch.length) {
            bestMatch = { keys: currentKeys, length: to.length };
          }
        }
      }
      if (item.children) {
        const childMatch = findSelectedKeyPath(item.children, path, currentKeys);
        if (childMatch.length > bestMatch.length) {
          bestMatch = childMatch;
        }
      }
    }
    return bestMatch;
  };

  const selectedKeys = useMemo(() => findSelectedKeyPath(menuItems, location.pathname).keys, [menuItems, location.pathname]);

  return (
    <Sider
      collapsible
      collapsed={collapsed}
      width={210}
      theme="light"
      className="sidebar-container"
      style={sidebarStyle}
      trigger={null}
    >
      <div className="sidebar-brand">
        <Image
          src={collapsed ? logo2 : logo} preview={false} />
      </div>
      <div className={`sidebar-menu-container ${collapsed ? 'sidebar-collapsed' : ''}`}>
        <Menu
          theme="light"
          selectedKeys={selectedKeys}
          mode="inline"
          items={menuItems}
          className="sidebar-menu"
          onSelect={onMenuSelect}
          {...(!collapsed && {
            expandIcon: ({ isOpen }) => (
              <ArrowDownIcon
                style={{
                  transform: isOpen ? 'rotate(180deg)' : 'rotate(0deg)',
                  transition: 'transform 0.3s ease',
                }}
                color={isOpen ? '#1272BF' : '#616161'}
              />
            )
          })}
        />
      </div>
      <SidebarFooter collapsed={collapsed} />
    </Sider>
  );
};

export default Sidebar;
