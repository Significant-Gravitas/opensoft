import React, { useState } from 'react';

function Component() {
  const [completionText, setCompletionText] = useState<string>('');

  const createTextCompletion = async () => {
    try {
      const response = await fetch(
        'http://localhost:8000/v1/b1/text_completions/',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            input: "What's the capital of America?",
          }),
        },
      );

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setCompletionText(data.output);
    } catch (error) {
      console.error('Error creating text completion:', error);
    }
  };

  return (
    <div>
      <button>Create Text Completion</button>
      <input
        type="text"
        aria-label="chat input"
        placeholder="Type your message here..."
      />
      {/* Any other UI elements */}
    </div>
  );
}

export default Component;
