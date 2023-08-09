import axios from 'axios';
import { API_TIMEOUT } from '@/constants.js';

let isRefreshing = false;
let failedQueue = [];


export const apiClient = axios.create({
    timeout: API_TIMEOUT
});


const processQueue = (error, token = null) => {
    failedQueue.forEach(prom => {
        if (error) {
            prom.reject(error);
        } else {
            prom.resolve(token);
        }
    });

    failedQueue = [];
};

apiClient.interceptors.response.use(
    response => {
        return response;
    },
    error => {
        const originalRequest = error.config;
        if (error.response.status === 401 && !originalRequest._retry) {
            if (isRefreshing) {
                return new Promise(function(resolve, reject) {
                    failedQueue.push({resolve, reject})
                }).then(token => {
                    originalRequest.headers['Authorization'] = 'Bearer ' + token;
                    return apiClient(originalRequest);
                }).catch(err => {
                    return Promise.reject(err);
                });
            }

            originalRequest._retry = true;
            isRefreshing = true;

            return new Promise(function(resolve, reject) {
                axios.get('/auth/refresh_token')
                    .then(({data}) => {
                        apiClient.defaults.headers.common['Authorization'] = 'Bearer ' + data.access_token;
                        originalRequest.headers['Authorization'] = 'Bearer ' + data.access_token;
                        processQueue(null, data.access_token);
                        resolve(apiClient(originalRequest));
                    })
                    .catch((err) => {
                        processQueue(err, null);
                        reject(err);
                    })
                    .then(() => { isRefreshing = false });
            });
        }
        return Promise.reject(error);
    }
);
