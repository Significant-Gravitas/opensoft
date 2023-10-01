// components/BackendSelector.tsx

import React, { useState, useEffect } from 'react';
import { render, fireEvent } from '@testing-library/react';
import { useRouter } from 'next/router';
import { createMemoryHistory } from 'history';

interface BackendSelectorProps {
  moduleName: string | null;
  onBackendSelect: (backend: string) => void;
}

const BackendSelector: React.FC<BackendSelectorProps> = ({
  moduleName,
  onBackendSelect,
}) => {
  const router = useRouter();
  const [backends, setBackends] = useState<string[]>([]);
  const [selectedBackend, setSelectedBackend] = useState<string | null>('b1'); // Initialize with b1

  useEffect(() => {
    if (moduleName) {
      fetchBackendsForModule(moduleName).then((data) => {
        setBackends(data);

        // If b1 is in the list of backends, preselect it
        if (data.includes('b1')) {
          setSelectedBackend('b1');
          onBackendSelect('b1');

          router.push({
            pathname: router.pathname,
            query: { ...router.query, backend: 'b1' },
          });
        } else {
          setSelectedBackend(null);
        }
      });
    }
  }, [moduleName]);

  const fetchBackendsForModule = async (moduleName: string) => {
    const response = await fetch(
      `http://localhost:8000/v3/b1/modules?name=${moduleName}`,
    );
    const data = await response.json();

    // Extract backends and deduplicate using a Set
    const uniqueBackends = [...new Set(data.map((item) => item.backend))];

    return uniqueBackends;
  };

  const handleBackendClick = (backend: string) => {
    console.log('handleBackendClick called with:', backend);
    setSelectedBackend(backend);
    onBackendSelect(backend);

    router.push({
      pathname: router.pathname,
      query: { ...router.query, backend },
    });
  };

  return (
    <div>
      {backends.map((backend) => (
        <button
          key={backend}
          onClick={() => handleBackendClick(backend)}
          style={{
            backgroundColor:
              backend === selectedBackend ? 'blue' : 'transparent', // Change color when selected
            color: backend === selectedBackend ? 'white' : 'black', // Adjust text color
            margin: '5px',
          }}
        >
          {backend}
        </button>
      ))}
    </div>
  );
};

export default BackendSelector;
