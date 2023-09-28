import React, {Suspense, useEffect, useState} from 'react';
import { BrowserRouter as Router, Route, Routes, useParams } from "react-router-dom";
import CrudModule from "./crud_module/v5/Component";
import PromptGenerator from "./prompt_generator/v3/Component";

function toCamelCase(str) {
    return str
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join('');
}

function ModuleDetail() {
    const { moduleName, version } = useParams();

    if (!moduleName || !version) {
        return <div>Invalid module or version</div>;
    }

    const componentPath = `./${moduleName}/${version}/Component`;

    const DynamicComponent = React.lazy(() => import(`${componentPath}`));

    return (
        <Suspense fallback={<div>Loading...</div>}>
            <DynamicComponent />
        </Suspense>
    );
}

function App() {
    const [modules, setModules] = useState([]);

    useEffect(() => {
        // Fetch the modules when the App component mounts
        fetch('http://127.0.0.1:8000/v5/b1/modules/')
            .then(response => response.json())
            .then(data => {
                setModules(data);
            })
            .catch(error => {
                console.error('There was an error fetching the modules', error);
            });
    }, []);

    return (
        <Router>
            <div style={{ display: "flex", flexDirection: "column", height: "100vh" }}>
                <h1>Iterface</h1>
                <div style={{ display: "flex", flexGrow: 1, flexWrap: 'nowrap', position: 'relative' }}>
                    <div style={{ flex: '0 0 30%', overflowY: "auto" }}>
                        <CrudModule />
                    </div>

                    {/* Component in the center right */}
                    <div style={{ flex: '0 0 70%', overflowY: "auto", borderLeft: "1px solid #ddd" }}>
                        <Routes>
                        <Route path="/:moduleName/:version" element={<ModuleDetail />} />
                        <Route path="*" element={<div>Not Found</div>} />
                    </Routes>

                    </div>
                    <div style={{ position: 'absolute', top: '10px', right: '10px', width: '25%', maxWidth: '400px'}}>
                        <PromptGenerator modules={modules} />
                    </div>
                </div>
            </div>
        </Router>
    );
}

export default App;
