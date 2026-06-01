import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// base: './' keeps asset paths relative, so the built site works whether you open
// it locally or host it under a subpath (e.g. a GitHub Pages project page).
export default defineConfig({
  plugins: [react()],
  base: './',
});
