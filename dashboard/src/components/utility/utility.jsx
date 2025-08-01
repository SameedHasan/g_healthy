import { Outlet } from "react-router-dom";
import Dashboard from "../dashboard/Dashboard";
import DynamicTable from "../tables/DynamicTable";

export const convertToRoutes = (menuItems) => {
  return menuItems
    ?.sort((a, b) => a.sequence_number - b.sequence_number)
    ?.map((menu) => {
      const basePath = menu.path || '';
      const route = {
        path: basePath,
        page_view: menu?.page_view,
      };

      if (menu.page_view === "Menu" && Array.isArray(menu.subRoutes) && menu.subRoutes.length > 0) {
        route.element = <Outlet />;
        route.children = menu.subRoutes.map((sub) => ({
          path: (sub.path || sub.key || sub.name || "").toLowerCase(),
          element: <DynamicTable page={sub} dataType={sub?.page || ""} />
        }));
      } else if (menu.page_view === "List" || menu.page_view === "list") {
        route.element = <DynamicTable page={menu} dataType={menu?.page } />;
      } else if (menu.page_view === "Dashboard") {
        route.element = <Dashboard />;
      }

      return route;
    })
    .filter(Boolean); // in case you ever want to skip bad configs
};
