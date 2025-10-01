import axios from 'axios';

const api = axios.create({
    baseURL: '/api/auth', // Vite proxy перенаправить це на http://localhost:8000
});

export const sendCode = (phone) => {
    return api.post('/send-code', { phone });
};

export const verifyCode = (phone, code) => {
    return api.post('/verify-code', { phone, code });
};

export const verify2FA = (phone, password) => {
    return api.post('/verify-2fa', { phone, password });
};