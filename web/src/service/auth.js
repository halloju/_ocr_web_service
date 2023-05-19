import axios from 'axios';

export async function initializeClient() {
    try {
        const response = await axios.get('/auth/refresh_token');
        const accessToken = response.data.access_token;
        const apiClient = axios.create({
            timeout: 1000,  // Replace this with your actual timeout
            headers: { Authorization: `Bearer ${accessToken}` }
        });
        return apiClient;
    } catch (err) {
        console.error(err);
    }
    return null;
}
