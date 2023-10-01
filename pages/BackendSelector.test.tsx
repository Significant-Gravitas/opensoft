import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import userEvent from '@testing-library/user-event';
import BackendSelector from './BackendSelector';
import { createMemoryHistory } from 'history';
import { useRouter } from 'next/router';
const mockFetch = jest.fn();
global.fetch = mockFetch;
jest.mock('next/router', () => {
  let query = {};

  return {
    useRouter: jest.fn(() => ({
      push: jest.fn((newRoute) => {
        // Update the query object when push is called
        const url = new URL(newRoute, 'http://localhost');
        query = Object.fromEntries(url.searchParams.entries());
      }),
      pathname: '/path',
      query,
    })),
  };
});

describe('BackendSelector', () => {
  afterEach(() => {
    jest.clearAllMocks();
    mockFetch.mockRestore(); // reset the fetch mock
  });

  beforeEach(() => {
    mockFetch.mockResolvedValueOnce({
      json: async () => [
        {
          name: 'testModule',
          version: 'v1',
          backend: 'b1',
        },
        {
          name: 'testModule',
          version: 'v1',
          backend: 'b2',
        },
      ],
    });
  });

  it('changes button color when a backend is selected', async () => {
    const { findByText } = render(
      <BackendSelector moduleName="testModule" onBackendSelect={jest.fn()} />,
    );

    const backend1Button = await findByText('b1');
    expect(backend1Button).not.toHaveStyle('background-color: blue');

    await userEvent.click(backend1Button);

    await waitFor(() => {
      expect(backend1Button).toHaveStyle('background-color: blue');
    });
  });

  it('calls onBackendSelect callback with selected backend', async () => {
    const onBackendSelectMock = jest.fn();
    const { findByText } = render(
      <BackendSelector
        moduleName="testModule"
        onBackendSelect={onBackendSelectMock}
      />,
    );

    const backend1Button = await findByText('b1');
    await userEvent.click(backend1Button);

    await waitFor(() => {
      expect(onBackendSelectMock).toHaveBeenCalledWith('b1');
    });
  });
});
