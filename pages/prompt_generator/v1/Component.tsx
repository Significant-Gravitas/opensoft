import React, { useState, useEffect, FormEvent } from 'react';
import TextInput from '../../TextInput'; // Update the path as needed

type Module = {
  name: string;
  version: string;
  backend: string;
};

const Component: React.FC = () => {
  const [moduleBackend, setModuleBackend] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [promptResponse, setPromptResponse] = useState<string | null>(null);
  const [selectedModule, setSelectedModule] = useState<Module | null>(null);
  const [loadingModules, setLoadingModules] = useState(false);
  const [modulesState, setModulesState] = useState<Module[]>([]);

  useEffect(() => {
    if (selectedModule) {
      setModuleBackend(
        `${selectedModule.name}/${selectedModule.version}/${selectedModule.backend}`,
      );
    }
  }, [selectedModule]);

  useEffect(() => {
    const fetchModules = async () => {
      setLoadingModules(true);
      try {
        const response = await fetch('http://127.0.0.1:8000/v1/b1/modules/');
        if (response.ok) {
          const fetchedModules: Module[] = await response.json();
          setModulesState(fetchedModules);
        } else {
          setMessage('Error fetching modules.');
        }
      } catch (error) {
        setMessage('Error fetching modules.');
      } finally {
        setLoadingModules(false);
      }
    };

    fetchModules();
  }, []);

  useEffect(() => {
    if (modulesState.length) {
      setSelectedModule(modulesState[0]);
    }
  }, [modulesState]);

  const handleSelectModule = (moduleIdentifier: string) => {
    const [name, version, backend] = moduleIdentifier.split('-');
    const foundModule = modulesState.find(
      (module) =>
        module.name === name &&
        module.version === version &&
        module.backend === backend,
    );
    if (foundModule) {
      setSelectedModule(foundModule);
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    if (!moduleBackend) return;

    const response = await fetch('http://127.0.0.1:8000/v1/b1/prompts', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        module_backend: moduleBackend,
        goal: 'pass_tests',
      }),
    });

    if (response.ok) {
      const data = await response.json();
      setMessage('Prompt created successfully!');
      setPromptResponse(data.prompt);
      setModuleBackend(null);
    } else {
      const data = await response.json();
      setMessage(data.detail || 'Error occurred while creating prompt');
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <form
        onSubmit={handleSubmit}
        style={{ width: '300px', textAlign: 'center', flexShrink: 0 }} // Prevent form from shrinking
      >
        <label>
          Module Backend:
          {loadingModules ? (
            <div>Loading...</div>
          ) : (
            <select
              value={
                selectedModule
                  ? `${selectedModule.name}-${selectedModule.version}-${selectedModule.backend}`
                  : ''
              }
              onChange={(e) => handleSelectModule(e.target.value)}
              style={{ width: '100%', marginTop: '10px', marginBottom: '10px' }}
            >
              {modulesState.map((module) => (
                <option
                  key={`${module.name}-${module.version}-${module.backend}`}
                  value={`${module.name}-${module.version}-${module.backend}`}
                >
                  {`${module.name}/${module.version}/${module.backend}`}
                </option>
              ))}
            </select>
          )}
        </label>
        <button type="submit">pass_tests</button>
      </form>
      {message && <div style={{ flexShrink: 0 }}>{message}</div>}
      {promptResponse && (
        <div style={{ flex: 1, overflow: 'auto' }}>
          {' '}
          {/* Make this div grow and fill space */}
          <TextInput value={promptResponse} />
        </div>
      )}
    </div>
  );
};

export default Component;
