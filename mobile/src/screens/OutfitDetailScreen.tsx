import React from 'react';
import { ImageBackground, StyleSheet, Text, View } from 'react-native';
import { GradientButton } from '../components/GradientButton';
import { RarityBadge } from '../components/RarityBadge';

export function OutfitDetailScreen() {
  return (
    <ImageBackground source={{ uri: 'https://picsum.photos/900/1600?winter' }} style={styles.bg} blurRadius={8}>
      <View style={styles.overlay}>
        <View style={styles.bottomSheet}>
          <Text style={styles.title}>Snowy First Confession Sweater</Text>
          <RarityBadge rarity="rare" />
          <Text style={styles.flavor}>Perfect for first snow confession, +200% warmth</Text>
          <View style={styles.actions}>
            <GradientButton title="Equip Now" onPress={() => {}} style={{ flex: 1 }} />
            <GradientButton title="Generate Selfie" onPress={() => {}} variant="secondary" style={{ flex: 1 }} />
          </View>
        </View>
      </View>
    </ImageBackground>
  );
}

const styles = StyleSheet.create({
  bg: { flex: 1 },
  overlay: { flex: 1, justifyContent: 'flex-end', backgroundColor: 'rgba(0,0,0,0.28)' },
  bottomSheet: { borderTopLeftRadius: 24, borderTopRightRadius: 24, padding: 18, backgroundColor: 'rgba(15,15,26,0.92)', gap: 10 },
  title: { color: '#fff', fontSize: 24, fontWeight: '700' },
  flavor: { color: '#D0C0FF' },
  actions: { flexDirection: 'row', gap: 8, marginTop: 4 },
});
