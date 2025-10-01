import React, { useState } from 'react';

const TwoFAForm = ({ onSubmit, loading }) => {
    const [password, setPassword] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(password);
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Двофакторна автентифікація</h2>
            <p>Будь ласка, введіть ваш 2FA пароль.</p>
            <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Ваш пароль"
                required
                disabled={loading}
            />
            <button type="submit" disabled={loading}>
                {loading ? 'Перевірка...' : 'Увійти'}
            </button>
        </form>
    );
};

export default TwoFAForm;
