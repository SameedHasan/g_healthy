import { create } from "zustand";
import React from "react";

// Routes store
export const useRoutesStore = create((set, get) => ({
	// State
	routes: [],
	isLoading: false,
	error: null,
	isInitialized: false,

	// Actions
	setRoutes: (routes) => set({ routes, isInitialized: true }),

	setLoading: (isLoading) => set({ isLoading }),

	setError: (error) => set({ error }),

	clearError: () => set({ error: null }),

	// Update routes from external source (like useFrappeGetCall)
	updateRoutesFromAPI: (data, isLoading, error) => {
		set({
			routes: data?.message || [],
			isLoading,
			error,
			isInitialized: !isLoading && !error && data?.message,
		});
	},

	// Get routes by type
	getRoutesByType: (pageView) => {
		const { routes } = get();
		return routes.filter((route) => route.page_view === pageView);
	},

	// Get route by path
	// Inside your zustand store
	getRouteByPath: (path) => {
		const { routes } = get();

		// Exact match on top-level route
		const directMatch = routes.find((route) => route.path === path);
		if (directMatch) return directMatch;

		// Split the path like '/logs/weight' => ['logs', 'weight']
		const segments = path.split("/").filter(Boolean);
		if (segments.length !== 2) return null; // Only support one level deep

		const [parentPath, subPath] = segments;
		const parentRoute = routes.find((route) => route.path === `/${parentPath}`);
		if (!parentRoute || !parentRoute.subRoutes) return null;

		const childRoute = parentRoute.subRoutes.find((sub) => sub.path === subPath);

		if (!childRoute) return null;

		// Optionally return merged info or include parent reference
		return {
			...childRoute,
			parent: parentRoute,
		};
	},

	// Get menu routes (with subroutes)
	getMenuRoutes: () => {
		const { routes } = get();
		return routes.filter((route) => route.page_view === "Menu");
	},

	// Get list routes
	getListRoutes: () => {
		const { routes } = get();
		return routes.filter((route) => route.page_view === "list");
	},

	// Get dashboard routes
	getDashboardRoutes: () => {
		const { routes } = get();
		return routes.filter((route) => route.page_view === "Dashboard");
	},

	getAllRoutes: () => {
		const { routes } = get();
		return routes;
	},
	// Reset store
	reset: () =>
		set({
			routes: [],
			isLoading: false,
			error: null,
			isInitialized: false,
		}),
}));

// Custom hook for using routes store with useFrappeGetCall
export const useRoutes = () => {
	const store = useRoutesStore();

	return store;
};
