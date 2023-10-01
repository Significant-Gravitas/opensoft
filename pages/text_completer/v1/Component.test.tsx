import React from 'react';
import {
  render,
  screen,
  fireEvent,
  act,
  waitFor,
} from '@testing-library/react';
import '@testing-library/jest-dom';
import Component from './Component';

global.fetch = jest.fn();

// Mocking the global fetch function
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: jest.fn(() => Promise.resolve({ output: 'Washington D.C.' })),
  }),
);

describe('TextCompletionButton Component', () => {
  it('should hit the /text_completions endpoint when clicked', async () => {
    const mockResponse = { output: 'Washington' };
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(mockResponse),
    });

    render(<Component />);

    const button = screen.getByText('Create Text Completion');
    fireEvent.click(button);

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/v1/b1/text_completions/',
        expect.objectContaining({
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            input: "What's the capital of America?",
          }),
        }),
      );
    });

    expect(global.fetch).toHaveBeenCalledWith(
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

    // Optionally, if you want to test the render result after the API call
    expect(screen.getByText('Washington')).toBeInTheDocument();
  });
  it('should render chat bar at the bottom and allow submission with Enter key', () => {
    render(<Component />);

    // Check that the chat bar is in the document
    const chatBar = screen.getByRole('textbox', { name: /chat input/i }); // assuming you use aria-label="chat input" or similar
    expect(chatBar).toBeInTheDocument();

    // Check that pressing Enter in the chat bar submits the input
    const inputContent = 'Sample query';
    fireEvent.change(chatBar, { target: { value: inputContent } });
    fireEvent.keyDown(chatBar, { key: 'Enter', code: 'Enter' });

    // Assuming you have a function to handle this event which will then process the inputContent
    expect(
      global.fetch,
    ).toHaveBeenCalledWith(/* your expected fetch parameters using inputContent */);

    // Optionally, if you want to check the content at the top, assuming it's a div or some container
    const topContent = screen.getByRole('region', { name: /top content/i }); // using aria-label or similar for the top content area
    expect(topContent).toBeInTheDocument();
  });
});

afterEach(() => {
  jest.clearAllMocks();
});
