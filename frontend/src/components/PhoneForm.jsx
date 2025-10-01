import React, { useState } from 'react';

const PhoneForm = ({ onSubmit, loading }) => {
    const [phone, setPhone] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
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
            />
            <button type="submit" disabled={loading}>
                {loading ? 'Надсилання...' : 'Надіслати код'}
            </button>
        </form>
    );
};

export default PhoneForm;
