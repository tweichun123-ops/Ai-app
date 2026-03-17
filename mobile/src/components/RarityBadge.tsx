import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { colors, fonts } from '../theme/theme';

type Rarity = 'common' | 'rare' | 'ssr';

export function RarityBadge({ rarity }: { rarity: Rarity }) {
  return (
    <View style={[styles.base, { backgroundColor: colors.rarity[rarity] }]}> 
      <Text style={styles.text}>{rarity.toUpperCase()}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  base: {
    borderRadius: 999,
    paddingHorizontal: 10,
    paddingVertical: 4,
    alignSelf: 'flex-start',
  },
  text: {
    color: '#fff',
    fontFamily: fonts.bold,
    fontSize: 10,
    letterSpacing: 0.6,
  },
});
