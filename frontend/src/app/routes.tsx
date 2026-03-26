import { createBrowserRouter, Navigate } from "react-router";
import { Layout } from "./components/Layout";
import { Login } from "./pages/Login";
import { Dashboard } from "./pages/Dashboard";
import { Devices } from "./pages/Devices";
import { Schedule } from "./pages/Schedule";
import { Settings } from "./pages/Settings";

// Protected route wrapper - checks auth each time
const ProtectedLayout = () => {
  const token = localStorage.getItem("token");
  return token ? <Layout /> : <Navigate to="/login" replace />;
};

export const router = createBrowserRouter([
  {
    path: "/login",
    Component: Login,
  },
  {
    path: "/",
    Component: ProtectedLayout,
    children: [
      { index: true, Component: Dashboard },
      { path: "devices", Component: Devices },
      { path: "schedule", Component: Schedule },
      { path: "settings", Component: Settings },
    ],
  },
]);