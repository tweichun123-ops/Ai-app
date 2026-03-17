import React, { useMemo, useState } from 'react';
import {
  Image,
  Pressable,
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { Card } from '../components/Card';
import { GradientButton } from '../components/GradientButton';
import { RarityBadge } from '../components/RarityBadge';
import { colors } from '../theme/theme';
import { RootStackParamList } from '../types/navigation';
import { AvatarTemplate, CustomizationProfile, defaultProfile, LanguageOption, VoiceType } from '../types/customization';

type Props = NativeStackScreenProps<RootStackParamList, 'CustomizationWizard'>;

const languageOptions: { key: LanguageOption; label: string }[] = [
  { key: 'en-US', label: '英语' },
  { key: 'ja-JP', label: '日语' },
  { key: 'ko-KR', label: '韩语' },
];

const templates: { key: AvatarTemplate; label: string; image: string }[] = [
  { key: 'kr_college', label: '韩系大学生', image: 'https://picsum.photos/420/620?kr-college' },
  { key: 'jp_senior', label: '日系温柔学长', image: 'https://picsum.photos/420/620?jp-senior' },
  { key: 'us_executive', label: '欧美商务精英', image: 'https://picsum.photos/420/620?us-exec' },
  { key: 'sunny_athlete', label: '阳光运动型', image: 'https://picsum.photos/420/620?athlete' },
  { key: 'artistic_musician', label: '艺术系音乐人', image: 'https://picsum.photos/420/620?music' },
  { key: 'gentle_researcher', label: '理工温柔研究员', image: 'https://picsum.photos/420/620?research' },
];

const voices: { key: VoiceType; label: string; premium: boolean }[] = [
  { key: 'kr_soft', label: '韩系软糯', premium: false },
  { key: 'jp_cool', label: '日系清冷', premium: true },
  { key: 'en_deep', label: '欧美低沉磁性', premium: true },
];

const stepTitles = ['语言选择', '形象匹配', '性格设置', '声线与称呼', '生成心动照'];

export function CustomizationWizardScreen({ navigation }: Props) {
  const [step, setStep] = useState(0);
  const [profile, setProfile] = useState<CustomizationProfile>(defaultProfile);

  const selectedTemplate = useMemo(() => templates.find((t) => t.key === profile.template) ?? templates[0], [profile.template]);

  const onNext = () => {
    if (step < 4) {
      setStep((v) => v + 1);
      return;
    }
    navigation.replace('Wardrobe');
  };

  const onBack = () => {
    if (step === 0) {
      navigation.goBack();
      return;
    }
    setStep((v) => v - 1);
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.headerRow}>
        <Pressable onPress={onBack}><Text style={styles.back}>← 返回</Text></Pressable>
        <Text style={styles.header}>理想型注册定制</Text>
        <Text style={styles.progress}>{step + 1}/5</Text>
      </View>

      <View style={styles.split}>
        <ScrollView style={styles.left} contentContainerStyle={{ gap: 12, paddingBottom: 24 }}>
          <Text style={styles.stepTitle}>{stepTitles[step]}</Text>
          {step === 0 && (
            <Card>
              <Text style={styles.label}>选择主要交流语言</Text>
              <View style={styles.rowWrap}>
                {languageOptions.map((opt) => (
                  <ChoicePill
                    key={opt.key}
                    active={profile.language === opt.key}
                    label={opt.label}
                    onPress={() => setProfile((p) => ({ ...p, language: opt.key }))}
                  />
                ))}
              </View>
            </Card>
          )}

          {step === 1 && (
            <>
              <Card>
                <Text style={styles.label}>主模板选择</Text>
                <View style={styles.rowWrap}>
                  {templates.map((tpl) => (
                    <ChoicePill
                      key={tpl.key}
                      active={profile.template === tpl.key}
                      label={tpl.label}
                      onPress={() => setProfile((p) => ({ ...p, template: tpl.key }))}
                    />
                  ))}
                </View>
              </Card>
              <Card>
                <Text style={styles.label}>轻度外观自定义</Text>
                <Text style={styles.subLabel}>发色</Text>
                <View style={styles.rowWrap}>
                  {(['black', 'brown', 'gold'] as const).map((c) => (
                    <ChoicePill key={c} active={profile.hairColor === c} label={c} onPress={() => setProfile((p) => ({ ...p, hairColor: c }))} />
                  ))}
                </View>
                <Text style={styles.subLabel}>体型</Text>
                <View style={styles.rowWrap}>
                  {(['slim', 'fit', 'broad'] as const).map((b) => (
                    <ChoicePill key={b} active={profile.bodyType === b} label={b} onPress={() => setProfile((p) => ({ ...p, bodyType: b }))} />
                  ))}
                </View>
              </Card>
            </>
          )}

          {step === 2 && (
            <Card>
              <Text style={styles.label}>性格滑杆（0-100）</Text>
              <MetricRow label="温柔度" value={profile.warmth} onMinus={() => setProfile((p) => ({ ...p, warmth: Math.max(0, p.warmth - 5) }))} onPlus={() => setProfile((p) => ({ ...p, warmth: Math.min(100, p.warmth + 5) }))} />
              <MetricRow label="主动度" value={profile.initiative} onMinus={() => setProfile((p) => ({ ...p, initiative: Math.max(0, p.initiative - 5) }))} onPlus={() => setProfile((p) => ({ ...p, initiative: Math.min(100, p.initiative + 5) }))} />
              <MetricRow label="幽默感" value={profile.humor} onMinus={() => setProfile((p) => ({ ...p, humor: Math.max(0, p.humor - 5) }))} onPlus={() => setProfile((p) => ({ ...p, humor: Math.min(100, p.humor + 5) }))} />
              <MetricRow label="占有欲" value={profile.possessiveness} onMinus={() => setProfile((p) => ({ ...p, possessiveness: Math.max(0, p.possessiveness - 5) }))} onPlus={() => setProfile((p) => ({ ...p, possessiveness: Math.min(100, p.possessiveness + 5) }))} />
            </Card>
          )}

          {step === 3 && (
            <>
              <Card>
                <Text style={styles.label}>声线选择（Pro+ 解锁高级）</Text>
                <View style={styles.rowWrap}>
                  {voices.map((v) => (
                    <ChoicePill
                      key={v.key}
                      active={profile.voice === v.key}
                      label={v.premium ? `${v.label} · Pro+` : v.label}
                      onPress={() => setProfile((p) => ({ ...p, voice: v.key }))}
                    />
                  ))}
                </View>
              </Card>
              <Card>
                <Text style={styles.label}>专属称呼</Text>
                <TextInput value={profile.nickname} onChangeText={(text) => setProfile((p) => ({ ...p, nickname: text || '宝贝' }))} style={styles.input} placeholder="例如：小仙女" placeholderTextColor="#b8a9d8" />
              </Card>
            </>
          )}

          {step === 4 && (
            <Card glow>
              <Text style={styles.label}>一键生成首张心动照</Text>
              <Text style={styles.desc}>已完成理想型注册定制，点击下方按钮生成“我们的第一张心动照”，并进入衣橱继续解锁搭配。</Text>
              <RarityBadge rarity="ssr" />
            </Card>
          )}

          <GradientButton title={step < 4 ? '下一步 →' : '生成并进入衣橱'} onPress={onNext} />
        </ScrollView>

        <View style={styles.right}>
          <Card glow style={{ flex: 1 }}>
            <Text style={styles.previewTitle}>右侧即时预览</Text>
            <Image source={{ uri: selectedTemplate.image }} style={styles.previewImage} />
            <Text style={styles.previewName}>{selectedTemplate.label}</Text>
            <Text style={styles.previewMeta}>语言：{profile.language} · 发色：{profile.hairColor} · 体型：{profile.bodyType}</Text>
            <Text style={styles.previewMeta}>性格：温柔{profile.warmth}/主动{profile.initiative}/幽默{profile.humor}/占有{profile.possessiveness}</Text>
            <Text style={styles.previewMeta}>声线：{profile.voice} · 称呼：{profile.nickname}</Text>
          </Card>
        </View>
      </View>
    </SafeAreaView>
  );
}

function ChoicePill({ label, active, onPress }: { label: string; active: boolean; onPress: () => void }) {
  return (
    <Pressable onPress={onPress} style={[styles.pill, active && styles.pillActive]}>
      <Text style={[styles.pillText, active && styles.pillTextActive]}>{label}</Text>
    </Pressable>
  );
}

function MetricRow({ label, value, onMinus, onPlus }: { label: string; value: number; onMinus: () => void; onPlus: () => void }) {
  return (
    <View style={styles.metricRow}>
      <Text style={styles.metricLabel}>{label}</Text>
      <View style={styles.metricControls}>
        <Pressable onPress={onMinus} style={styles.metricBtn}><Text style={styles.metricBtnText}>-</Text></Pressable>
        <Text style={styles.metricValue}>{value}</Text>
        <Pressable onPress={onPlus} style={styles.metricBtn}><Text style={styles.metricBtnText}>+</Text></Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#121126', paddingTop: 8 },
  headerRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: 12, paddingVertical: 8 },
  back: { color: '#d8c8ff', fontSize: 14 },
  header: { color: '#fff', fontSize: 20, fontWeight: '700' },
  progress: { color: '#ffd7ea', fontSize: 13 },
  split: { flex: 1, flexDirection: 'row', gap: 10, paddingHorizontal: 12, paddingBottom: 12 },
  left: { width: '44%' },
  right: { width: '56%' },
  stepTitle: { color: '#fff', fontSize: 18, fontWeight: '700', marginBottom: 2 },
  label: { color: '#fff', fontSize: 15, fontWeight: '600', marginBottom: 8 },
  subLabel: { color: '#d5c5ff', marginTop: 6, marginBottom: 6 },
  desc: { color: '#d0c0ff', lineHeight: 20, marginBottom: 10 },
  rowWrap: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  pill: { borderRadius: 999, borderWidth: 1, borderColor: 'rgba(255,255,255,0.2)', paddingHorizontal: 12, paddingVertical: 6 },
  pillActive: { borderColor: '#FF5E8A', backgroundColor: 'rgba(255,94,138,0.2)' },
  pillText: { color: '#ddd', fontSize: 12 },
  pillTextActive: { color: '#fff' },
  input: { height: 44, borderRadius: 12, borderWidth: 1, borderColor: 'rgba(255,255,255,0.2)', color: '#fff', paddingHorizontal: 10 },
  metricRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', paddingVertical: 6 },
  metricLabel: { color: '#fff' },
  metricControls: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  metricBtn: { width: 26, height: 26, borderRadius: 13, alignItems: 'center', justifyContent: 'center', backgroundColor: 'rgba(255,255,255,0.14)' },
  metricBtnText: { color: '#fff', fontWeight: '700' },
  metricValue: { color: '#ffd7ea', minWidth: 30, textAlign: 'center' },
  previewTitle: { color: colors.textPrimary, fontWeight: '700', marginBottom: 8 },
  previewImage: { width: '100%', height: 300, borderRadius: 12, marginBottom: 10 },
  previewName: { color: '#fff', fontSize: 16, fontWeight: '600', marginBottom: 6 },
  previewMeta: { color: '#d0c0ff', fontSize: 12, marginBottom: 4 },
});
