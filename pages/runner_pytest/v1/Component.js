import React, { useState } from 'react';

const PytestFailures = () => {
    const [testPath, setTestPath] = useState("");
    const [testNumber, setTestNumber] = useState(0);
    const [message, setMessage] = useState("");
    const [testResult, setTestResult] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();

        const response = await fetch(`http://127.0.0.1:8000/v2/b1/pytest_failures?n=${testNumber}&path=${testPath}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        });

        if (response.ok) {
            const data = await response.json();
            if(data) {
                setMessage("Test result retrieved successfully!");
                setTestResult(data);
            } else {
                setMessage("No failure found for the given test number in the specified path.");
                setTestResult("");
            }
        } else {
            const data = await response.json();
            setMessage(data.detail || "Error occurred while retrieving test result");
            setTestResult("");
        }
    };

    return (
        <div style={{
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            minHeight: '100vh'
        }}>
            <h2>Pytest Failures</h2>
            <form onSubmit={handleSubmit} style={{ width: '300px', textAlign: 'center', marginBottom: '20px' }}>
                <label>
                    Test File Path:
                    <input
                        type="text"
                        value={testPath}
                        onChange={(e) => setTestPath(e.target.value)}
                        style={{ width: '100%', marginTop: '10px', marginBottom: '10px' }}
                    />
                </label>
                <label>
                    Test Number (n):
                    <input
                        type="number"
                        value={testNumber}
                        onChange={(e) => setTestNumber(e.target.value)}
                        style={{ width: '100%', marginTop: '10px', marginBottom: '10px' }}
                    />
                </label>
                <button type="submit">Retrieve Test Failure</button>
            </form>
            {message && <p>{message}</p>}
            {testResult && (
                <div style={{ textAlign: 'center', width: '100%', overflowX: 'scroll' }}>
                    <pre style={{ display: 'inline-block', textAlign: 'left' }}>{testResult}</pre>
                </div>
            )}
        </div>
    );
};

export default PytestFailures;
