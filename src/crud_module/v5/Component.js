import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

function Component() {
    const [modules, setModules] = useState([]);

    useEffect(() => {
        // Fetch all the modules from the backend when component mounts
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
        <div>
            <h2>Modules</h2>
            <ul>
                {modules.map(module => (
                    <li key={module.name}>
                        <Link to={`/${module.name}/${module.version}`}>{`${module.name}/${module.version}`}</Link>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Component;
