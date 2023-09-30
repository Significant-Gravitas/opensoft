import React, { useState, useEffect } from 'react';
import Link from 'next/link'; // Use Next.js's Link component

type Module = {
  name: string;
  version: string;
  backend: string; // Add the backend property
};



function ModuleList({ onModuleChange }: { onModuleChange: (name: string, version: string, backend: string) => void }) {
  const [modules, setModules] = useState<Module[]>([]);

  useEffect(() => {
    // Fetch all the modules from the backend when component mounts
    fetch('http://127.0.0.1:8000/v1/b1/modules/')
      .then((response) => response.json())
      .then((data) => {
        setModules(data);
      })
      .catch((error) => {
        console.error('There was an error fetching the modules', error);
      });
  }, []);

  return (
    <div>
      <h2>Modules</h2>
      <ul>
        {modules.map((module) => (
          <li key={module.name}>
            <Link
              href={{
                pathname: '/',
                query: { name: module.name, version: module.version, backend: module.backend }
              }}
            >
              <span
                onClick={(e) => {
                  e.preventDefault();
                  onModuleChange(module.name, module.version, module.backend);
                }}
                style={{ cursor: 'pointer' }}
              >
                {`${module.name}/${module.version}/${module.backend}`}
              </span>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ModuleList;
