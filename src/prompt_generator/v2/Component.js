import React, { useState, useRef, useEffect } from "react";

const PromptCreation = () => {
    const [moduleBackend, setModuleBackend] = useState("");
    const [goal, setGoal] = useState("");
    const [message, setMessage] = useState("");
    const [promptResponse, setPromptResponse] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();

        const response = await fetch("http://127.0.0.1:8000/v1/b1/prompts", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                module_backend: moduleBackend,
                goal: goal
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
            ref={componentRef}
            style={{
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'flex-start',
                alignItems: 'center',
                minHeight: '100vh',
                marginLeft: '20px',
                overflowY: 'auto',
                width: '100%',  // Added this line
            }}>
            <form onSubmit={handleSubmit} style={{ width: '300px', textAlign: 'center' }}>
                <label>
                    Module Backend:
                    <input
                        type="text"
                        value={moduleBackend}
                        onChange={(e) => setModuleBackend(e.target.value)}
                        style={{ width: '100%', marginTop: '10px', marginBottom: '10px' }}
                    />
                </label>
                <label>
                    Goal:
                    <input
                        type="text"
                        value={goal}
                        onChange={(e) => setGoal(e.target.value)}
                        style={{ width: '100%', marginTop: '10px', marginBottom: '10px' }}
                    />
                </label>
                <button type="submit">Create Prompt</button>
            </form>
            {message && <p>{message}</p>}
            {promptResponse && (
            <div ref={componentRef} style={{ textAlign: 'center', width: '100%' }}>
                <pre style={{ display: 'inline-block', textAlign: 'left' }}>{promptResponse}</pre>
            </div>
        )}

        </div>
    );
};

export default PromptCreation;
