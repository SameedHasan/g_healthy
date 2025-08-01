import React from 'react';
import { Routes, Route, Navigate, Outlet } from 'react-router-dom';

const RenderRoutes = ({ routes }) => {
  const renderRoutesRecursively = (routesArray, parentPath = '') => {
    return routesArray.flatMap((route) => {
      const fullPath = parentPath
        ? `${parentPath.replace(/\/$/, '')}/${route.path.replace(/^\//, '')}`
        : route.path;

      const elements = [];
      // Handle redirect route
      if (route.redirect) {
        elements.push(
          <Route
            key={fullPath + '_redirect'}
            path={route.path}
            element={<Navigate to={route.redirect} replace />}
          />
        );
        return elements;
      }

      // Auto-redirect to first child if it's a Menu with subroutes
      if (route.page_view === 'Menu' && route.children?.length > 0) {
        const firstChild = route.children[0];
        const firstChildPath = `${fullPath}/${firstChild.path?.replace(/^\//, '') || ''}`;
        elements.push(
          <Route
            key={fullPath + '_auto_redirect'}
            path={route.path}
            element={<Navigate to={firstChildPath} replace />}
          />
        );
      }

      // Main route with its element or <Outlet /> for nested children
      if (route.children && route.children.length > 0) {
        // Route has children - use Outlet and render children
        elements.push(
          <Route
            key={fullPath}
            path={route.path}
            element={route.element || <Outlet />}
          >
            {renderRoutesRecursively(route.children, fullPath)}
          </Route>
        );
      } else {
        // Route has no children - render the element directly
        elements.push(
          <Route
            key={fullPath}
            path={route.path}
            element={route.element}
          />
        );
      }

      return elements;
    });
  };

  return <Routes>{renderRoutesRecursively(routes)}</Routes>;
};

export default RenderRoutes;
