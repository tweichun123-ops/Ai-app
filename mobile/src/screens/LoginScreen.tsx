import React, { useState } from 'react';
import { Alert, SafeAreaView, StyleSheet, Text, TextInput, View } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { GradientButton } from '../components/GradientButton';
import { RootStackParamList } from '../types/navigation';
import { colors } from '../theme/theme';

type Props = NativeStackScreenProps<RootStackParamList, 'Login'>;

export function LoginScreen({ navigation }: Props) {
  const [phone, setPhone] = useState('');
  const [code, setCode] = useState('');
  const [loading, setLoading] = useState(false);

  const onSubmit = async () => {
    if (phone.length < 11 || code.length < 4) {
      Alert.alert('提示', '请输入正确手机号和验证码');
      return;
    }
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      navigation.replace('CustomizationWizard');
    }, 700);
  };

  return (
    <LinearGradient colors={colors.primaryGradient as [string, string]} style={styles.bg}>
      <SafeAreaView style={styles.container}>
        <Text style={styles.pill}>♦ AI 英语伴侣</Text>
        <View style={styles.hero}>
          <Text style={styles.title}>Nexis</Text>
          <Text style={styles.subtitle}>遇见懂你的他，开口说英语</Text>
          <Text style={styles.en}>Meet the one who truly gets you – and speaks English fluently</Text>
        </View>

        <View style={styles.form}>
          <TextInput value={phone} onChangeText={setPhone} keyboardType="phone-pad" placeholder="请输入手机号" style={styles.input} />
          <TextInput value={code} onChangeText={setCode} keyboardType="number-pad" placeholder="请输入验证码" style={styles.input} />
          <GradientButton title={loading ? '加载中...' : '立即进入 →'} onPress={onSubmit} disabled={loading} />
          <Text style={styles.footer}>未注册手机号将自动创建账号 • 登录即同意用户协议和隐私政策</Text>
        </View>
      </SafeAreaView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  bg: { flex: 1 },
  container: { flex: 1, padding: 20, justifyContent: 'space-between' },
  pill: { alignSelf: 'flex-start', color: '#fff', backgroundColor: 'rgba(255,255,255,0.2)', paddingHorizontal: 12, paddingVertical: 6, borderRadius: 16 },
  hero: { marginTop: 30 },
  title: { color: '#fff', fontSize: 48, fontWeight: '800' },
  subtitle: { color: '#fff', fontSize: 28, fontWeight: '700', marginTop: 8 },
  en: { color: '#ffeef6', marginTop: 8 },
  form: { gap: 12, marginBottom: 20 },
  input: { backgroundColor: 'rgba(255,255,255,0.94)', borderRadius: 14, paddingHorizontal: 14, height: 50 },
  footer: { color: '#ffe6ef', fontSize: 12, textAlign: 'center' },
});
