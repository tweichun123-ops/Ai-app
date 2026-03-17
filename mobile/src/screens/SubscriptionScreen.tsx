import React from 'react';
import { ScrollView, StyleSheet, Text, View } from 'react-native';
import { Card } from '../components/Card';
import { GradientButton } from '../components/GradientButton';
import { tiers, colors } from '../theme/theme';

export function SubscriptionScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.header}>Choose Your Love Level</Text>
      <ScrollView contentContainerStyle={styles.content}>
        {tiers.filter((t) => t.name !== 'Free').map((tier) => (
          <Card key={tier.name} glow={tier.highlight}>
            <Text style={styles.name}>{tier.name}</Text>
            <Text style={styles.price}>${tier.price} {tier.period}</Text>
            <Text style={styles.desc}>Premium emotional companion + language growth benefits.</Text>
          </Card>
        ))}
      </ScrollView>
      <GradientButton title="Unlock Now" onPress={() => {}} style={styles.cta} />
      <Text style={styles.footer}>Cancel anytime • Secure payment</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background, paddingTop: 60, paddingHorizontal: 16 },
  header: { color: '#fff', fontSize: 28, fontWeight: '700' },
  content: { gap: 12, paddingVertical: 16 },
  name: { color: '#fff', fontSize: 18, fontWeight: '700' },
  price: { color: '#FFD7E9', fontSize: 22, fontWeight: '800', marginTop: 4 },
  desc: { color: '#D0C0FF', marginTop: 8 },
  cta: { marginTop: 6 },
  footer: { color: '#AFA1CC', textAlign: 'center', marginTop: 10, marginBottom: 20 },
});
