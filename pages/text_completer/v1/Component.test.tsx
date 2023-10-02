import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import Component from './Component';

const mockFetchResponse = {
  ok: true,
  json: () => Promise.resolve({ output: 'Washington D.C.' }),
};

// Mocking the global fetch function
global.fetch = jest.fn().mockResolvedValue(mockFetchResponse);

beforeEach(() => {
  jest.clearAllMocks();
});

describe('TextCompletionButton Component', () => {
  const inputContent = 'Sample query';
  const expectedFetchParams = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      input: inputContent,
    }),
  };

  it('should hit the /text_completions endpoint when clicked', async () => {
    render(<Component />);

    const chatBar = screen.getByRole('textbox', { name: /chat input/i });
    fireEvent.change(chatBar, { target: { value: inputContent } });

    const button = screen.getByText('Create Text Completion');
    fireEvent.click(button);

    await screen.findByText('Washington D.C.');

    expect(global.fetch).toHaveBeenCalledWith(
      'http://localhost:8000/v1/b1/text_completions/',
      expectedFetchParams,
    );
  });

  it('should render chat bar at the bottom and allow submission with Enter key', async () => {
    render(<Component />);

    const chatBar = screen.getByRole('textbox', { name: /chat input/i });
    fireEvent.change(chatBar, { target: { value: inputContent } });
    fireEvent.keyPress(chatBar, { key: 'Enter', charCode: 13 });

    await waitFor(() => screen.getByText('Washington D.C.'));

    expect(global.fetch).toHaveBeenCalledWith(
      'http://localhost:8000/v1/b1/text_completions/',
      expectedFetchParams,
    );
  });
});

afterEach(() => {
  jest.clearAllMocks();
});
