type TextInputProps = {
  value: string;
  onChange?: (value: string) => void;
};

const TextInput: React.FC<TextInputProps> = ({ value, onChange }) => {
  return (
    <textarea
      value={value}
      onChange={(e) => onChange && onChange(e.target.value)}
      style={{
        whiteSpace: 'pre-line',
        width: '100%', // Expand to full width of parent
        height: '100%', // Expand to full height of parent
        border: '1px solid #ccc',
        padding: '8px',
        borderRadius: '4px',
        resize: 'both', // Allow resizing in both directions
        boxSizing: 'border-box', // Include padding and border in element's total width and height
      }}
    />
  );
};

export default TextInput;
