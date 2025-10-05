import React, { useState } from 'react';

const PhoneForm = ({ onSubmit, loading }) => {
    const [phone, setPhone] = useState('');
    const [error, setError] = useState('');

    const validatePhone = (value) => {
        const phoneRegex = /^\+\d{10,15}$/;
        return phoneRegex.test(value);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!validatePhone(phone)) {
            setError('Введіть правильний номер телефону у форматі +XXXXXXXXXXXX');
            return;
        }
        setError('');
        onSubmit(phone);
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Введіть номер телефону</h2>
            <p>Включаючи код країни (наприклад, +380991234567)</p>
            <input
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="+380991234567"
                required
                disabled={loading}
                className={error ? 'input-error' : ''}
            />
            {error && <p className="error-message">{error}</p>}
            <button type="submit" disabled={loading}>
                {loading ? 'Надсилання...' : 'Надіслати код'}
            </button>
        </form>
    );
};

export default PhoneForm;
