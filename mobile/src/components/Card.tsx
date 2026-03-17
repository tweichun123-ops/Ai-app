import React, { PropsWithChildren } from 'react';
import { StyleSheet, View, ViewStyle } from 'react-native';
import { colors, shadows } from '../theme/theme';

type Props = PropsWithChildren<{ glow?: boolean; style?: ViewStyle }>;

export function Card({ children, glow, style }: Props) {
  return <View style={[styles.card, glow && styles.glow, style]}>{children}</View>;
}

const styles = StyleSheet.create({
  card: {
    borderRadius: 20,
    padding: 16,
    backgroundColor: colors.cardBg,
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.12)',
    ...shadows.soft,
  },
  glow: {
    borderColor: 'rgba(255,94,138,0.65)',
    ...shadows.glow,
  },
});
