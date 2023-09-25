import React, { Suspense } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import CrudModuleV1 from "./crud_module_/v1/CrudModuleV1";
import { useParams } from "react-router-dom";

function toCamelCase(str) {
    return str
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join('');
}


function ModuleDetail() {
    const { moduleName } = useParams();

    // Convert moduleName to CamelCase for the component's name
    const componentName = toCamelCase(moduleName);
    // Form the dynamic path
    const componentPath = `./${moduleName}/${componentName}`;

    const DynamicComponent = React.lazy(() => import(`${componentPath}`));

    return (
        <Suspense fallback={<div>Loading...</div>}>
            <DynamicComponent />
        </Suspense>
    );
}



function App() {
    return (
        <Router>
            <div style={{ display: "flex", flexDirection: "column", height: "100vh" }}>
                <h1>Feedback App</h1>
                <div style={{ display: "flex", flexGrow: 1 }}>
                    <div style={{ flexBasis: "30%", overflowY: "auto" }}>
                        <CrudModuleV1 />
                    </div>
                    <div style={{ flexBasis: "70%", overflowY: "auto", borderLeft: "1px solid #ddd" }}>
                        <Routes>
                            <Route path="/:moduleName" element={<ModuleDetail />} />
                        </Routes>
                    </div>
                </div>
            </div>
        </Router>
    );
}


export default App;
