import React, { useMemo, useState } from 'react';
import { FlatList, Image, Pressable, StyleSheet, Text, View } from 'react-native';
import { Card } from '../components/Card';
import { HeartPoints } from '../components/HeartPoints';
import { RarityBadge } from '../components/RarityBadge';
import { colors } from '../theme/theme';

const MOCK = [
  { id: '1', name: 'Snowy First Confession Sweater', rarity: 'rare', preview: 'https://picsum.photos/420/620?1' },
  { id: '2', name: 'Midnight Date Suit', rarity: 'ssr', preview: 'https://picsum.photos/420/620?2' },
  { id: '3', name: 'Soft Campus Knit', rarity: 'common', preview: 'https://picsum.photos/420/620?3' },
] as const;

export function WardrobeScreen() {
  const [selectedId, setSelectedId] = useState<string>(MOCK[0].id);
  const selected = useMemo(() => MOCK.find((i) => i.id === selectedId) ?? MOCK[0], [selectedId]);

  return (
    <View style={styles.container}>
      <View style={styles.headerRow}>
        <Text style={styles.header}>His Wardrobe</Text>
        <HeartPoints value={1280} />
      </View>

      <View style={styles.mainSplit}>
        <View style={styles.leftList}>
          <FlatList
            data={MOCK}
            keyExtractor={(item) => item.id}
            contentContainerStyle={{ gap: 10 }}
            renderItem={({ item }) => (
              <Pressable onPress={() => setSelectedId(item.id)}>
                <Card glow={item.id === selectedId}>
                  <Text style={styles.itemName}>{item.name}</Text>
                  <RarityBadge rarity={item.rarity} />
                </Card>
              </Pressable>
            )}
          />
        </View>

        <View style={styles.rightPreview}>
          <Card glow>
            <Text style={styles.previewTitle}>Right-side Realtime Preview</Text>
            <Image source={{ uri: selected.preview }} style={styles.previewImage} />
            <Text style={styles.itemName}>{selected.name}</Text>
            <RarityBadge rarity={selected.rarity} />
          </Card>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background, paddingTop: 56, paddingHorizontal: 12 },
  headerRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 },
  header: { color: '#fff', fontSize: 26, fontWeight: '700' },
  mainSplit: { flex: 1, flexDirection: 'row', gap: 10 },
  leftList: { width: '42%' },
  rightPreview: { width: '58%' },
  previewTitle: { color: '#fff', fontWeight: '700', marginBottom: 8 },
  previewImage: { width: '100%', height: 320, borderRadius: 12, marginBottom: 10 },
  itemName: { color: '#fff', marginBottom: 6 },
});
