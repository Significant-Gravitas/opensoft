import React, { useState } from "react";

const FeedbackForm = () => {
    const [content, setContent] = useState("");
    const [message, setMessage] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();

        const response = await fetch("http://127.0.0.1:8000/feedback/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                user_id: 1,  // For simplicity, assuming user_id as 1
                content: content,
            }),
        });

        if (response.ok) {
            setMessage("Feedback submitted successfully!");
        } else {
            const data = await response.json();
            if (typeof data.detail === 'object') {
                setMessage(JSON.stringify(data.detail));
            } else {
                setMessage(data.detail || "Error occurred while submitting feedback");
            }
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <label>
                    Feedback:
                    <textarea
                        value={content}
                        onChange={(e) => setContent(e.target.value)}
                    />
                </label>
                <button type="submit">Submit</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
};

export default FeedbackForm;
