import React, { Suspense, useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import dynamic from 'next/dynamic';
import ModuleList from './crud_module/v3/Component';
import PromptGenerator from './prompt_generator/v2/Component';
import BackendSelector from './BackendSelector';

function toCamelCase(str: string): string {
  return str
    .split('_')
    .map((word: string) => word.charAt(0).toUpperCase() + word.slice(1))
    .join('');
}

interface ModuleDetailProps {
  moduleDetail: {
    name: string | null;
    version: string | null;
    backend: string;
  };
}


function ModuleDetail({ moduleDetail }: ModuleDetailProps) {
  const { name: moduleName, version } = moduleDetail;

  if (!moduleName || !version) {
    return <div>Invalid module or version</div>;
  }

  const DynamicComponent = dynamic(
    () =>
      import(
        `./${moduleName || 'defaultModule'}/${
          version || 'defaultVersion'
        }/Component`
      ),
  ); // add a default module and version if required

  return (
    <Suspense fallback={<div>Loading...</div>}>
      <DynamicComponent />
    </Suspense>
  );
}

function App() {
  const [selectedBackend, setSelectedBackend] = useState<string>('b1');

  const handleBackendSelect = (backend: string) => {
    setSelectedBackend(backend);
    // Update URL or other necessary places with the backend information
    // For instance, you can add it to router.query as done for module name and version
  };

  const router = useRouter();
  const { name, version, backend } = router.query;

  useEffect(() => {
    if (name && version) {
      setCurrentModule({ name, version });
    }
  }, [name, version, backend]); // Added backend to the dependencies

  const [currentModule, setCurrentModule] = useState<{
    name: string | null;
    version: string | null;
  }>({
    name: null,
    version: null,
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <h1>Iterface</h1>
      <div
        style={{
          display: 'flex',
          flexGrow: 1,
          flexWrap: 'nowrap',
          position: 'relative',
        }}
      >
        <div style={{ flex: '0 0 30%', overflowY: 'auto' }}>
          <ModuleList />
        </div>
        <div
          style={{
            flex: '0 0 70%',
            overflowY: 'auto',
            borderLeft: '1px solid #ddd',
            padding: '10px',
          }}
        >
          {currentModule.name && (
            <BackendSelector
              moduleName={currentModule.name}
              onBackendSelect={handleBackendSelect}
            />
          )}
          <ModuleDetail
            moduleDetail={{ ...currentModule, backend: selectedBackend }}
          />
        </div>
        <div
          style={{
            position: 'absolute',
            top: '10px',
            right: '10px',
            width: '25%',
            maxWidth: '400px',
          }}
        >
          <PromptGenerator /> {/* Removed the modules prop */}
        </div>
      </div>
    </div>
  );
}

export default App;
