import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';

type Module = {
  name: string;
  version: string;
  backend: string;
};

function ModuleList() {
  const router = useRouter();
  const { name, version, backend } = router.query;

  const [currentModule, setCurrentModule] = useState<{
    name: string | null;
    version: string | null;
  }>({
    name: null,
    version: null,
  });

  useEffect(() => {
    if (name && version) {
      setCurrentModule({ name, version });
      // Optionally, update backend state here too if it changes.
    }
  }, [name, version, backend]);

  const [modules, setModules] = useState<Module[]>([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/v3/b1/modules/')
      .then((response) => response.json())
      .then((data) => {
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
                query: {
                  name: module.name,
                  version: module.version,
                  backend: module.backend,
                },
              }}
            >
              <span
                onClick={(e) => {
                  e.preventDefault();
                  // Directly update the URL here
                  router.push(
                    {
                      pathname: '/',
                      query: {
                        name: module.name,
                        version: module.version,
                        backend: module.backend,
                      },
                    },
                    undefined,
                    { shallow: true },
                  );
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
