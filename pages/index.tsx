import React, { Suspense, useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import dynamic from 'next/dynamic';
import ModuleList from './crud_module/v5/Component';
import PromptGenerator from './prompt_generator/v3/Component';

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
  };
}

interface ModuleListProps {
  onModuleChange: (moduleName: string, version: string) => void;
}
function ModuleDetail({ moduleDetail }: ModuleDetailProps) {
  const router = useRouter();
  const { name: moduleName, version } = moduleDetail;

  if (!moduleName || !version) {
    return <div>Invalid module or version</div>;
  }

  const DynamicComponent = dynamic(
    () =>
      import(
        `./${moduleName || 'defaultModule'}/${version || 'defaultVersion'}/Component`
      ),
  ); // add a default module and version if required

  return (
    <Suspense fallback={<div>Loading...</div>}>
      <DynamicComponent />
    </Suspense>
  );
}

function App() {
  const router = useRouter();
  const { name, version } = router.query;

  useEffect(() => {
    if (name && version) {
      setCurrentModule({ name, version });
    }
  }, [name, version]);

  const handleModuleChange = (
    moduleName: string,
    version: string,
    backend: string,
  ) => {
    setCurrentModule({ name: moduleName, version });

    // Use shallow routing to change the URL without running data fetching methods again
    router.push(
      {
        pathname: '/',
        query: { name: moduleName, version, backend },
      },
      undefined,
      { shallow: true },
    );
  };

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
          <ModuleList onModuleChange={handleModuleChange} />
        </div>
        <div
          style={{
            flex: '0 0 70%',
            overflowY: 'auto',
            borderLeft: '1px solid #ddd',
          }}
        >
          <ModuleDetail moduleDetail={currentModule} />
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
