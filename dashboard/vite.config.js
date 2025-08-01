import path from "path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import proxyOptions from "./proxyOptions";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 8080,
    proxy: proxyOptions,
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
  build: {
    outDir: "../g_healthy/public/dashboard",
    emptyOutDir: true,
    target: "es2015",
    chunkSizeWarningLimit: 8000,

    // Reduce memory usage
    minify: "esbuild", 
    sourcemap: false, 
    cssCodeSplit: true,
  },
});
