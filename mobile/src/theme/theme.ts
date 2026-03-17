export const colors = {
  primaryGradient: ['#FF9EA3', '#FF5E8A'],
  secondaryGradient: ['#D89AFF', '#E84A6D'],
  background: '#0F0F1A',
  cardBg: 'rgba(26,15,26,0.6)',
  textPrimary: '#FFFFFF',
  textSecondary: '#D0C0FF',
  accentGold: '#FFD700',
  rarity: {
    common: '#A0A0A0',
    rare: '#4A90E2',
    ssr: '#C300FF',
  },
};

export const fonts = {
  regular: 'Pretendard-Regular',
  medium: 'Pretendard-Medium',
  bold: 'Pretendard-Bold',
  script: 'Satisfy-Regular',
};

export const spacing = {
  xs: 4,
  s: 8,
  m: 12,
  l: 16,
  xl: 24,
  xxl: 32,
  xxxl: 48,
};

export const shadows = {
  soft: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.15,
    shadowRadius: 4,
    elevation: 3,
  },
  glow: {
    shadowColor: '#FF5E8A',
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.6,
    shadowRadius: 12,
    elevation: 8,
  },
};

export const tiers = [
  { name: 'Free', price: 0, period: '', highlight: false },
  { name: 'Basic', price: 7.9, period: '/mo', highlight: false },
  { name: 'Pro', price: 17.9, period: '/mo', highlight: true },
  { name: 'Eternal', price: 499, period: 'one-time', highlight: false },
];
