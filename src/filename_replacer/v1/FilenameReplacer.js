import React, { useState } from "react";

const FilenameReplacer = () => {
    const [moduleTargets, setModuleTargets] = useState(["fixture_to_remove"]);
    const [filenameSearch, setFilenameSearch] = useState("xyz");
    const [filenameReplacement, setFilenameReplacement] = useState("def");
    const [message, setMessage] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();

        const response = await fetch("http://127.0.0.1:8000/v1/filename_replacement", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                module_names: moduleTargets,
                filename_contains: filenameSearch,
                replace_with: filenameReplacement,
            }),
        });

        if (response.ok) {
            const data = await response.json();
            setMessage("Filename replaced successfully!");
        } else {
            const data = await response.json();
            setMessage(data.detail || "Error occurred while replacing filename");
        }
    };

    return (
        <div style={{
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            height: '100vh'
        }}>
            <form onSubmit={handleSubmit} style={{ width: '300px', textAlign: 'center' }}>
                <label>
                    Module Targets (comma separated):
                    <input
                        type="text"
                        value={moduleTargets}
                        onChange={(e) => setModuleTargets(e.target.value.split(','))}
                        style={{ width: '100%', marginTop: '10px', marginBottom: '10px' }}
                    />
                </label>
                <label>
                    Filename Search:
                    <input
                        type="text"
                        value={filenameSearch}
                        onChange={(e) => setFilenameSearch(e.target.value)}
                        style={{ width: '100%', marginTop: '10px', marginBottom: '10px' }}
                    />
                </label>
                <label>
                    Filename Replacement:
                    <input
                        type="text"
                        value={filenameReplacement}
                        onChange={(e) => setFilenameReplacement(e.target.value)}
                        style={{ width: '100%', marginTop: '10px', marginBottom: '10px' }}
                    />
                </label>
                <button type="submit">Replace</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
};

export default FilenameReplacer;
