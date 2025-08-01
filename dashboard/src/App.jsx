import React, { useEffect } from "react";
import { ConfigProvider, Spin } from "antd";
import { BrowserRouter } from "react-router-dom";
import MainLayout from "./components/layout/MainLayout";
import RenderRoutes from "./components/utility/renderRoutes";
import theme from "./themes/theme.json";
import "../styles/fonts.css";
import "./App.css";
import AuthGate from "./components/auth/AuthGate";
import { useRoutesStore } from "./store";
import { useFrappeAuth, useFrappeGetCall } from "frappe-react-sdk";
import { convertToRoutes } from "./components/utility/utility.jsx";

function App() {
const { currentUser } = useFrappeAuth();
  const { data, error, isLoading } = useFrappeGetCall(
    "g_healthy.g_healthy.doctype.routes.api.get_parent_and_child_data",
    {},
    currentUser ? currentUser.name:false
  );



  const { routes, updateRoutesFromAPI } = useRoutesStore();

  // Sync API data with Zustand store
  useEffect(() => {
    updateRoutesFromAPI(data, isLoading, error);
  }, [data, isLoading, error, updateRoutesFromAPI]);

  if (isLoading) {
    return (
      <Spin
        size="large"
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "100vh",
        }}
      />
    );
  }

  if (error) {
    return (
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "100vh",
          flexDirection: "column",
        }}
      >
        <h2>Error Loading Routes</h2>
        <p>{error}</p>
        <button onClick={() => window.location.reload()}>Retry</button>
      </div>
    );
  }

  return (
    <ConfigProvider theme={theme}>
      <BrowserRouter basename="/dashboard">
        <AuthGate>
          <MainLayout theme={theme} routesData={routes}>
            <RenderRoutes routes={convertToRoutes(routes||[])} />
          </MainLayout>
        </AuthGate>
      </BrowserRouter>
    </ConfigProvider>
  );
}

export default App;
