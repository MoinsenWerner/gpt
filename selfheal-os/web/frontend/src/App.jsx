import React, { useState, useEffect } from 'react';
import ServiceList from './components/ServiceList.jsx';
import LogViewer from './components/LogViewer.jsx';

export default function App() {
  const [usage, setUsage] = useState({});
  const [services, setServices] = useState([]);
  const [log, setLog] = useState([]);
  const [dark, setDark] = useState(false);

  useEffect(() => {
    fetch('/status')
      .then(res => res.json())
      .then(data => {
        setUsage(data.usage || {});
        setServices(data.services || []);
      });
    fetch('/log')
      .then(res => res.json())
      .then(data => setLog(data.log || []));
  }, []);

  const toggleTheme = () => setDark(!dark);

  return (
    <div className={dark ? 'dark bg-gray-900 text-white min-h-screen p-4' : 'bg-white text-gray-900 min-h-screen p-4'}>
      <button onClick={toggleTheme} className="mb-4 px-2 py-1 border rounded">
        Toggle {dark ? 'Light' : 'Dark'} Mode
      </button>
      <div className="mb-4">
        <h1 className="text-2xl font-bold">System Usage</h1>
        <div>CPU: {usage.cpu}% RAM: {usage.ram}% DISK: {usage.disk}%</div>
      </div>
      <ServiceList services={services} />
      <LogViewer log={log} />
    </div>
  );
}
