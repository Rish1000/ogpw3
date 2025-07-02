import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from '../App';

describe('App', () => {
  it('renders OGPW title', () => {
    render(<App />);
    expect(screen.getByText('OGPW')).toBeInTheDocument();
  });

  it('renders upload interface initially', () => {
    render(<App />);
    expect(screen.getByText('OGPW Network Analysis')).toBeInTheDocument();
  });
});