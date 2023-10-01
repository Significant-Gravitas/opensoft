import React, { useState, useEffect } from 'react';
import Link from 'next/link'; // Use Next.js's Link component

type Module = {
  name: string;
  version: string;
  backend: string; // Add the backend property
};

function ModuleList({
  onModuleChange,
}: {
  onModuleChange: (name: string, version: string, backend: string) => void;
}) {
  const [modules, setModules] = useState<Module[]>([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/v2/b1/modules/')
      .then((response) => response.json())
      .then((data) => {
        // Deduplication logic
        const uniqueModulesMap: { [key: string]: Module } = {};
        const deduplicatedModules: Module[] = [];

        for (const module of data) {
          const key = `${module.name}/${module.version}`;
          if (!uniqueModulesMap[key]) {
            uniqueModulesMap[key] = module;
            deduplicatedModules.push(module);
          }
        }

        setModules(deduplicatedModules);
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
                query: { name: module.name, version: module.version },
              }}
            >
              <span
                onClick={(e) => {
                  e.preventDefault();
                  onModuleChange(module.name, module.version, module.backend);
                }}
                style={{ cursor: 'pointer' }}
              >
                {`${module.name}/${module.version}`}
              </span>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ModuleList;
