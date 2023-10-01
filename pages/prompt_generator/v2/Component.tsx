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
  const [modulesState, setModulesState] = useState<Module[]>([]);

  useEffect(() => {
    if (selectedModule) {
      setModuleBackend(
        `${selectedModule.name}/${selectedModule.version}/${selectedModule.backend}`,
      );
    }
  }, [selectedModule]);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const name = params.get('name') || '';
    const version = params.get('version') || '';
    const backend = params.get('backend') || '';

    if (name && version && backend) {
      setSelectedModule({
        name,
        version,
        backend,
      });
    } else {
      setMessage('Invalid module details in URL.');
    }
  }, []);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    // Clear previous message and prompt response
    setMessage(null);
    setPromptResponse(null);

    if (!moduleBackend) return;

    const response = await fetch('http://127.0.0.1:8000/v2/b1/prompts', {
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
    } else {
      const data = await response.json();
      setMessage(data.detail || 'Error occurred while creating prompt');
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <form
        onSubmit={handleSubmit}
        style={{ width: '300px', textAlign: 'center', flexShrink: 0 }}
      >
        <p>
          Module Backend:
          {selectedModule
            ? `${selectedModule.name}/${selectedModule.version}/${selectedModule.backend}`
            : 'Loading...'}
        </p>
        <button type="submit">pass_tests</button>
      </form>
      {message && <div style={{ flexShrink: 0 }}>{message}</div>}
      {promptResponse && (
        <div style={{ flex: 1, overflow: 'auto' }}>
          <TextInput value={promptResponse} />
        </div>
      )}
    </div>
  );
};

export default Component;
