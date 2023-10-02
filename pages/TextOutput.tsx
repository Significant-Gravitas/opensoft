import React from 'react';

interface CodeBlockProps {
  code: string;
}

const CodeBlock: React.FC<CodeBlockProps> = ({ code }) => (
  <pre style={{ background: '#f5f5f5', padding: '10px', borderRadius: '5px' }}>
    <code>{code}</code>
  </pre>
);

interface ChatGPTTextProps {
  text: string;
}

const ChatGPTText: React.FC<ChatGPTTextProps> = ({ text }) => {
  const sections = text.split('```');

  return (
    <div style={{ fontFamily: 'Arial, sans-serif', padding: '10px' }}>
      {sections.map((section, index) => {
        if (index % 2 === 1) {
          return <CodeBlock key={index} code={section.trim()} />;
        }
        return <p key={index}>{section}</p>;
      })}
    </div>
  );
};

export default ChatGPTText;
