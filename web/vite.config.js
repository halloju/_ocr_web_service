import { fileURLToPath, URL } from 'url';

import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

// https://vitejs.dev/config/
export default defineConfig({
    base: '/',
    plugins: [vue()],
    resolve: {
        extentions: ['.vue', '.js', '.json', '.mjs'],
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url)),
            '/images': './src/assets/images'
        }
    },
    server: {
        host: '0.0.0.0',
        port: 3000
    },
    build: {
        chunkSizeWarningLimit: 1500,
        rollupOptions: {
            output: {
                manualChunks(id) {
                    if (id.includes('node_modules')) {
                        return id.toString().split('node_modules/')[1].split('/')[0].toString();
                    }
                },
                // entryFileNames: 'assets/[name].js',
                // chunkFileNames: 'assets/[name].js',
                assetFileNames: ({ name }) => {
                    console.log(name);
                    if (/\.(gif|jpe?g|png|svg)$/.test(name ?? '')) {
                        return 'assets/images/[name][extname]';
                    }
                    if (/\.css$/.test(name ?? '')) {
                        return 'assets/css/[name]-[hash][extname]';
                    }
                    // default value
                    // ref: https://rollupjs.org/guide/en/#outputassetfilenames
                    return 'assets/[name]-[hash][extname]';
                }
            }
        }
    }
});
