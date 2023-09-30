import React from 'react';
import {render, screen, fireEvent, within} from '@testing-library/react';
import '@testing-library/jest-dom'; // for the "toBeInTheDocument" function and other extensions
import userEvent from '@testing-library/user-event';

import ModuleList from './Component'; // Adjust the import path accordingly

describe('<ModuleList />', () => {
  it('should display modules and handle clicks', async () => {
    const mockOnModuleChange = jest.fn();

    global.fetch = jest.fn().mockResolvedValue({
      json: jest.fn().mockResolvedValue([
        { name: 'ModuleA', version: '1.0', backend: 'backendA' },
        { name: 'ModuleB', version: '1.1', backend: 'backendB' }
      ])
    });

    render(<ModuleList onModuleChange={mockOnModuleChange} />);

    const moduleA = await screen.findByText('ModuleA/1.0');
    expect(moduleA).toBeInTheDocument();


    const spanElement = within(moduleA).getByText('ModuleA/1.0');
    userEvent.click(spanElement);

    expect(mockOnModuleChange).toHaveBeenCalledWith('ModuleA', '1.0', 'backendA');
  });
});
