import React, { useState, useEffect, useMemo } from 'react';
import { Layout } from 'antd';
import { useNavigate, useLocation } from 'react-router-dom';
import Sidebar from './Sidebar';
import MediaSidebar from './MediaSidebar';
import Header from './Header';
import ContentWrapper from './ContentWrapper';
import generateMenuItems from '../utility/generateMenuItems';

const titles = {
  '/': 'Dashboard',
  '/goals/nutritional': 'Nutritional',
  '/goals/activity': 'Activity',
  '/goals/behavioral': 'Behavioral',
  '/logs/goals': 'Goals',
  '/logs/weight': 'Weight',
  '/logs/activity': 'Activity',
  '/logs/kicks': 'Kicks',
  '/logs/contractions': 'Contractions',
  '/media': 'Media',
  '/Lessons': 'Lessons',
  '/exercises': 'Exercises',
  '/recipes': 'Recipes',
  '/app-users': 'App Users',
  '/surveys': 'Surveys',
  '/community': 'Community',
  '/settings': 'Settings',
  '/settings/accounts': 'Accounts',
  '/settings/roles': 'Roles',
  '/settings/divisions': 'Divisions',
  '/settings/types': 'Types',
  '/settings/categories': 'Categories',
  '/settings/goal-preferences': 'Goal Preferences',
  '/settings/tags': 'Tags'
};



const MainLayout = ({ children, theme, routesData }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const [collapsed, setCollapsed] = useState(false);
  const [forceCollapsed, setForceCollapsed] = useState(false);
  const [showMediaSidebar, setShowMediaSidebar] = useState(false);
  const [searchText, setSearchText] = useState('');


  const handleSearch = (value) => setSearchText(value);

  useEffect(() => {
    const isMediaPath = location.pathname.startsWith('/media');
    setShowMediaSidebar(isMediaPath);
    setForceCollapsed(isMediaPath);
  }, [location.pathname]);

  const toggleSidebar = () => {
    if (!showMediaSidebar) setCollapsed(!collapsed);
  };
  const menuItems = useMemo(() => {
    return generateMenuItems(routesData,location.pathname);
  }, [location.pathname]);

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sidebar
        collapsed={collapsed || forceCollapsed}
        theme={theme}
        menuItems={menuItems}
      />

      <MediaSidebar
        visible={showMediaSidebar}
        theme={theme}
      />

      <Layout
        style={useMemo(() => ({
          marginLeft: (collapsed || forceCollapsed)
            ? (showMediaSidebar ? 300 : 80)
            : 210,
          transition: 'margin-left 0.15s ease-out',
          flex: 1,
          width: 'calc(100vw - ' +
            ((collapsed || forceCollapsed)
              ? (showMediaSidebar ? '308px' : '80px')
              : '210px') +
            ')',
        }), [collapsed, forceCollapsed, showMediaSidebar])}
      >
        <Header
          collapsed={collapsed}
          toggleSidebar={toggleSidebar}
          onSearch={handleSearch}
        />
        <ContentWrapper theme={theme}>
          {React.cloneElement(children, { searchText: searchText })}
        </ContentWrapper>
      </Layout>
    </Layout>
  );
};

export default MainLayout;
