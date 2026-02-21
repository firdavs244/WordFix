import { describe, it, expect } from 'vitest';
import { render } from '@/test/utils';
import { NotificationTypeIcon } from '../components/NotificationTypeIcon';

describe('NotificationTypeIcon', () => {
  it('renders an icon container', () => {
    const { container } = render(<NotificationTypeIcon type="badge_earned" />);
    expect(container.querySelector('[aria-hidden="true"]')).toBeInTheDocument();
  });

  it('applies rarity color for badge_earned', () => {
    const { container } = render(<NotificationTypeIcon type="badge_earned" />);
    const wrapper = container.querySelector('[aria-hidden="true"]');
    expect(wrapper?.className).toContain('text-yellow-400');
  });

  it('applies color for streak_warning', () => {
    const { container } = render(<NotificationTypeIcon type="streak_warning" />);
    const wrapper = container.querySelector('[aria-hidden="true"]');
    expect(wrapper?.className).toContain('text-orange-400');
  });
});
