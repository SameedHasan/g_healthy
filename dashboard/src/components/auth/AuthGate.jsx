import React, { useEffect } from "react";
import { useFrappeAuth } from "frappe-react-sdk";
import { useLocation, Navigate } from "react-router-dom";
import LoginForm from "./LoginForm";

const AuthGate = ({ children }) => {
  const { currentUser, isLoading } = useFrappeAuth();
  const location = useLocation();
  if (isLoading) return <div>Loading...</div>;

  // If at /dashboard/login and already logged in, redirect to /dashboard
//   if (location.pathname === "/dashboard/login" && currentUser) {
//     return <Navigate to="/dashboard/logs" replace />;
//   }

  // If at /dashboard/login and not logged in, show login form
  if (location.pathname === "/login") {
    return <LoginForm />;
  }

  // If not logged in, redirect to login
  if (!currentUser && location.pathname !== "/login") {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // If logged in, render the app
  return <>{children}</>;
};

export default AuthGate; 