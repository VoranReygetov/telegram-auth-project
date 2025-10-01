import React, { useState } from 'react';
import PhoneForm from '../components/PhoneForm';
import CodeForm from '../components/CodeForm';
import TwoFAForm from '../components/TwoFAForm';
import { sendCode, verifyCode, verify2FA } from '../api/auth';
import './LoginPage.css';

const LoginPage = () => {
    const [step, setStep] = useState('phone'); // phone, code, 2fa, success
    const [phone, setPhone] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handlePhoneSubmit = async (phoneNumber) => {
        setLoading(true);
        setError('');
        try {
            await sendCode(phoneNumber);
            setPhone(phoneNumber);
            setStep('code');
        } catch (err) {
            setError(err.response?.data?.detail || 'Не вдалося надіслати код.');
        } finally {
            setLoading(false);
        }
    };

    const handleCodeSubmit = async (code) => {
        setLoading(true);
        setError('');
        try {
            const response = await verifyCode(phone, code);
            if (response.data.message === '2FA password required') {
                setStep('2fa');
            } else if (response.data.access_token) {
                localStorage.setItem('token', response.data.access_token);
                setStep('success');
            }
        } catch (err) {
            setError(err.response?.data?.detail || 'Невірний код.');
        } finally {
            setLoading(false);
        }
    };

    const handle2FASubmit = async (password) => {
        setLoading(true);
        setError('');
        try {
            const response = await verify2FA(phone, password);
            if (response.data.access_token) {
                localStorage.setItem('token', response.data.access_token);
                setStep('success');
            }
        } catch (err) {
            setError(err.response?.data?.detail || 'Невірний 2FA пароль.');
        } finally {
            setLoading(false);
        }
    };

    const renderStep = () => {
        switch (step) {
            case 'phone':
                return <PhoneForm onSubmit={handlePhoneSubmit} loading={loading} />;
            case 'code':
                return <CodeForm onSubmit={handleCodeSubmit} loading={loading} phone={phone} />;
            case '2fa':
                return <TwoFAForm onSubmit={handle2FASubmit} loading={loading} />;
            case 'success':
                return <div className="success-message"><h2>Авторизація успішна!</h2><p>Ваш токен збережено.</p></div>;
            default:
                return null;
        }
    };

    return (
        <div className="login-container">
            <div className="login-box">
                <h1>Вхід через Telegram</h1>
                {error && <p className="error-message">{error}</p>}
                {renderStep()}
            </div>
        </div>
    );
};

export default LoginPage;
