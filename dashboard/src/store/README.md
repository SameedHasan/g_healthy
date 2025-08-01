# Zustand Store Structure

## Routes Store

The routes store manages the application's routing data and provides convenient methods to access different types of routes.

### Usage Examples

```jsx
import { useRoutesStore } from '../store';

// In a component
function MyComponent() {
  const { 
    routes, 
    isLoading, 
    error, 
    fetchRoutes, 
    getMenuRoutes, 
    getListRoutes 
  } = useRoutesStore();

  // Access specific route types
  const menuRoutes = getMenuRoutes();
  const listRoutes = getListRoutes();

  // Manual fetch if needed
  const handleRefresh = () => {
    fetchRoutes();
  };

  return (
    <div>
      {isLoading && <div>Loading...</div>}
      {error && <div>Error: {error}</div>}
      {routes.map(route => (
        <div key={route.path}>{route.name}</div>
      ))}
    </div>
  );
}
```

### Store Methods

- `routes`: Array of all routes
- `isLoading`: Boolean indicating if routes are being fetched
- `error`: Error message if fetch failed
- `isInitialized`: Boolean indicating if routes have been loaded
- `fetchRoutes()`: Manually fetch routes from API
- `getRoutesByType(pageView)`: Get routes by page_view type
- `getRouteByPath(path)`: Get specific route by path
- `getMenuRoutes()`: Get all menu routes
- `getListRoutes()`: Get all list routes
- `getDashboardRoutes()`: Get all dashboard routes
- `reset()`: Reset store to initial state

## Adding New Stores

1. Create a new store file: `src/store/newStore.js`
2. Export it from `src/store/index.js`
3. Use it in components with the same pattern

Example:
```jsx
// src/store/userStore.js
import { create } from 'zustand';

export const useUserStore = create((set, get) => ({
  user: null,
  setUser: (user) => set({ user }),
  // ... other actions
}));

// src/store/index.js
export { useUserStore } from './userStore';
``` 