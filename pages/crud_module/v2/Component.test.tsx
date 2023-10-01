import React from 'react';
import { render, act, fireEvent, waitFor } from '@testing-library/react';
import ModuleList from './Component';  // Adjust the path as needed
import fetchMock from 'jest-fetch-mock';

beforeAll(() => {
  fetchMock.enableMocks();
});

afterEach(() => {
  fetchMock.resetMocks();
});

describe('ModuleList', () => {

  test('renders initial state', () => {
    const { getByText } = render(<ModuleList onModuleChange={() => {}} />);
    expect(getByText('Modules')).toBeInTheDocument();
  });

  test('fetches and displays modules', async () => {
    const mockData = [
      { name: 'Module1', version: '1.0.0', backend: 'backend1' },
      { name: 'Module2', version: '2.0.0', backend: 'backend2' }
    ];

    fetchMock.mockOnce(JSON.stringify(mockData));

    const { getByText } = render(<ModuleList onModuleChange={() => {}} />);

    await waitFor(() => {
      expect(getByText('Module1/1.0.0')).toBeInTheDocument();
      expect(getByText('Module2/2.0.0')).toBeInTheDocument();
    });
  });

  test('handles duplicate modules correctly', async () => {
    const mockData = [
      { name: 'Module1', version: '1.0.0', backend: 'backend1' },
      { name: 'Module1', version: '1.0.0', backend: 'backend1' },
      { name: 'Module2', version: '2.0.0', backend: 'backend2' }
    ];

    fetchMock.mockOnce(JSON.stringify(mockData));

    const { getByText, queryAllByText } = render(<ModuleList onModuleChange={() => {}} />);

    await waitFor(() => {
      expect(queryAllByText('Module1/1.0.0')).toHaveLength(1);
      expect(getByText('Module2/2.0.0')).toBeInTheDocument();
    });
  });

  test('triggers onModuleChange callback when module is clicked', async () => {
    const mockData = [
      { name: 'Module1', version: '1.0.0', backend: 'backend1' }
    ];

    fetchMock.mockOnce(JSON.stringify(mockData));

    const mockCallback = jest.fn();
    const { getByText } = render(<ModuleList onModuleChange={mockCallback} />);

    await waitFor(() => {
      fireEvent.click(getByText('Module1/1.0.0'));
    });

    expect(mockCallback).toHaveBeenCalledWith('Module1', '1.0.0', 'backend1');
  });

  test('displays error on fetch failure', async () => {
    fetchMock.mockRejectOnce(new Error('Failed to fetch'));

    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

    render(<ModuleList onModuleChange={() => {}} />);

    await waitFor(() => {
      expect(consoleSpy).toHaveBeenCalledWith('There was an error fetching the modules', expect.anything());
    });

    consoleSpy.mockRestore();
  });

});
