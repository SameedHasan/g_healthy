// generateMenuItems.js
import React from 'react';
import { Link } from 'react-router-dom';
import * as Icons from '../../utils/icons';


const generateMenuItems = (menuData, currentPath) => {

  const isActive = (path) =>
    currentPath === path || currentPath.startsWith(path + '/');

  return menuData.map((menu) => {
    const basePath = menu.path || `/${menu.name?.toLowerCase()}`;
    const IconComponent = Icons[menu?.icon]; // access icon like "LogsIcon"

    const menuItem = {
      key: menu.name?.toLowerCase(),
      icon: IconComponent ? (
        <Link to={basePath}>
          <IconComponent active={isActive(basePath)} width={24} height={24} />
        </Link>
      ) : null,
      label: <Link to={basePath}>{menu.title || menu.name}</Link>,
    };

    if (menu.subRoutes && menu.subRoutes.length > 0 && menu.path !== "/media") {
      menuItem.children = menu.subRoutes.map((sub) => {
        const subPath = `${basePath}/${sub.path || sub.key || sub.name}`.toLowerCase();
        return {
          key: sub.name?.toLowerCase(),
          label: <Link to={subPath} state={{
            "page" : sub?.page || ""
          }}>{sub.label || sub.name}</Link>,
        };
      });
    }

    return menuItem;
  });
};

export default generateMenuItems;
