import React from 'react';

export default function ServiceList({ services }) {
  const restart = svc => {
    fetch(`/action/${svc}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: 'restart' })
    });
  };

  return (
    <div className="mb-4">
      <h2 className="text-xl font-bold">Services</h2>
      <ul className="space-y-1">
        {services.map(s => (
          <li key={s} className="flex justify-between">
            <span>{s}</span>
            <button onClick={() => restart(s)} className="text-blue-500">Restart</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
