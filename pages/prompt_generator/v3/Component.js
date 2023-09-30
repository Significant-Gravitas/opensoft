import React, { useState, useRef, useEffect } from "react";

const Component = ({ modules }) => {
    const [moduleBackend, setModuleBackend] = useState("");
    const [goal, setGoal] = useState("");
    const [message, setMessage] = useState("");
    const [promptResponse, setPromptResponse] = useState("");
    const [selectedModule, setSelectedModule] = useState("");

    useEffect(() => {
        if (modules.length) {
            setSelectedModule(modules[0].name);
        }
    }, [modules]);

    const handleSubmit = async (e) => {
        e.preventDefault();

        const response = await fetch("http://127.0.0.1:8000/v3/b1/prompts", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                module_backend: moduleBackend,
                goal: "pass_tests"  // Set the goal value to "pass_tests" directly.
            }),
        });

        if (response.ok) {
            const data = await response.json();
            setMessage("Prompt created successfully!");
            setPromptResponse(data.prompt);

            // Clear the input states after a successful submission
            setModuleBackend("");
            setGoal("");
        } else {
            const data = await response.json();
            setMessage(data.detail || "Error occurred while creating prompt");
        }
    };


    const componentRef = useRef(null);

    useEffect(() => {
        const handleKeyDown = (event) => {
            if ((event.ctrlKey || event.metaKey) && event.key === 'a') {
                if (event.target.tagName === "INPUT" || event.target.tagName === "TEXTAREA") {
                    return; // If the event originates from an input or textarea, just return without doing anything
                }

                event.preventDefault();

                const selection = window.getSelection();
                const range = document.createRange();
                range.selectNodeContents(componentRef.current);
                selection.removeAllRanges();
                selection.addRange(range);
            }
        };

        document.addEventListener('keydown', handleKeyDown);

        return () => {
            // Cleanup the event listener on component unmount
            document.removeEventListener('keydown', handleKeyDown);
        };
    }, []);

    return (
        <div
            // ... existing code ...
        >
            <form onSubmit={handleSubmit} style={{ width: '300px', textAlign: 'center' }}>
                <label>
                    Module Backend:
                    <select
                        value={selectedModule}
                        onChange={(e) => setSelectedModule(e.target.value)}
                        style={{ width: '100%', marginTop: '10px', marginBottom: '10px' }}
                    >
                        {modules.map(module => (
                            <option key={module.name} value={module.name}>
                                {module.name}
                            </option>
                        ))}
                    </select>
                </label>
                <button type="submit">pass_tests</button>
            </form>
            {/* ... rest of the return code ... */}
        </div>
    );
};

export default Component;
