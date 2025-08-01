import React from 'react';
import { Link } from 'react-router-dom';
import { DashboardIcon, LogsIcon, MediaIcon, LessonsIcon, GoalsIcon, RecipesIcon, AppUserIcon, SurveysIcon, CommunityIcon, SettingsIcon, ExercisesIcon } from '../utils/icons';

// Function to create menu items with Link components
const createMenuItems = (currentPath) => {
  // Helper function to check if a path is active
  const isActive = (path) => currentPath === path || currentPath.startsWith(path + '/');

  return [
    {
      key: 'dashboard',
      icon: (
        <Link to="/">
          <DashboardIcon width={24} height={24} active={isActive('/')} />
        </Link>
      ),
      label: <Link to="/">Dashboard</Link>
    },
    {
      key: 'logs',
      icon: <LogsIcon active={isActive('/logs')} />,
      label: "Logs",
      children: [
        {
          key: 'goals-log',
          label: <Link to="/logs/goals">Goals</Link>
        },
        {
          key: 'weight',
          label: <Link to="/logs/weight">Weight</Link>
        },
        {
          key: 'activity-log',
          label: <Link to="/logs/activity">Activity</Link>
        },
        {
          key: 'kicks',
          label: <Link to="/logs/kicks">Kicks</Link>
        },
        {
          key: 'contractions',
          label: <Link to="/logs/contractions">Contractions</Link>
        },
      ],
    },
    {
      key: 'media',
      icon: (
        <Link to="/media">
          <MediaIcon active={isActive('/media')} />
        </Link>
      ),
      label: <Link to="/media">Media</Link>
    },
    {
      key: 'Lessons',
      icon: (
        <Link to="/Lessons">
          <LessonsIcon active={isActive('/Lessons')} />
        </Link>
      ),
      label: <Link to="/Lessons">Lessons</Link>
    },
    {
      key: 'goals-main',
      icon: <GoalsIcon active={isActive('/goals')} />,
      label: 'Goals',
      children: [
        {
          key: 'nutritional',
          label: <Link to="/goals/nutritional">Nutritional</Link>
        },
        {
          key: 'activity',
          label: <Link to="/goals/activity">Activity</Link>
        },
        {
          key: 'behavioral',
          label: <Link to="/goals/behavioral">Behavioral</Link>
        },
      ],
    },
    {
      key: 'exercises',
      icon: (
        <Link to="/exercises">
          <ExercisesIcon active={isActive('/exercises')} />
        </Link>
      ),
      label: <Link to="/exercises">Exercises</Link>
    },
    {
      key: 'recipes',
      icon: (
        <Link to="/recipes">
          <RecipesIcon active={isActive('/recipes')} />
        </Link>
      ),
      label: <Link to="/recipes">Recipes</Link>
    },
    {
      key: 'app-users',
      icon: (
        <Link to="/app-users">
          <AppUserIcon active={isActive('/app-users')} />
        </Link>
      ),
      label: <Link to="/app-users">App Users</Link>
    },
    {
      key: 'surveys',
      icon: (
        <Link to="/surveys">
          <SurveysIcon active={isActive('/surveys')} />
        </Link>
      ),
      label: <Link to="/surveys">Surveys</Link>
    },
    {
      key: 'community',
      icon: (
        <Link to="/community">
          <CommunityIcon active={isActive('/community')} />
        </Link>
      ),
      label: <Link to="/community">Community</Link>
    },
    {
      key: 'settings-main',
      icon: <SettingsIcon active={isActive('/settings')} />,
      label: 'Settings',
      children: [
        {
          key: 'accounts-setting',
          label: <Link to="/settings/accounts">Accounts</Link>
        },
        {
          key: 'roles',
          label: <Link to="/settings/roles">Roles</Link>
        },
        {
          key: 'divisions',
          label: <Link to="/settings/divisions">Divisions</Link>
        },
        {
          key: 'types',
          label: <Link to="/settings/types">Types</Link>
        },
        {
          key: 'categories',
          label: <Link to="/settings/categories">Categories</Link>
        },
        {
          key: 'goal-preferences',
          label: <Link to="/settings/goal-preferences">Goal Preferences</Link>
        },
        {
          key: 'tags',
          label: <Link to="/settings/tags">Tags</Link>
        },
      ],
    },
  ];
};

export default createMenuItems;
