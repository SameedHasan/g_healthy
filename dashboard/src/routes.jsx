import React from 'react';
import DynamicTable from './components/tables/DynamicTable';
import Dashboard from './components/dashboard/Dashboard';
import useTableData from './hooks/useTableData';
// Remove imports for individual table components as we're using DynamicTable

// Component to wrap DynamicTable with data from useTableData hook
const DynamicTableWithData = ({ dataType, mediaType = 'all', searchText = '' }) => {
  const { data, loading, handleSearch } = useTableData(dataType, mediaType);

  // Apply search when searchText changes
  React.useEffect(() => {
    if (handleSearch) {
      handleSearch(searchText);
    }
  }, [searchText, handleSearch]);

  return (
    <DynamicTable
      dataType={dataType}
      data={data}
      loading={loading}
      onSearch={handleSearch}
      mediaType={mediaType}
    />
  );
};

// Import placeholder components for other routes
// In a real app, you would import actual components
const WeightLog = () => <div>Weight Log Content</div>;
const ActivityLog = () => <div>Activity Log Content</div>;
const KicksLog = () => <div>Kicks Log Content</div>;
const ContractionsLog = () => <div>Contractions Log Content</div>;
const Goals = () => <div>Goals Content</div>;
const Recipes = () => <div>Recipes Content</div>;
const Surveys = () => <div>Surveys Content</div>;
const Community = () => <div>Community Content</div>;
const Settings = () => <div>Settings Content</div>;
const Unauthorized = () => <div>You don't have permission to access this page</div>;


const routes = [
  {
    path: '/',
    element: <Dashboard />,
    // Open to all users
  },
  {
    path: '/logs',
    // This is a parent route, can have children
    children: [
      {
        path: 'goals',
        element: <DynamicTableWithData dataType="goals" />
      },
      {
        path: 'weight',
        element: <DynamicTableWithData dataType="weight-log" />
      },
      {
        path: 'activity',
        element: <DynamicTableWithData dataType="activity" />
      },
      {
        path: 'kicks',
        element: <DynamicTableWithData dataType="kicks" />
      },
      {
        path: 'contractions',
        element: <DynamicTableWithData dataType="contractions" />
      }
    ]
  },
  {
    path: '/media',
    // Media section with sub-routes
    children: [
      {
        path: 'all',
        element: <DynamicTableWithData dataType="media" mediaType="all" />
      },
      {
        path: 'images',
        element: <DynamicTableWithData dataType="media" mediaType="images" />
      },
      {
        path: 'videos',
        element: <DynamicTableWithData dataType="media" mediaType="videos" />
      },
      {
        path: 'audio',
        element: <DynamicTableWithData dataType="media" mediaType="audio" />
      },
      {
        path: 'documents',
        element: <DynamicTableWithData dataType="media" mediaType="documents" />
      }
    ]
  },
  {
    path: '/Lessons',
    element: <DynamicTableWithData dataType="Lessons" />
  },
  {
    path: '/goals',
    children: [
      {
        path: 'nutritional',
        element: <DynamicTableWithData dataType="nutritional" />
      },
      {
        path: 'activity',
        element: <DynamicTableWithData dataType="activity" />
      },
      {
        path: 'behavioral',
        element: <DynamicTableWithData dataType="behavioral" />
      }

    ]
  },
  {
    path: '/exercises',
    element: <DynamicTableWithData dataType="exercises" />
  },
  {
    path: '/recipes',
    element: <DynamicTableWithData dataType="recipes" />
  },
  {
    path: '/app-users',
    element: <DynamicTableWithData dataType="app-users" />
  },
  {
    path: '/surveys',
    element: <DynamicTableWithData dataType="surveys" />
  },
  {
    path: '/community',
    element: <DynamicTableWithData dataType="goals" />
  },
  {
    path: '/settings',
    children: [
      {
        path: 'accounts',
        element: <DynamicTableWithData dataType="accounts" />
      },
      {
        path: 'roles',
        element: <DynamicTableWithData dataType="roles" />
      },
      {
        path: 'divisions',
        element: <DynamicTableWithData dataType="divisions" />
      },
      {
        path: 'types',
        element: <DynamicTableWithData dataType="types" />
      },
      {
        path: 'categories',
        element: <DynamicTableWithData dataType="categories" />
      },
      {
        path: 'goal-preferences',
        element: <DynamicTableWithData dataType="goal-preferences" />
      },
      {
        path: 'tags',
        element: <DynamicTableWithData dataType="tags" />
      }
    ]
  },
  {
    path: '/unauthorized',
    element: <Unauthorized />
  },
  {
    // Catch-all route for 404
    path: '*',
    redirect: '/'
  }
];

export default routes;
