import React, { useState } from 'react';

const CodeForm = ({ onSubmit, loading, phone }) => {
    const [code, setCode] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(code);
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Введіть код підтвердження</h2>
            <p>Код було надіслано на ваш Telegram акаунт ({phone}).</p>
            <input
                type="text"
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder="12345"
                required
                disabled={loading}
            />
            <button type="submit" disabled={loading}>
                {loading ? 'Перевірка...' : 'Підтвердити'}
            </button>
        </form>
    );
};

export default CodeForm;
