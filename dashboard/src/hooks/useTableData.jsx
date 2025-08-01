import { useState, useCallback, useMemo } from 'react';
import tableData from '../data/tableData';
import dpImg from '../assets/images/dp.png';

// Generate Lessons data
const generateLessonsData = () => {
  const LessonsItems = [
    { title: '5 Fun Ways to Stay Active', category: 'Lifestyle', tags: 'kids, activity, fitness', author: 'Coach Jenny', status: 'Published', date: '10/10/2025' },
    { title: 'How to Set Realistic Goals', category: 'Coaching', tags: 'goal-setting, progress, tips', author: 'Coach Marcus', status: 'Published', date: '10/10/2025' },
    { title: 'Understanding Childhood Obesity', category: 'Health Tips', tags: 'nutrition, growth, BMI', author: 'Dr. Ramos', status: 'Scheduled', date: '10/10/2025' },
    { title: '5 Fun Ways to Stay Active', category: 'Lifestyle', tags: 'kids, activity, fitness', author: 'Coach Jenny', status: 'Published', date: '10/10/2025' },
    { title: 'Smart Snacks for School Days', category: 'Nutrition', tags: 'snacks, healthy eating, family', author: 'Admin Sophia', status: 'Draft', date: '10/10/2025' },
    { title: 'Weekend Wellness Challenges', category: 'Lifestyle', tags: 'gamification, wellness, kids', author: 'Coach Jenny', status: 'Scheduled', date: '10/10/2025' },
    { title: '5 Fun Ways to Stay Active', category: 'Lifestyle', tags: 'kids, activity, fitness', author: 'Coach Jenny', status: 'Published', date: '10/10/2025' },
    { title: 'How to Set Realistic Goals', category: 'Coaching', tags: 'goal-setting, progress, tips', author: 'Coach Marcus', status: 'Published', date: '10/10/2025' },
    { title: 'Understanding Childhood Obesity', category: 'Health Tips', tags: 'nutrition, growth, BMI', author: 'Dr. Ramos', status: 'Scheduled', date: '10/10/2025' },
    { title: '5 Fun Ways to Stay Active', category: 'Lifestyle', tags: 'kids, activity, fitness', author: 'Coach Jenny', status: 'Published', date: '10/10/2025' },
  ];

  return LessonsItems.map((item, index) => ({
    key: `Lessons-${index + 1}`,
    id: `LIB${10000 + index}`,
    title: item.title,
    category: item.category,
    tags: item.tags,
    author: item.author,
    status: item.status,
    datePublished: item.date
  }));
};

// Generate media data
const generateMediaData = () => {
  const mediaTypes = [
    { name: 'Staying Active Every Day', type: 'pdf', size: '1 MB', tags: 'Lose weight', date: '10/10/2025' },
    { name: 'Welcome to Your Health Journey', type: 'video', size: '20 MB', tags: 'Intro, Family Health', date: '10/10/2025' },
    { name: 'Fun Ways to Stay Active', type: 'pdf', size: '1 MB', tags: 'Exercise, Kids, Movement', date: '10/10/2025' },
    { name: 'Healthy Eating Made Simple', type: 'pdf', size: '1 MB', tags: 'Nutrition, Meal, Planning', date: '10/10/2025' },
    { name: 'Setting Goals as a Family', type: 'video', size: '20 MB', tags: 'GoalSetting, Motivation', date: '10/10/2025' },
    { name: 'Why Sleep is Important', type: 'video', size: '20 MB', tags: 'Sleep, Wellness', date: '10/10/2025' },
    { name: 'Understanding Growth & BMI', type: 'video', size: '20 MB', tags: 'Health, Tracking', date: '10/10/2025' },
    { name: 'Making Healthy Habits Fun', type: 'pdf', size: '1 MB', tags: 'Routine, KidsHealth', date: '10/10/2025' },
    { name: 'Staying Hydrated Every Day', type: 'pdf', size: '1 MB', tags: 'Water, Wellness', date: '10/10/2025' },
    { name: 'Fun Ways to Stay Active', type: 'pdf', size: '1 MB', tags: 'Exercise, Kids, Movement', date: '10/10/2025' },
  ];

  return mediaTypes.map((item, index) => ({
    key: `media-${index + 1}`,
    id: `MED${10000 + index}`,
    name: item.name,
    fileSize: item.size,
    tags: item.tags,
    dateAdded: item.date,
    type: item.type,
    icon: item.type === 'pdf' ? 'pdf' : 'video'
  }));
};

// Generate app-users data
const generateAppUsersData = () => {
  const users = [
    { avatar: dpImg, initials: 'ES', name: 'Emily Smith', age: '40 yo', pregnancy: '36 weeks', email: 'examplemail@email.com', phone: '+1234567890', status: 'Active' },
    { avatar: null, initials: 'JW', name: 'Jenni Weigh', age: '40 yo', pregnancy: '36 weeks', email: 'examplemail@email.com', phone: '+1234567890', status: 'Active' },
    { avatar: dpImg, initials: 'AL', name: 'Amanda Lesley', age: '40 yo', pregnancy: '36 weeks', email: 'examplemail@email.com', phone: '+1234567890', status: 'Active' },
    { avatar: null, initials: 'DH', name: 'Dianna Hutaman', age: '40 yo', pregnancy: '36 weeks', email: 'examplemail@email.com', phone: '+1234567890', status: 'Active' },
    { avatar: null, initials: 'KF', name: 'Kelly Farizi', age: '40 yo', pregnancy: '36 weeks', email: 'examplemail@email.com', phone: '+1234567890', status: 'Active' },
  ];
  return users.map((item, index) => ({
      key: `user-${index + 1}`,
      name: item.name,
      avatar: item.avatar,
      initials: item.initials,
      age: item.age,
      pregnancy: item.pregnancy,
      email: item.email,
      phone: item.phone,
      status: item.status,
    }));
};

// Generate weight log data
const generateWeightLogData = () => {
  const rows = [
    { id: 'ID12345', name: 'Emma Wilson', address: '1234 Main Street, Baton Rouge, LA', prevWeight: 38.7, currentWeight: 37, logDate: '07/10/2026 10:30 AM' },
    { id: 'ID12345', name: 'Stephanie Nolan', address: '1234 Main Street, Baton Rouge, LA', prevWeight: 34, currentWeight: 35.5, logDate: '07/10/2026 10:30 AM' },
    { id: 'ID12345', name: 'Ashley Baker Jr', address: '1234 Main Street, Baton Rouge, LA', prevWeight: 30.3, currentWeight: 32, logDate: '07/10/2026 10:30 AM' },
    { id: 'ID12345', name: 'Morgan Russel', address: '1234 Main Street, Baton Rouge, LA', prevWeight: 36.1, currentWeight: 35.6, logDate: '07/10/2026 10:30 AM' },
    { id: 'ID12345', name: 'Lindsey Liam', address: '1234 Main Street, Baton Rouge, LA', prevWeight: 38.7, currentWeight: 40.5, logDate: '07/10/2026 10:30 AM' },
    { id: 'ID12345', name: 'Emma Wilson', address: '1234 Main Street, Baton Rouge, LA', prevWeight: 38.7, currentWeight: 42.5, logDate: '07/10/2026 10:30 AM' },
    { id: 'ID12345', name: 'Stephanie Nolan', address: '1234 Main Street, Baton Rouge, LA', prevWeight: 38.7, currentWeight: 44.5, logDate: '07/10/2026 10:30 AM' },
    { id: 'ID12345', name: 'Ashley Baker Jr', address: '1234 Main Street, Baton Rouge, LA', prevWeight: 38.7, currentWeight: 46.5, logDate: '07/10/2026 10:30 AM' },
    { id: 'ID12345', name: 'Morgan Russel', address: '1234 Main Street, Baton Rouge, LA', prevWeight: 38.7, currentWeight: 48.5, logDate: '07/10/2026 10:30 AM' },
    { id: 'ID12345', name: 'Lindsey Liam', address: '1234 Main Street, Baton Rouge, LA', prevWeight: 45, currentWeight: 50.5, logDate: '07/10/2026 10:30 AM' },
    { id: 'ID12345', name: 'Ashley Baker Jr', address: '1234 Main Street, Baton Rouge, LA', prevWeight: 42, currentWeight: 50.5, logDate: '07/10/2026 10:30 AM' },
    { id: 'ID12345', name: 'Morgan Russel', address: '1234 Main Street, Baton Rouge, LA', prevWeight: 41, currentWeight: 50.5, logDate: '07/10/2026 10:30 AM' },
  ];
  return rows.map((row, index) => ({
    key: `weight-log-${index + 1}`,
    ...row,
    change: parseFloat((row.currentWeight - row.prevWeight).toFixed(2)),
  }));
};

// Generate Activity data
const generateActivityData = () => {
  const rows = [
    { id: 'ID12345', name: 'Emma Wilson', address: '1234 Main Street, Baton Rouge, LA', activityType: 'Cardio', duration: 60, logDate: '07/10/2026 10:30 AM' },
    { id: 'ID12345', name: 'Stephanie Nolan', address: '1234 Main Street, Baton Rouge, LA', activityType: 'Yoga', duration: 50, logDate: '07/10/2026 10:28 AM' },
    { id: 'ID12345', name: 'Ashley Baker Jr', address: '1234 Main Street, Baton Rouge, LA', activityType: 'Strength', duration: 30, logDate: '07/10/2026 10:23 AM' },
    { id: 'ID12345', name: 'Morgan Russel', address: '1234 Main Street, Baton Rouge, LA', activityType: 'Meditation', duration: 90, logDate: '07/10/2026 10:22 AM' },
    { id: 'ID12345', name: 'Lindsey Liam', address: '1234 Main Street, Baton Rouge, LA', activityType: 'Meditation', duration: 45, logDate: '07/10/2026 10:21 AM' },
    // ... add more rows as needed ...
  ];
  return rows.map((row, index) => ({
    key: `activity-${index + 1}`,
    ...row,
  }));
};

// Generate Contractions data
const generateContractionsData = () => {
  const rows = [
    { id: 'ID12345', name: 'Emma Wilson', address: '1234 Main Street, Baton Rouge, LA', totalContractions: 10, avgDuration: '2 hrs 30 min', avgInterval: '10 min', logDate: '07/10/2026 10:30 AM', status: 'Normal' },
    { id: 'ID12345', name: 'Stephanie Nolan', address: '1234 Main Street, Baton Rouge, LA', totalContractions: 20, avgDuration: '3 hrs', avgInterval: '30 min', logDate: '07/10/2026 10:28 AM', status: 'Irregular' },
    { id: 'ID12345', name: 'Ashley Baker Jr', address: '1234 Main Street, Baton Rouge, LA', totalContractions: 26, avgDuration: '2 hrs', avgInterval: '25 min', logDate: '07/10/2026 10:23 AM', status: 'Warning' },
    { id: 'ID12345', name: 'Morgan Russel', address: '1234 Main Street, Baton Rouge, LA', totalContractions: 15, avgDuration: '1 hr 30 min', avgInterval: '2 min', logDate: '07/10/2026 10:22 AM', status: 'Possible Labor' },
    { id: 'ID12345', name: 'Lindsey Liam', address: '1234 Main Street, Baton Rouge, LA', totalContractions: 8, avgDuration: '2 hrs', avgInterval: '10 min', logDate: '07/10/2026 10:21 AM', status: 'Active Labor' },
    // ... add more rows as needed ...
  ];
  return rows.map((row, index) => ({
    key: `contraction-${index + 1}`,
    ...row,
  }));
};

// Generate Kicks data
const generateKicksData = () => {
  const rows = [
    { id: 'ID12345', name: 'Emma Wilson', address: '1234 Main Street, Baton Rouge, LA', numberOfKicks: 10, start: '07/10/2026 8:30 AM', end: '07/10/2026 10:30 AM', note: 'After eating' },
    { id: 'ID12345', name: 'Stephanie Nolan', address: '1234 Main Street, Baton Rouge, LA', numberOfKicks: 10, start: '07/10/2026 8:28 AM', end: '07/10/2026 10:28 AM', note: 'At night' },
    { id: 'ID12345', name: 'Ashley Baker Jr', address: '1234 Main Street, Baton Rouge, LA', numberOfKicks: 12, start: '07/10/2026 8:23 AM', end: '07/10/2026 10:23 AM', note: 'Loud noise' },
    { id: 'ID12345', name: 'Morgan Russel', address: '1234 Main Street, Baton Rouge, LA', numberOfKicks: 8, start: '07/10/2026 8:22 AM', end: '07/10/2026 10:22 AM', note: 'Emotional' },
    { id: 'ID12345', name: 'Lindsey Liam', address: '1234 Main Street, Baton Rouge, LA', numberOfKicks: 9, start: '07/10/2026 8:21 AM', end: '07/10/2026 10:21 AM', note: 'After eating' },
    // ... add more rows as needed ...
  ];
  return rows.map((row, index) => ({
    key: `kick-${index + 1}`,
    ...row,
  }));
};

// Generate Accounts data
const generateAccountsData = () => {
  const rows = [
    { name: 'Amanda Lee', initials: 'AL', avatar: null, role: 'Super Admin', division: ['Division 1', 'Division 2'], lastLogin: 'Today', status: 'Active' },
    { name: 'Michael Santos', initials: 'MS', avatar: null, role: 'Hospital Admin', division: ['Division 2', 'Long Division 5', 'Example Division 3', '+2'], lastLogin: 'Yesterday', status: 'Active' },
    { name: 'Karen Lim', initials: 'KL', avatar: null, role: 'Coach Supervisor', division: ['Division 3', 'Other Division'], lastLogin: '10/10/2025', status: 'Active' },
    { name: 'Andrew Nolan', initials: 'AN', avatar: null, role: 'Coach Supervisor', division: ['Division 1', 'Example'], lastLogin: '10/10/2025', status: 'Active' },
    { name: 'Samuel Grant', initials: 'SG', avatar: null, role: 'Content Manager', division: ['Division 1', 'Example Long Division 2'], lastLogin: '10/10/2025', status: 'Active' },
    { name: 'Olivia Chen', initials: 'OC', avatar: null, role: 'System Editor', division: ['Division 1'], lastLogin: '10/10/2025', status: 'Active' },
    { name: 'Jorge Morales', initials: 'JM', avatar: null, role: 'Support Specialist', division: ['Division 1', 'Division 2'], lastLogin: '10/10/2025', status: 'Active' },
    // ... more rows as needed ...
  ];
  return rows.map((row, index) => ({
    key: `account-${index + 1}`,
    ...row,
  }));
};

// Generate Roles data
const generateRolesData = () => {
  const rows = [
    { name: 'Super Admin', numberOfUser: 4, status: 'Active' },
    { name: 'Hospital Admin', numberOfUser: 10, status: 'Active' },
    { name: 'Coach Supervisor', numberOfUser: 5, status: 'Active' },
    { name: 'Content Manager', numberOfUser: 7, status: 'Active' },
    { name: 'System Editor', numberOfUser: 12, status: 'Active' },
    { name: 'Support Specialist', numberOfUser: 8, status: 'Active' },
    // ... more rows as needed ...
  ];
  return rows.map((row, index) => ({
    key: `role-${index + 1}`,
    ...row,
  }));
};

// Generate Divisions data
const generateDivisionsData = () => {
  const rows = [
    { name: 'Division 1', numberOfUser: 120, status: 'Active' },
    { name: 'Division 2', numberOfUser: 32, status: 'Active' },
    { name: 'Division 3', numberOfUser: 36, status: 'Active' },
    { name: 'Division 4', numberOfUser: 68, status: 'Active' },
    // ... more rows as needed ...
  ];
  return rows.map((row, index) => ({
    key: `division-${index + 1}`,
    ...row,
  }));
};

// Generate Types data
const generateTypesData = () => {
  const rows = [
    { name: 'Library', createdDate: '10/10/2025', status: 'Active' },
    { name: 'Recipes', createdDate: '10/10/2025', status: 'Active' },
    { name: 'Lessons', createdDate: '10/10/2025', status: 'Active' },
    // ... more rows as needed ...
  ];
  return rows.map((row, index) => ({
    key: `type-${index + 1}`,
    ...row,
  }));
};

// Generate Categories data
const generateCategoriesData = () => {
  const rows = [
    { categoryName: 'Breakfast', type: 'Recipes', itemsUsed: 24, createdDate: '10/10/2025', status: 'Active' },
    { categoryName: 'Lunch', type: 'Recipes', itemsUsed: 8, createdDate: '10/10/2025', status: 'Active' },
    { categoryName: 'Dinner', type: 'Recipes', itemsUsed: 12, createdDate: '10/10/2025', status: 'Active' },
    { categoryName: 'Drinks', type: 'Recipes', itemsUsed: 20, createdDate: '10/10/2025', status: 'Active' },
    { categoryName: 'Desserts', type: 'Recipes', itemsUsed: 8, createdDate: '10/10/2025', status: 'Active' },
    { categoryName: 'Behavioral', type: 'Goal', itemsUsed: 8, createdDate: '10/10/2025', status: 'Active' },
    { categoryName: 'Nutritional', type: 'Goal', itemsUsed: 8, createdDate: '10/10/2025', status: 'Active' },
    { categoryName: 'Activity', type: 'Goal', itemsUsed: 8, createdDate: '10/10/2025', status: 'Active' },
    // ... more rows as needed ...
  ];
  return rows.map((row, index) => ({
    key: `category-${index + 1}`,
    ...row,
  }));
};

// Generate Goal Preferences data
const generateGoalPreferencesData = () => {
  const rows = [
    { name: 'Meal Planning & Preparation', goalCategory: 'Nutritional', helpText: 'Plan meals, prep ahead, and simplify grocery shopping.', status: 'Active' },
    { name: 'Macronutrient Distribution', goalCategory: 'Nutritional', helpText: 'Balance carbs, protein, and fats to support your goals.', status: 'Active' },
    { name: 'Caloric Awareness', goalCategory: 'Nutritional', helpText: 'Track your calorie intake to manage weight, energy, and health.', status: 'Active' },
    { name: 'Dietary Patterns', goalCategory: 'Nutritional', helpText: 'Plan meals, prep ahead, and simplify grocery shopping.', status: 'Active' },
    { name: 'Nutritional Education', goalCategory: 'Nutritional', helpText: 'Balance carbs, protein, and fats to support your goals.', status: 'Active' },
    { name: 'Resistance Training', goalCategory: 'Activity', helpText: 'Plan meals, prep ahead, and simplify grocery shopping.', status: 'Active' },
    { name: 'Cardiovascular Exercise', goalCategory: 'Activity', helpText: 'Balance carbs, protein, and fats to support your goals.', status: 'Active' },
    { name: 'Flexibility & Mobility Work', goalCategory: 'Activity', helpText: 'Track your calorie intake to manage weight, energy, and health.', status: 'Active' },
    { name: 'NEAT (Non-Exercise Activity Thermogenesis)', goalCategory: 'Activity', helpText: 'Plan meals, prep ahead, and simplify grocery shopping.', status: 'Active' },
    // ... more rows as needed ...
  ];
  return rows.map((row, index) => ({
    key: `goal-preference-${index + 1}`,
    ...row,
  }));
};

// Generate Tags data
const generateTagsData = () => {
  const rows = [
    { categoryName: 'Quick', type: 'Recipes', itemsUsed: 24, createdDate: '10/10/2025', status: 'Active' },
    { categoryName: 'Vegetarian', type: 'Recipes', itemsUsed: 8, createdDate: '10/10/2025', status: 'Active' },
    { categoryName: 'Under 500 cal', type: 'Recipes', itemsUsed: 12, createdDate: '10/10/2025', status: 'Active' },
    { categoryName: 'Immune booster', type: 'Recipes', itemsUsed: 20, createdDate: '10/10/2025', status: 'Active' },
    { categoryName: 'Low sodium', type: 'Recipes', itemsUsed: 8, createdDate: '10/10/2025', status: 'Active' },
    { categoryName: 'Lifestyle', type: 'Library', itemsUsed: 8, createdDate: '10/10/2025', status: 'Active' },
    { categoryName: 'Health Tips', type: 'Library', itemsUsed: 8, createdDate: '10/10/2025', status: 'Active' },
    { categoryName: 'Parenting', type: 'Library', itemsUsed: 8, createdDate: '10/10/2025', status: 'Active' },
    { categoryName: 'Nutrition', type: 'Library', itemsUsed: 8, createdDate: '10/10/2025', status: 'Active' },
    // ... more rows as needed ...
  ];
  return rows.map((row, index) => ({
    key: `tag-${index + 1}`,
    ...row,
  }));
};

// Get initial data based on data type
const getInitialData = (dataType) => {
  switch (dataType) {
    case 'goals':
      return tableData;
    case 'Lessons':
      return generateLessonsData();
    case 'media':
      return generateMediaData();
    case 'app-users':
      return generateAppUsersData();
    case 'weight-log':
      return generateWeightLogData();
    case 'activity':
      return generateActivityData();
    case 'contractions':
      return generateContractionsData();
    case 'kicks':
      return generateKicksData();
    case 'accounts':
      return generateAccountsData();
    case 'roles':
      return generateRolesData();
    case 'divisions':
      return generateDivisionsData();
    case 'types':
      return generateTypesData();
    case 'categories':
      return generateCategoriesData();
    case 'goal-preferences':
      return generateGoalPreferencesData();
    case 'tags':
      return generateTagsData();
    default:
      return [];
  }
};

// Get search fields based on data type
const getSearchFields = (dataType) => {
  switch (dataType) {
    case 'goals':
      return ['name', 'goal', 'category', 'address', 'id'];
    case 'Lessons':
      return ['title', 'category', 'tags', 'author', 'status', 'datePublished'];
    case 'media':
      return ['name', 'tags', 'fileSize', 'dateAdded'];
    case 'app-users':
      return ['name', 'age', 'pregnancy', 'email', 'phone', 'status'];
    case 'activity':
      return ['id', 'name', 'address', 'activityType', 'duration', 'logDate'];
    case 'contractions':
      return ['id', 'name', 'address', 'totalContractions', 'avgDuration', 'avgInterval', 'logDate', 'status'];
    case 'kicks':
      return ['id', 'name', 'address', 'numberOfKicks', 'start', 'end', 'note'];
    case 'accounts':
      return ['name', 'role', 'division', 'lastLogin', 'status'];
    case 'roles':
      return ['name', 'numberOfUser', 'status'];
    case 'divisions':
      return ['name', 'numberOfUser', 'status'];
    case 'types':
      return ['name', 'createdDate', 'status'];
    case 'categories':
      return ['categoryName', 'type', 'itemsUsed', 'createdDate', 'status'];
    case 'goal-preferences':
      return ['name', 'goalCategory', 'helpText', 'status'];
    case 'tags':
      return ['categoryName', 'type', 'itemsUsed', 'createdDate', 'status'];
    default:
      return ['name', 'id'];
  }
};

const useTableData = (dataType = 'goals', mediaType = 'all') => {
  // Get initial data based on data type
  const initialData = useMemo(() => getInitialData(dataType), [dataType]);

  // Get search fields based on data type
  const searchFields = useMemo(() => getSearchFields(dataType), [dataType]);

  // Filter media data based on media type
  const filteredInitialData = useMemo(() => {
    if (dataType !== 'media' || mediaType === 'all') {
      return initialData;
    }

    const typeMap = {
      'images': 'image',
      'videos': 'video',
      'audio': 'audio',
      'documents': 'pdf'
    };

    const fileType = typeMap[mediaType] || null;
    if (!fileType) return initialData;

    return initialData.filter(item => item.type === fileType);
  }, [initialData, dataType, mediaType]);

  const [data, setData] = useState(filteredInitialData);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(false);
  const [sortField, setSortField] = useState(null);
  const [sortOrder, setSortOrder] = useState('ascend');

  // Handle search
  const handleSearch = useCallback((value) => {
    setLoading(true);
    setSearchTerm(value);

    if (!value) {
      setData(initialData);
      setLoading(false);
      return;
    }

    const lowerCaseValue = value.toLowerCase();
    const filteredData = initialData.filter(item =>
      searchFields.some(field => {
        const fieldValue = item[field];
        return fieldValue && String(fieldValue).toLowerCase().includes(lowerCaseValue);
      })
    );

    setData(filteredData);
    setLoading(false);
  }, [initialData, searchFields]);

  // Handle sorting
  const handleSort = useCallback((field) => {
    setLoading(true);

    // If clicking the same field, toggle sort order
    const newSortOrder = field === sortField && sortOrder === 'ascend' ? 'descend' : 'ascend';

    setSortField(field);
    setSortOrder(newSortOrder);

    const sortedData = [...data].sort((a, b) => {
      const valueA = a[field];
      const valueB = b[field];

      // Handle string comparison
      if (typeof valueA === 'string' && typeof valueB === 'string') {
        return newSortOrder === 'ascend'
          ? valueA.localeCompare(valueB)
          : valueB.localeCompare(valueA);
      }

      // Handle number comparison
      if (valueA < valueB) return newSortOrder === 'ascend' ? -1 : 1;
      if (valueA > valueB) return newSortOrder === 'ascend' ? 1 : -1;
      return 0;
    });

    setData(sortedData);
    setLoading(false);
  }, [data, sortField, sortOrder]);

  return {
    data,
    searchTerm,
    loading,
    handleSearch,
    handleSort
  };
};

export default useTableData;
