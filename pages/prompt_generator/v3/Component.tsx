import React, { useState, useRef, useEffect, FormEvent } from 'react';

type Module = {
  name: string;
  version: string;
  backend: string;
};


type ComponentProps = {
  modules?: Module[];  // Made this optional
};

const Component: React.FC = () => {
  const [moduleBackend, setModuleBackend] = useState('');
  const [, setGoal] = useState('');
  const [, setMessage] = useState('');
  const [, setPromptResponse] = useState('');
  const [selectedModule, setSelectedModule] = useState('');
  const [loadingModules, setLoadingModules] = useState(false);
  const [modulesState, setModulesState] = useState<Module[]>([]);

  // Fetch modules on mount
  useEffect(() => {
    const fetchModules = async () => {
      setLoadingModules(true);
      try {
        const response = await fetch('http://127.0.0.1:8000/v6/b1/modules/');
        if (response.ok) {
          const fetchedModules: Module[] = await response.json();
          setModulesState(fetchedModules);
          if (fetchedModules.length) {
            setSelectedModule(fetchedModules[0].name);
          }
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
      setSelectedModule(modulesState[0].name);
    }
  }, [modulesState]);



  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    const response = await fetch('http://127.0.0.1:8000/v3/b1/prompts', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        module_backend: moduleBackend,
        goal: 'pass_tests', // Set the goal value to "pass_tests" directly.
      }),
    });

    if (response.ok) {
      const data = await response.json();
      setMessage('Prompt created successfully!');
      setPromptResponse(data.prompt);

      // Clear the input states after a successful submission
      setModuleBackend('');
      setGoal('');
    } else {
      const data = await response.json();
      setMessage(data.detail || 'Error occurred while creating prompt');
    }
  };

  const componentRef = useRef(null);

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      const target = event.target as Element; // <-- Cast the target to Element

      if ((event.ctrlKey || event.metaKey) && event.key === 'a') {
        if (
          target.tagName === 'INPUT' || // <-- Use the new target variable
          target.tagName === 'TEXTAREA' // <-- Use the new target variable
        ) {
          return;
        }

        event.preventDefault();

        const selection = window.getSelection();
        if (selection && componentRef.current) {
          // <-- Check if componentRef.current is non-null
          const range = document.createRange();
          range.selectNodeContents(componentRef.current);
          // eslint-disable-next-line prettier/prettier
        selection.removeAllRanges();
          selection.addRange(range);
        }
      }
    };

    document.addEventListener('keydown', handleKeyDown);

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [componentRef.current]);

  return (
    <div>
      <form
        onSubmit={handleSubmit}
        style={{ width: '300px', textAlign: 'center' }}
      >
        <label>
          Module Backend:
          {loadingModules ? (
            <div>Loading...</div>
          ) : (
            <select
              value={selectedModule}
              onChange={(e) => setSelectedModule(e.target.value)}
              style={{ width: '100%', marginTop: '10px', marginBottom: '10px' }}
            >
              {modulesState.map((module) => (
                <option key={module.name} value={`${module.name}/${module.version}/${module.backend}`}>
                  {`${module.name}/${module.version}/${module.backend}`}
                </option>
              ))}
            </select>
          )}
        </label>
        <button type="submit">pass_tests</button>
      </form>
    </div>
  );
};

export default Component;
