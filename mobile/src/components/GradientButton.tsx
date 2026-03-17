import React from 'react';
import { Pressable, StyleSheet, Text, ViewStyle } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { colors, fonts, shadows } from '../theme/theme';

type Variant = 'primary' | 'secondary' | 'premium';

type Props = {
  title: string;
  onPress: () => void;
  disabled?: boolean;
  variant?: Variant;
  style?: ViewStyle;
};

const gradientByVariant: Record<Variant, string[]> = {
  primary: colors.primaryGradient,
  secondary: colors.secondaryGradient,
  premium: [colors.accentGold, '#FF9EA3'],
};

export function GradientButton({ title, onPress, disabled, variant = 'primary', style }: Props) {
  return (
    <Pressable onPress={onPress} disabled={disabled} style={[style, disabled && styles.disabled]}>
      <LinearGradient colors={gradientByVariant[variant]} style={[styles.base, variant === 'premium' && styles.premium]}>
        <Text style={styles.title}>{title}</Text>
      </LinearGradient>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  base: {
    borderRadius: 24,
    minHeight: 56,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 20,
    ...shadows.glow,
  },
  premium: {
    borderWidth: 1,
    borderColor: 'rgba(255,215,0,0.8)',
  },
  title: {
    color: colors.textPrimary,
    fontFamily: fonts.bold,
    fontSize: 16,
  },
  disabled: {
    opacity: 0.55,
  },
});
