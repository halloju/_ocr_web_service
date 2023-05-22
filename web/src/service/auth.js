import axios from 'axios';
import { API_TIMEOUT } from '@/constants.js';

export async function initializeClient() {
    try {
        const response = await axios.get('/auth/refresh_token');
        const accessToken = response.data.access_token;
        const apiClient = axios.create({
            timeout: API_TIMEOUT,
            headers: { Authorization: `Bearer ${accessToken}` }
        });
        return apiClient;
    } catch (err) {
        console.error(err);
    }
    return null;
}
