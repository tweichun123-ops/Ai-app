import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { colors, fonts } from '../theme/theme';

export function HeartPoints({ value }: { value: number }) {
  return (
    <View style={styles.row}>
      <Text style={styles.heart}>♥</Text>
      <Text style={styles.value}>{value}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: 'row', alignItems: 'center', gap: 4 },
  heart: { color: '#FF6E9F', fontSize: 14 },
  value: { color: colors.textPrimary, fontFamily: fonts.medium, fontSize: 13 },
});
