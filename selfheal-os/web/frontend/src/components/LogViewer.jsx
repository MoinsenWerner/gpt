import React from 'react';

export default function LogViewer({ log }) {
  return (
    <div>
      <h2 className="text-xl font-bold">Logs</h2>
      <pre className="bg-gray-200 dark:bg-gray-800 p-2 overflow-auto h-64">{log.join('\n')}</pre>
    </div>
  );
}
