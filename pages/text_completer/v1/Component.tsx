import React, { useState } from 'react';
import ChatGPTText from '../../TextOutput'; // Assuming it's in the same directory. Adjust the import path if needed.

function Component() {
  const [inputText, setInputText] = useState<string>('');
  const [completionText, setCompletionText] = useState<string>('');
  const [error, setError] = useState<string | null>(null);

  const handleKeyPress = async (event: React.KeyboardEvent) => {
    if (event.key === 'Enter') {
      createTextCompletion();
    }
  };

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputText(event.target.value);
  };

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
            input: inputText,
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
      <button onClick={createTextCompletion}>Create Text Completion</button>
      <input
        type="text"
        aria-label="chat input"
        placeholder="Type your message here..."
        onKeyPress={handleKeyPress}
        onChange={handleChange}
        value={inputText}
      />
      <ChatGPTText text={completionText} />{' '}
      {/* This line is the change where we use ChatGPTText */}
    </div>
  );
}

export default Component;
